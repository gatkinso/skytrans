package main

import (
	"context"
	"flag"
	"fmt"
	"log"
	"net"
	"time"

	es "github.com/gatkinso/gomac/endpointsecurity"

	"google.golang.org/grpc"

	"github.com/neo4j/neo4j-go-driver/v4/neo4j"

	pb "gotrans/skytransproto/transport/proto"

	"google.golang.org/protobuf/proto"
	pi "google.golang.org/protobuf/runtime/protoimpl"
	"google.golang.org/protobuf/types/known/anypb"
)

var (
	port = flag.Int("port", 1967, "The server port")
)

// server is used to implement TransportServer.
type server struct {
	pb.UnimplementedTransportServer

	id     uint64
	driver neo4j.Driver
}

func (s *server) GetString(msg *pb.Request) string {
	return pi.X.MessageStringOf(msg)
}

type ProcessItem struct {
	actor_start_time  uint32 `bson:"start_time"`
	actor_pid         uint32 `bson:"pid"`
	parent_start_time uint32 `bson:"parent_start_time"`
	actor_ppid        uint32 `bson:"ppid"`
}

func (s *server) DoTransactionEvent(id uint64, msg *pb.Request) error {
	start := time.Now()

	session := s.driver.NewSession(neo4j.SessionConfig{AccessMode: neo4j.AccessModeWrite})
	defer session.Close()

	tx, _ := session.BeginTransaction()

	hostname := msg.Meta.Data.GetStringValues()["Hostname"]

	log.Printf("Batch %v  (%v).....", id, len(msg.GetImpl()))

	for i, item := range msg.GetImpl() {
		var s pb.Stencil
		err := anypb.UnmarshalTo(item, &s, proto.UnmarshalOptions{})

		if err != nil {
			log.Printf("UnmarshalTo failed %v\n", i)
			return err
		}

		var cypherQueryStr string
		var variableMap map[string]interface{}

		processItem := ProcessItem{
			actor_start_time:  s.GetUintValues()["actor_start_time"],
			actor_pid:         s.GetUintValues()["actor_pid"],
			parent_start_time: s.GetUintValues()["parent_start_time"],
			actor_ppid:        s.GetUintValues()["actor_ppid"],
		}

		event_type := s.GetUintValues()["event_type"]
		switch event_type {
		case uint32(es.ES_EVENT_TYPE_NOTIFY_EXEC):
			cypherQueryStr =
				`MERGE (actor:Process {start_time:$actor_start_time, pid:$actor_pid})
				ON CREATE
					SET actor.ppid = $actor_ppid, 
						actor.parent_start_time = $parent_start_time, 
						actor.pathname = $actor_pathname, 
						actor.filename = $actor_filename
				WITH actor
				MERGE (target:Process:Execed {start_time:$target_start_time, pid:$tgt_pid})
				ON CREATE
					SET target.created = true,
						target.parent_start_time = $actor_start_time, 
						target.ppid = $tgt_ppid,
						target.pathname = $tgt_pathname, 
						target.filename = $tgt_filename
				WITH actor, target
				FOREACH(ignoreMe IN CASE WHEN target.created = true THEN [1] ELSE [] END|
					SET target.created = false
					MERGE (actor)-[r:EXEC]-(target)
				)`

			variableMap = map[string]interface{}{
				"hostname":          hostname,
				"actor_start_time":  s.GetUintValues()["actor_start_time"],
				"actor_pid":         s.GetUintValues()["actor_pid"],
				"parent_start_time": s.GetUintValues()["parent_start_time"],
				"actor_ppid":        s.GetUintValues()["actor_ppid"],
				"actor_pathname":    s.GetStringValues()["actor_executable_path"],
				"actor_filename":    s.GetStringValues()["actor_executable_name"],
				"target_start_time": s.GetUintValues()["target_start_time"],
				"tgt_pid":           s.GetUintValues()["tgt_pid"],
				"tgt_ppid":          s.GetUintValues()["tgt_ppid"],
				"tgt_pathname":      s.GetStringValues()["tgt_executable_path"],
				"tgt_filename":      s.GetStringValues()["tgt_executable_name"]}

		case uint32(es.ES_EVENT_TYPE_NOTIFY_FORK):
			cypherQueryStr =
				`MERGE (actor:Process {start_time:$actor_start_time, pid:$actor_pid})
						ON CREATE
							SET actor.ppid = $actor_ppid,
								actor.parent_start_time = $parent_start_time,
								actor.pathname = $actor_pathname,
								actor.filename = $actor_filename
						WITH actor
						MERGE (target:Process:Forked {start_time:$child_start_time, pid:$tgt_pid})
						ON CREATE
							SET target.created = true,
								target.parent_start_time = $actor_start_time,
								target.ppid = $tgt_ppid,
								target.pathname = $tgt_pathname,
								target.filename = $tgt_filename
						WITH actor, target
						FOREACH(ignoreMe IN CASE WHEN target.created = true THEN [1] ELSE [] END|
							SET target.created = false
							MERGE (actor)-[r:FORK]-(target)
						)`

			variableMap = map[string]interface{}{
				"hostname":          hostname,
				"actor_start_time":  s.GetUintValues()["actor_start_time"],
				"actor_pid":         s.GetUintValues()["actor_pid"],
				"parent_start_time": s.GetUintValues()["parent_start_time"],
				"actor_ppid":        s.GetUintValues()["actor_ppid"],
				"actor_pathname":    s.GetStringValues()["actor_executable_path"],
				"actor_filename":    s.GetStringValues()["actor_executable_name"],
				"child_start_time":  s.GetUintValues()["child_start_time"],
				"tgt_pid":           s.GetUintValues()["tgt_pid"],
				"tgt_ppid":          s.GetUintValues()["tgt_ppid"],
				"tgt_pathname":      s.GetStringValues()["tgt_executable_path"],
				"tgt_filename":      s.GetStringValues()["tgt_executable_name"]}

		case uint32(es.ES_EVENT_TYPE_LAST + 1): //TODO define proper value type for discovered processes
			if processItem.actor_pid == 1 {
				cypherQueryStr =
					`MERGE (h:Host {hostname:$hostname})
							WITH h
							MERGE (actor:Process:Discovered {start_time:$actor_start_time, pid:$actor_pid})
							ON CREATE
								SET
									actor.pathname = $pathname,
									actor.filename = $filename,
									actor.parent_start_time = $parent_start_time,
									actor.ppid = $actor_ppid
							WITH actor, h
							MERGE (actor)-[r:RAN_ON]-(h)`
			} else {
				cypherQueryStr =
					`MERGE (h:Host {hostname:$hostname})
							WITH h
							MERGE (parent:Process:Discovered {start_time:$parent_start_time, pid:$actor_ppid})
							MERGE (actor:Process:Discovered {start_time:$actor_start_time, pid:$actor_pid})
							ON CREATE
								SET
									actor.pathname = $pathname,
									actor.filename = $filename,
									actor.parent_start_time = $parent_start_time,
									actor.ppid = $actor_ppid
							WITH parent, actor
							FOREACH(ignoreMe IN CASE WHEN parent IS NOT null THEN [1] ELSE [] END|
								MERGE (actor)-[r:CHILD]-(parent)
							)
							FOREACH(ignoreMe IN CASE WHEN parent IS null THEN [1] ELSE [] END|
								MERGE (actor)-[r:RAN_ON]-(h)
							)`
			}

			variableMap = map[string]interface{}{
				"hostname":          hostname,
				"actor_start_time":  s.GetUintValues()["actor_start_time"],
				"actor_pid":         s.GetUintValues()["actor_pid"],
				"parent_start_time": s.GetUintValues()["parent_start_time"],
				"actor_ppid":        s.GetUintValues()["actor_ppid"],
				"pathname":          s.GetStringValues()["actor_executable_path"],
				"filename":          s.GetStringValues()["actor_executable_name"]}
		default:
			continue
		}

		res, err := tx.Run(cypherQueryStr, variableMap)

		if err != nil {
			log.Printf("Run %d failed %v%v\n", i, err, res)
			return err
		}

		//return result.Consume()
		//})
		//if err != nil {
		//	log.Printf("WriteTransaction failed: %v", err)
		//	return err
		//}
	}

	tx.Commit()

	duration := time.Since(start)

	secs := float32(duration.Milliseconds()) / 1000

	log.Printf("Finshed Batch %v (%v) in %v ms. Rate: %v", id, len(msg.GetImpl()), duration.Milliseconds(), float32(len(msg.GetImpl()))/secs)

	return nil
}

// Implements TransportServer
func (s *server) Exchange(ctx context.Context, req *pb.Request) (*pb.Response, error) {
	//log.Printf(s.GetString(in))
	s.id += 1
	s.DoTransactionEvent(s.id, req)

	var res pb.Response

	return &res, nil
}

func main() {
	flag.Parse()

	log.SetFlags(log.LstdFlags | log.Lmicroseconds)

	lis, err := net.Listen("tcp", fmt.Sprintf(":%d", *port))
	if err != nil {
		log.Fatalf("failed to listen: %v", err)
	}

	driver_, err := neo4j.NewDriver("neo4j://neo01:7687", neo4j.BasicAuth("neo4j", "password", ""))
	if err != nil {
		log.Fatalf("NewDriver failed")
		return
	}
	defer driver_.Close()

	myserver := grpc.NewServer()
	pb.RegisterTransportServer(myserver, &server{id: 0, driver: driver_})

	log.Printf("server listening at %v", lis.Addr())

	if err := myserver.Serve(lis); err != nil {
		log.Fatalf("failed to serve: %v", err)
	}
}
