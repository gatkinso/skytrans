// Implements TransportServer
package main

import (
	"context"
	"fmt"
	pb "gotrans/skytransproto/transport/proto"
	"log"
	"time"

	es "github.com/gatkinso/gomac/endpointsecurity"
	"go.mongodb.org/mongo-driver/mongo"

	"google.golang.org/grpc/codes"
	"google.golang.org/grpc/status"
)

func (s *Server) DoTransactionEvent(ctx context.Context, msg *pb.Request) error {
	start := time.Now()

	id := msg.GetMeta().Data.Uint64Values["req_id"]

	for _, item := range msg.GetEvents() {

		var res *mongo.InsertOneResult
		var err error

		res = nil
		err = nil

		switch item.Esevent.EventType {
		case uint32(es.ES_EVENT_TYPE_NOTIFY_EXEC):
			res, err = execCollection.InsertOne(ctx, item.Esevent.Exec)

		case uint32(es.ES_EVENT_TYPE_NOTIFY_FORK):
			res, err = forkCollection.InsertOne(ctx, item.Esevent.Fork)

		case uint32(es.ES_EVENT_TYPE_NOTIFY_EXIT):
			res, err = exitCollection.InsertOne(ctx, item.Esevent.Exit)

		case uint32(es.ES_EVENT_TYPE_LAST + 1):

		default:
			continue
		}

		if res != nil && err != nil {
			return status.Errorf(
				codes.Internal,
				fmt.Sprintf("Internal error: %v\n", err),
			)
		}
		_, err = actorCollection.InsertOne(ctx, item.Esevent.Process)

		if err != nil {
			return status.Errorf(
				codes.Internal,
				fmt.Sprintf("Internal error: %v\n", err),
			)
		}
	}

	duration := time.Since(start)

	secs := float32(duration.Milliseconds()) / 1000

	log.Printf("Finshed Batch (%d) of count (%d) in %v ms. Rate: %v", id, len(msg.GetEvents()), duration.Milliseconds(), float32(len(msg.GetEvents()))/secs)

	return nil
}

func (s *Server) Exchange(ctx context.Context, req *pb.Request) (*pb.Response, error) {
	s.DoTransactionEvent(ctx, req)

	var res pb.Response

	return &res, nil
}
