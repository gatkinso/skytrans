package main

import (
	"context"
	"log"
	"net"

	"go.mongodb.org/mongo-driver/mongo"
	"go.mongodb.org/mongo-driver/mongo/options"
	"google.golang.org/grpc"

	pb "gotrans/skytransproto/transport/proto"
)

var esNotifyCollection *mongo.Collection
var esAuthCollection *mongo.Collection
var esMetaCollection *mongo.Collection

var addr string = "0.0.0.0:1967"

type Server struct {
	pb.TransportServer
}

func main() {
	client, err := mongo.NewClient(options.Client().ApplyURI("mongodb://mongo-pm1:27017/"))
	if err != nil {
		log.Fatal(err)
	}

	err = client.Connect(context.Background())
	if err != nil {
		log.Fatal(err)
	}

	esNotifyCollection = client.Database("anubixdb").Collection("notify")
	esAuthCollection = client.Database("anubixdb").Collection("auth")
	esMetaCollection = client.Database("anubixdb").Collection("meta")

	lis, err := net.Listen("tcp", addr)

	if err != nil {
		log.Fatalf("Failed to listen on: %v\n", err)
	}

	log.Printf("Listening on %s\n", addr)

	s := grpc.NewServer()
	pb.RegisterTransportServer(s, &Server{})

	if err = s.Serve(lis); err != nil {
		log.Fatalf("Failed to serve: %v\n", err)
	}
}
