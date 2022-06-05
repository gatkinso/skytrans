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

	pi "google.golang.org/protobuf/runtime/protoimpl"
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

	//"CREATE (a:Greeting) SET a.message = $message RETURN a.message + ', from node ' + id(a)",
	//map[string]interface{}{"message": "hello, world"})

	var gmt string
	gmt = msg.Meta.Data.GetStringValues()["GMT Time"]
	var hostname string
	hostname = msg.Meta.Data.GetStringValues()["Hostname"]
	//log.Printf("%s :  %s", gmt, hostname)
	//log.Printf(pi.X.MessageStringOf(msg.Meta.Data))
	_, err = session.WriteTransaction(func(transaction neo4j.Transaction) (interface{}, error) {
		result, err := transaction.Run(
			"CREATE (p:Process) SET p = {gmt:$gmt, hostname:$hostname}",
			map[string]interface{}{"gmt": gmt, "hostname": hostname})
		if err != nil {
			log.Printf("Run failed")
			return nil, err
		}

		return result.Consume()
	})
	if err != nil {
		log.Printf("WriteTransaction failed: %v", err)
		return err
	}

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
