package main

import (
	"context"
	"flag"
	"fmt"
	"log"
	"net"

	"google.golang.org/grpc"

	"github.com/neo4j/neo4j-go-driver/v4/neo4j"

	pb "transport"

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
}

func (s *server) GetString(msg *pb.Request) string {
	return pi.X.MessageStringOf(msg)
}

func (s *server) DoEvent(msg *pb.Request, uri, username, password string) error {
	driver, err := neo4j.NewDriver(uri, neo4j.BasicAuth(username, password, ""))
	if err != nil {
		log.Printf("NewDriver failed")
		return err
	}
	defer driver.Close()

	session := driver.NewSession(neo4j.SessionConfig{AccessMode: neo4j.AccessModeWrite})
	defer session.Close()

	log.Printf("Processing %v.....", len(msg.GetImpl()))
	for i, item := range msg.GetImpl() {
		var s pb.Stencil
		err := anypb.UnmarshalTo(item, &s, proto.UnmarshalOptions{})

		_, err = session.WriteTransaction(func(transaction neo4j.Transaction) (interface{}, error) {
			result, err := transaction.Run(
				`MERGE (h:Host {hostname:$hostname}) 
				 MERGE (p:Process {pid:$pid, pathname:$pathname, filename:$filename}) 
				 MERGE (p)-[r:RAN_ON]-(h)`,
				map[string]interface{}{
					"hostname": msg.Meta.Data.GetStringValues()["Hostname"],
					"pid":      s.GetIntValues()["process->pid"],
					"pathname": s.GetStringValues()["process->executable->path"],
					"filename": s.GetStringValues()["process->executable->filename"]})
			if err != nil {
				log.Printf("Run failed %v", i)
				return nil, err
			}

			return result.Consume()
		})
		if err != nil {
			log.Printf("WriteTransaction failed: %v", err)
			return err
		}
	}

	log.Printf(" done")

	return err
}

// SayHello implements TransportServer
func (s *server) Exchange(ctx context.Context, in *pb.Request) (*pb.Response, error) {
	//log.Printf(s.GetString(in))
	s.DoEvent(in, "neo4j://192.168.135.199:7687", "neo4j", "password")
	return &pb.Response{}, nil
}

func main() {
	flag.Parse()

	log.SetFlags(log.LstdFlags | log.Lmicroseconds)

	lis, err := net.Listen("tcp", fmt.Sprintf(":%d", *port))
	if err != nil {
		log.Fatalf("failed to listen: %v", err)
	}

	myserver := grpc.NewServer()
	pb.RegisterTransportServer(myserver, &server{})

	log.Printf("server listening at %v", lis.Addr())

	if err := myserver.Serve(lis); err != nil {
		log.Fatalf("failed to serve: %v", err)
	}
}
