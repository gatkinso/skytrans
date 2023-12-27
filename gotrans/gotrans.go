package main

import (
	"context"
	"flag"
	"fmt"
	"log"
	"net"
	"time"

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

func (s *server) DoEvent(id uint64, msg *pb.Request) error {
	start := time.Now()

	session := s.driver.NewSession(neo4j.SessionConfig{AccessMode: neo4j.AccessModeWrite})
	defer session.Close()

	//log.Printf("Batch %v  (%v).....", id, len(msg.GetImpl()))
	for i, item := range msg.GetImpl() {
		var s pb.Stencil
		err := anypb.UnmarshalTo(item, &s, proto.UnmarshalOptions{})

		if err != nil {
			log.Printf("UnmarshalTo failed: %v\n", err)
			return err
		}

		_, err = session.WriteTransaction(func(transaction neo4j.Transaction) (interface{}, error) {
			result, err := transaction.Run(
				`MERGE (h:Host {hostname:$hostname}) 
				 MERGE (p:Process {pid:$pid, ppid:$ppid, pathname:$actor_executable_path, start_time:$actor_start_time}) 
				 MERGE (p)-[r:RAN_ON]-(h)`,
				map[string]interface{}{
					"hostname":              msg.Meta.Data.GetStringValues()["hostname"],
					"pid":                   s.GetIntValues()["actor_pid"],
					"ppid":                  s.GetIntValues()["actor_ppid"],
					"actor_start_time":      s.GetInt64Values()["actor_start_time"],
					"actor_executable_path": s.GetStringValues()["actor_executable_path"]})
			if err != nil {
				log.Printf("Run failed %v", i)
				return nil, err
			}

			return result.Consume()
		})
		if err != nil {
			log.Printf("WriteTransaction failed: %v\n", err)
			return err
		}
	}

	duration := time.Since(start)

	secs := float32(duration.Milliseconds()) / 1000

	log.Printf("Finshed Batch %v (%v) in %v ms. Rate: %v", id, len(msg.GetImpl()), duration.Milliseconds(), float32(len(msg.GetImpl()))/secs)

	return nil
}

func (s *server) DoTransactionEvent(id uint64, msg *pb.Request) error {
	start := time.Now()

	session := s.driver.NewSession(neo4j.SessionConfig{AccessMode: neo4j.AccessModeWrite})
	defer session.Close()

	tx, _ := session.BeginTransaction()

	log.Printf("Batch %v  (%v).....", id, len(msg.GetImpl()))

	for i, item := range msg.GetImpl() {
		var s pb.Stencil
		err := anypb.UnmarshalTo(item, &s, proto.UnmarshalOptions{})

		if err != nil {
			log.Printf("UnmarshalTo failed %v\n", i)
			return err
		}

		teat1 := s.GetUintValues()["actor_start_time"]

		_, err = tx.Run(
			`MERGE (h:Host {hostname:$hostname})
			 MERGE (actor:Process {start_time:$start_time, pid:$pid, parent_start_time:$parent_start_time, ppid:$ppid, pathname:$pathname, filename:$filename})
			 MERGE (actor)-[r:RAN_ON]-(h)`,
			map[string]interface{}{
				"hostname": msg.Meta.Data.GetStringValues()["hostname"], //this only needs to happen once.

				"session_id": s.GetUint64Values()["session_id"],

				"sequence_num": s.GetUint64Values()["sequence_num"],

				"start_time":        teat1,
				"pid":               s.GetUintValues()["actor_pid"],
				"parent_start_time": s.GetUintValues()["parent_start_time"],
				"ppid":              s.GetUintValues()["actor_ppid"],
				"pathname":          s.GetStringValues()["actor_executable_path"],
				"filename":          s.GetStringValues()["actor_executable_name"]})

		if err != nil {
			log.Printf("Run %d failed %v\n", i, err)
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

// SayHello implements TransportServer
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
