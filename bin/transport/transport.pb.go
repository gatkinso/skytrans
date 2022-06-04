//
//  Copyright (C) 2017 Skyloupe, LLC
//
//  Licensed under the Apache License, Version 2.0 (the "License").
//  You may not use this file except in compliance with the License.
//  A copy of the License is located at
//
//  https://www.apache.org/licenses/LICENSE-2.0.html
//
//  or in the "license" file accompanying this file. This file is distributed
//  on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
//  express or implied. See the License for the specific language governing
//  permissions and limitations under the License.
//

// Code generated by protoc-gen-go. DO NOT EDIT.
// versions:
// 	protoc-gen-go v1.28.0
// 	protoc        v3.19.4
// source: transport.proto

package com_skyloupe_skytrans

import (
	protoreflect "google.golang.org/protobuf/reflect/protoreflect"
	protoimpl "google.golang.org/protobuf/runtime/protoimpl"
	anypb "google.golang.org/protobuf/types/known/anypb"
	reflect "reflect"
	sync "sync"
)

const (
	// Verify that this generated code is sufficiently up-to-date.
	_ = protoimpl.EnforceVersion(20 - protoimpl.MinVersion)
	// Verify that runtime/protoimpl is sufficiently up-to-date.
	_ = protoimpl.EnforceVersion(protoimpl.MaxVersion - 20)
)

type Metadata struct {
	state         protoimpl.MessageState
	sizeCache     protoimpl.SizeCache
	unknownFields protoimpl.UnknownFields

	Data *Stencil `protobuf:"bytes,10,opt,name=data,proto3" json:"data,omitempty"`
}

func (x *Metadata) Reset() {
	*x = Metadata{}
	if protoimpl.UnsafeEnabled {
		mi := &file_transport_proto_msgTypes[0]
		ms := protoimpl.X.MessageStateOf(protoimpl.Pointer(x))
		ms.StoreMessageInfo(mi)
	}
}

func (x *Metadata) String() string {
	return protoimpl.X.MessageStringOf(x)
}

func (*Metadata) ProtoMessage() {}

func (x *Metadata) ProtoReflect() protoreflect.Message {
	mi := &file_transport_proto_msgTypes[0]
	if protoimpl.UnsafeEnabled && x != nil {
		ms := protoimpl.X.MessageStateOf(protoimpl.Pointer(x))
		if ms.LoadMessageInfo() == nil {
			ms.StoreMessageInfo(mi)
		}
		return ms
	}
	return mi.MessageOf(x)
}

// Deprecated: Use Metadata.ProtoReflect.Descriptor instead.
func (*Metadata) Descriptor() ([]byte, []int) {
	return file_transport_proto_rawDescGZIP(), []int{0}
}

func (x *Metadata) GetData() *Stencil {
	if x != nil {
		return x.Data
	}
	return nil
}

type Request struct {
	state         protoimpl.MessageState
	sizeCache     protoimpl.SizeCache
	unknownFields protoimpl.UnknownFields

	Meta    *Metadata    `protobuf:"bytes,10,opt,name=meta,proto3" json:"meta,omitempty"`
	Payload *Stencil     `protobuf:"bytes,100,opt,name=payload,proto3" json:"payload,omitempty"`
	Impl    []*anypb.Any `protobuf:"bytes,1000,rep,name=impl,proto3" json:"impl,omitempty"`
}

func (x *Request) Reset() {
	*x = Request{}
	if protoimpl.UnsafeEnabled {
		mi := &file_transport_proto_msgTypes[1]
		ms := protoimpl.X.MessageStateOf(protoimpl.Pointer(x))
		ms.StoreMessageInfo(mi)
	}
}

func (x *Request) String() string {
	return protoimpl.X.MessageStringOf(x)
}

func (*Request) ProtoMessage() {}

func (x *Request) ProtoReflect() protoreflect.Message {
	mi := &file_transport_proto_msgTypes[1]
	if protoimpl.UnsafeEnabled && x != nil {
		ms := protoimpl.X.MessageStateOf(protoimpl.Pointer(x))
		if ms.LoadMessageInfo() == nil {
			ms.StoreMessageInfo(mi)
		}
		return ms
	}
	return mi.MessageOf(x)
}

// Deprecated: Use Request.ProtoReflect.Descriptor instead.
func (*Request) Descriptor() ([]byte, []int) {
	return file_transport_proto_rawDescGZIP(), []int{1}
}

func (x *Request) GetMeta() *Metadata {
	if x != nil {
		return x.Meta
	}
	return nil
}

func (x *Request) GetPayload() *Stencil {
	if x != nil {
		return x.Payload
	}
	return nil
}

func (x *Request) GetImpl() []*anypb.Any {
	if x != nil {
		return x.Impl
	}
	return nil
}

type Response struct {
	state         protoimpl.MessageState
	sizeCache     protoimpl.SizeCache
	unknownFields protoimpl.UnknownFields

	Meta    *Metadata    `protobuf:"bytes,10,opt,name=meta,proto3" json:"meta,omitempty"`
	Payload *Stencil     `protobuf:"bytes,100,opt,name=payload,proto3" json:"payload,omitempty"`
	Impl    []*anypb.Any `protobuf:"bytes,1000,rep,name=impl,proto3" json:"impl,omitempty"`
}

func (x *Response) Reset() {
	*x = Response{}
	if protoimpl.UnsafeEnabled {
		mi := &file_transport_proto_msgTypes[2]
		ms := protoimpl.X.MessageStateOf(protoimpl.Pointer(x))
		ms.StoreMessageInfo(mi)
	}
}

func (x *Response) String() string {
	return protoimpl.X.MessageStringOf(x)
}

func (*Response) ProtoMessage() {}

func (x *Response) ProtoReflect() protoreflect.Message {
	mi := &file_transport_proto_msgTypes[2]
	if protoimpl.UnsafeEnabled && x != nil {
		ms := protoimpl.X.MessageStateOf(protoimpl.Pointer(x))
		if ms.LoadMessageInfo() == nil {
			ms.StoreMessageInfo(mi)
		}
		return ms
	}
	return mi.MessageOf(x)
}

// Deprecated: Use Response.ProtoReflect.Descriptor instead.
func (*Response) Descriptor() ([]byte, []int) {
	return file_transport_proto_rawDescGZIP(), []int{2}
}

func (x *Response) GetMeta() *Metadata {
	if x != nil {
		return x.Meta
	}
	return nil
}

func (x *Response) GetPayload() *Stencil {
	if x != nil {
		return x.Payload
	}
	return nil
}

func (x *Response) GetImpl() []*anypb.Any {
	if x != nil {
		return x.Impl
	}
	return nil
}

var File_transport_proto protoreflect.FileDescriptor

var file_transport_proto_rawDesc = []byte{
	0x0a, 0x0f, 0x74, 0x72, 0x61, 0x6e, 0x73, 0x70, 0x6f, 0x72, 0x74, 0x2e, 0x70, 0x72, 0x6f, 0x74,
	0x6f, 0x12, 0x11, 0x73, 0x6b, 0x79, 0x6c, 0x6f, 0x75, 0x70, 0x65, 0x2e, 0x73, 0x6b, 0x79, 0x74,
	0x72, 0x61, 0x6e, 0x73, 0x1a, 0x19, 0x67, 0x6f, 0x6f, 0x67, 0x6c, 0x65, 0x2f, 0x70, 0x72, 0x6f,
	0x74, 0x6f, 0x62, 0x75, 0x66, 0x2f, 0x61, 0x6e, 0x79, 0x2e, 0x70, 0x72, 0x6f, 0x74, 0x6f, 0x1a,
	0x0d, 0x73, 0x74, 0x65, 0x6e, 0x63, 0x69, 0x6c, 0x2e, 0x70, 0x72, 0x6f, 0x74, 0x6f, 0x22, 0x3a,
	0x0a, 0x08, 0x4d, 0x65, 0x74, 0x61, 0x64, 0x61, 0x74, 0x61, 0x12, 0x2e, 0x0a, 0x04, 0x64, 0x61,
	0x74, 0x61, 0x18, 0x0a, 0x20, 0x01, 0x28, 0x0b, 0x32, 0x1a, 0x2e, 0x73, 0x6b, 0x79, 0x6c, 0x6f,
	0x75, 0x70, 0x65, 0x2e, 0x73, 0x6b, 0x79, 0x74, 0x72, 0x61, 0x6e, 0x73, 0x2e, 0x53, 0x74, 0x65,
	0x6e, 0x63, 0x69, 0x6c, 0x52, 0x04, 0x64, 0x61, 0x74, 0x61, 0x22, 0x9b, 0x01, 0x0a, 0x07, 0x52,
	0x65, 0x71, 0x75, 0x65, 0x73, 0x74, 0x12, 0x2f, 0x0a, 0x04, 0x6d, 0x65, 0x74, 0x61, 0x18, 0x0a,
	0x20, 0x01, 0x28, 0x0b, 0x32, 0x1b, 0x2e, 0x73, 0x6b, 0x79, 0x6c, 0x6f, 0x75, 0x70, 0x65, 0x2e,
	0x73, 0x6b, 0x79, 0x74, 0x72, 0x61, 0x6e, 0x73, 0x2e, 0x4d, 0x65, 0x74, 0x61, 0x64, 0x61, 0x74,
	0x61, 0x52, 0x04, 0x6d, 0x65, 0x74, 0x61, 0x12, 0x34, 0x0a, 0x07, 0x70, 0x61, 0x79, 0x6c, 0x6f,
	0x61, 0x64, 0x18, 0x64, 0x20, 0x01, 0x28, 0x0b, 0x32, 0x1a, 0x2e, 0x73, 0x6b, 0x79, 0x6c, 0x6f,
	0x75, 0x70, 0x65, 0x2e, 0x73, 0x6b, 0x79, 0x74, 0x72, 0x61, 0x6e, 0x73, 0x2e, 0x53, 0x74, 0x65,
	0x6e, 0x63, 0x69, 0x6c, 0x52, 0x07, 0x70, 0x61, 0x79, 0x6c, 0x6f, 0x61, 0x64, 0x12, 0x29, 0x0a,
	0x04, 0x69, 0x6d, 0x70, 0x6c, 0x18, 0xe8, 0x07, 0x20, 0x03, 0x28, 0x0b, 0x32, 0x14, 0x2e, 0x67,
	0x6f, 0x6f, 0x67, 0x6c, 0x65, 0x2e, 0x70, 0x72, 0x6f, 0x74, 0x6f, 0x62, 0x75, 0x66, 0x2e, 0x41,
	0x6e, 0x79, 0x52, 0x04, 0x69, 0x6d, 0x70, 0x6c, 0x22, 0x9c, 0x01, 0x0a, 0x08, 0x52, 0x65, 0x73,
	0x70, 0x6f, 0x6e, 0x73, 0x65, 0x12, 0x2f, 0x0a, 0x04, 0x6d, 0x65, 0x74, 0x61, 0x18, 0x0a, 0x20,
	0x01, 0x28, 0x0b, 0x32, 0x1b, 0x2e, 0x73, 0x6b, 0x79, 0x6c, 0x6f, 0x75, 0x70, 0x65, 0x2e, 0x73,
	0x6b, 0x79, 0x74, 0x72, 0x61, 0x6e, 0x73, 0x2e, 0x4d, 0x65, 0x74, 0x61, 0x64, 0x61, 0x74, 0x61,
	0x52, 0x04, 0x6d, 0x65, 0x74, 0x61, 0x12, 0x34, 0x0a, 0x07, 0x70, 0x61, 0x79, 0x6c, 0x6f, 0x61,
	0x64, 0x18, 0x64, 0x20, 0x01, 0x28, 0x0b, 0x32, 0x1a, 0x2e, 0x73, 0x6b, 0x79, 0x6c, 0x6f, 0x75,
	0x70, 0x65, 0x2e, 0x73, 0x6b, 0x79, 0x74, 0x72, 0x61, 0x6e, 0x73, 0x2e, 0x53, 0x74, 0x65, 0x6e,
	0x63, 0x69, 0x6c, 0x52, 0x07, 0x70, 0x61, 0x79, 0x6c, 0x6f, 0x61, 0x64, 0x12, 0x29, 0x0a, 0x04,
	0x69, 0x6d, 0x70, 0x6c, 0x18, 0xe8, 0x07, 0x20, 0x03, 0x28, 0x0b, 0x32, 0x14, 0x2e, 0x67, 0x6f,
	0x6f, 0x67, 0x6c, 0x65, 0x2e, 0x70, 0x72, 0x6f, 0x74, 0x6f, 0x62, 0x75, 0x66, 0x2e, 0x41, 0x6e,
	0x79, 0x52, 0x04, 0x69, 0x6d, 0x70, 0x6c, 0x32, 0x52, 0x0a, 0x09, 0x54, 0x72, 0x61, 0x6e, 0x73,
	0x70, 0x6f, 0x72, 0x74, 0x12, 0x45, 0x0a, 0x08, 0x45, 0x78, 0x63, 0x68, 0x61, 0x6e, 0x67, 0x65,
	0x12, 0x1a, 0x2e, 0x73, 0x6b, 0x79, 0x6c, 0x6f, 0x75, 0x70, 0x65, 0x2e, 0x73, 0x6b, 0x79, 0x74,
	0x72, 0x61, 0x6e, 0x73, 0x2e, 0x52, 0x65, 0x71, 0x75, 0x65, 0x73, 0x74, 0x1a, 0x1b, 0x2e, 0x73,
	0x6b, 0x79, 0x6c, 0x6f, 0x75, 0x70, 0x65, 0x2e, 0x73, 0x6b, 0x79, 0x74, 0x72, 0x61, 0x6e, 0x73,
	0x2e, 0x52, 0x65, 0x73, 0x70, 0x6f, 0x6e, 0x73, 0x65, 0x22, 0x00, 0x42, 0x17, 0x5a, 0x15, 0x63,
	0x6f, 0x6d, 0x2e, 0x73, 0x6b, 0x79, 0x6c, 0x6f, 0x75, 0x70, 0x65, 0x2e, 0x73, 0x6b, 0x79, 0x74,
	0x72, 0x61, 0x6e, 0x73, 0x62, 0x06, 0x70, 0x72, 0x6f, 0x74, 0x6f, 0x33,
}

var (
	file_transport_proto_rawDescOnce sync.Once
	file_transport_proto_rawDescData = file_transport_proto_rawDesc
)

func file_transport_proto_rawDescGZIP() []byte {
	file_transport_proto_rawDescOnce.Do(func() {
		file_transport_proto_rawDescData = protoimpl.X.CompressGZIP(file_transport_proto_rawDescData)
	})
	return file_transport_proto_rawDescData
}

var file_transport_proto_msgTypes = make([]protoimpl.MessageInfo, 3)
var file_transport_proto_goTypes = []interface{}{
	(*Metadata)(nil),  // 0: skyloupe.skytrans.Metadata
	(*Request)(nil),   // 1: skyloupe.skytrans.Request
	(*Response)(nil),  // 2: skyloupe.skytrans.Response
	(*Stencil)(nil),   // 3: skyloupe.skytrans.Stencil
	(*anypb.Any)(nil), // 4: google.protobuf.Any
}
var file_transport_proto_depIdxs = []int32{
	3, // 0: skyloupe.skytrans.Metadata.data:type_name -> skyloupe.skytrans.Stencil
	0, // 1: skyloupe.skytrans.Request.meta:type_name -> skyloupe.skytrans.Metadata
	3, // 2: skyloupe.skytrans.Request.payload:type_name -> skyloupe.skytrans.Stencil
	4, // 3: skyloupe.skytrans.Request.impl:type_name -> google.protobuf.Any
	0, // 4: skyloupe.skytrans.Response.meta:type_name -> skyloupe.skytrans.Metadata
	3, // 5: skyloupe.skytrans.Response.payload:type_name -> skyloupe.skytrans.Stencil
	4, // 6: skyloupe.skytrans.Response.impl:type_name -> google.protobuf.Any
	1, // 7: skyloupe.skytrans.Transport.Exchange:input_type -> skyloupe.skytrans.Request
	2, // 8: skyloupe.skytrans.Transport.Exchange:output_type -> skyloupe.skytrans.Response
	8, // [8:9] is the sub-list for method output_type
	7, // [7:8] is the sub-list for method input_type
	7, // [7:7] is the sub-list for extension type_name
	7, // [7:7] is the sub-list for extension extendee
	0, // [0:7] is the sub-list for field type_name
}

func init() { file_transport_proto_init() }
func file_transport_proto_init() {
	if File_transport_proto != nil {
		return
	}
	file_stencil_proto_init()
	if !protoimpl.UnsafeEnabled {
		file_transport_proto_msgTypes[0].Exporter = func(v interface{}, i int) interface{} {
			switch v := v.(*Metadata); i {
			case 0:
				return &v.state
			case 1:
				return &v.sizeCache
			case 2:
				return &v.unknownFields
			default:
				return nil
			}
		}
		file_transport_proto_msgTypes[1].Exporter = func(v interface{}, i int) interface{} {
			switch v := v.(*Request); i {
			case 0:
				return &v.state
			case 1:
				return &v.sizeCache
			case 2:
				return &v.unknownFields
			default:
				return nil
			}
		}
		file_transport_proto_msgTypes[2].Exporter = func(v interface{}, i int) interface{} {
			switch v := v.(*Response); i {
			case 0:
				return &v.state
			case 1:
				return &v.sizeCache
			case 2:
				return &v.unknownFields
			default:
				return nil
			}
		}
	}
	type x struct{}
	out := protoimpl.TypeBuilder{
		File: protoimpl.DescBuilder{
			GoPackagePath: reflect.TypeOf(x{}).PkgPath(),
			RawDescriptor: file_transport_proto_rawDesc,
			NumEnums:      0,
			NumMessages:   3,
			NumExtensions: 0,
			NumServices:   1,
		},
		GoTypes:           file_transport_proto_goTypes,
		DependencyIndexes: file_transport_proto_depIdxs,
		MessageInfos:      file_transport_proto_msgTypes,
	}.Build()
	File_transport_proto = out.File
	file_transport_proto_rawDesc = nil
	file_transport_proto_goTypes = nil
	file_transport_proto_depIdxs = nil
}
