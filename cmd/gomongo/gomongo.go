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

var execCollection *mongo.Collection
var forkCollection *mongo.Collection
var exitCollection *mongo.Collection
var actorCollection *mongo.Collection
var itemCollection *mongo.Collection

var addr string = "0.0.0.0:1967"

type Server struct {
	pb.TransportServer
}

func main() {
	client, err := mongo.NewClient(options.Client().ApplyURI("mongodb://root:root@localhost:27017/"))
	if err != nil {
		log.Fatal(err)
	}

	err = client.Connect(context.Background())
	if err != nil {
		log.Fatal(err)
	}

	execCollection = client.Database("anubixdb").Collection("exec")
	forkCollection = client.Database("anubixdb").Collection("fork")
	exitCollection = client.Database("anubixdb").Collection("exit")
	actorCollection = client.Database("anubixdb").Collection("actor")
	itemCollection = client.Database("anubixdb").Collection("item")

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
