package main

import (
	"context"
	"flag"
	"fmt"
	"log"
	"net"

	"google.golang.org/grpc"

	pi "google.golang.org/protobuf/runtime/protoimpl"

	pb "transport"
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

// SayHello implements TransportServer
func (s *server) Exchange(ctx context.Context, in *pb.Request) (*pb.Response, error) {
	log.Printf(s.GetString(in))
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
