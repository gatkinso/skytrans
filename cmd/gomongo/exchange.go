// Implements TransportServer
package main

import (
	"context"
	"fmt"
	pb "gotrans/skytransproto/transport/proto"
	"log"
	"time"

	"go.mongodb.org/mongo-driver/mongo"

	"google.golang.org/grpc/codes"
	"google.golang.org/grpc/status"
)

func (s *Server) DoTransactionEvent(ctx context.Context, msg *pb.Request) error {
	if len(msg.GetPbEsMessages()) == 0 {
		return nil
	}

	start := time.Now()

	id := msg.GetMeta().Data.Uint64Values["req_id"]

	var fmtStr string
	var setStr bool
	setStr = true

	for _, item := range msg.GetPbEsMessages() {
		var res *mongo.InsertOneResult
		var err error

		res = nil
		err = nil

		switch item.ActionType {
		case pb.PbEsActionTypeT_PB_ES_ACTION_TYPE_AUTH:
			res, err = esAuthCollection.InsertOne(ctx, item)
			if setStr {
				fmtStr = "(%d) Auth count   [%d] \tin %d ms. Rate: %d/sec"
				setStr = false
			}

		case pb.PbEsActionTypeT_PB_ES_ACTION_TYPE_NOTIFY:
			res, err = esNotifyCollection.InsertOne(ctx, item)
			if setStr {
				fmtStr = "(%d) Notify count (%d) \tin %d ms. Rate: %d/sec"
				setStr = false
			}

		default:
			continue
		}

		if res != nil && err != nil {
			return status.Errorf(
				codes.Internal,
				fmt.Sprintf("Internal error: %v\n", err),
			)
		}
	}

	duration := time.Since(start)
	secs := float32(duration.Milliseconds()) / 1000
	log.Printf(fmtStr, id, len(msg.GetPbEsMessages()), duration.Milliseconds(), int32(float32(len(msg.GetPbEsMessages()))/secs))

	return nil
}

func (s *Server) Exchange(ctx context.Context, req *pb.Request) (*pb.Response, error) {
	s.DoTransactionEvent(ctx, req)

	var res pb.Response

	return &res, nil
}
