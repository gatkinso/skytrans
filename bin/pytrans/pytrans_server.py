from concurrent import futures
from logging import FileHandler
from timeit import default_timer as timer
from google.protobuf.json_format import MessageToJson
from google.protobuf.any_pb2 import Any

from neo4j import GraphDatabase
from neomodel import config, db

import os
import multiprocessing
import grpc
import transport_pb2
import transport_pb2_grpc
import stencil_pb2
import model
import threading, queue
import time
import json

import contextlib
import socket
from estypes import es_event_type_t, es_proc_suspend_resume_type_t

mutex = threading.Lock()
file_mutex = threading.Lock()

class Neo4jClient:
    def __init__(self):
        self.processed = False

    def build_process_json_str(self, audit_md5_token_, hostname_, es_message_version_, executable_path_, pid_, ppid_, original_ppid_, is_platform_binary_, is_es_client_, filename_):
        json_object = {
            "audit_md5_token" : audit_md5_token_, 
            "hostname" : hostname_,
            "es_message_version": es_message_version_,
            "executable_path" : executable_path_,
            "pid" : pid_, 
            "ppid" : ppid_, 
            "original_ppid" : original_ppid_, 
            "is_platform_binary" : is_platform_binary_, 
            "is_es_client" : is_es_client_,
            "filename" : filename_
        }

        json_str = json.dumps(json_object)
        return json_str

    def build_file_json_str(self, pathname_md5_, hostname_, es_message_version_, target_path_, filename_):
        json_object = {
            "pathname_md5" : pathname_md5_, 
            "hostname" : hostname_, 
            "es_message_version" : es_message_version_, 
            "target_path" : target_path_, 
            "filename" : filename_
        }

        json_str = json.dumps(json_object)
        return json_str

    def build_relationship_json_str(self, action_, global_seq_num_, unix_time_, value_):
        json_object = {
            "action" : action_,
            "global_seq_num": global_seq_num_,
            "unix_time": unix_time_,
            "value_": value_
        }
        json_str = json.dumps(json_object)
        return json_str

    def create_file(self, stencil_, hostname_, es_message_version_, target_path_, md5_tag_base):
        file_mutex.acquire()
        _pathname_md5= [0]*4
        _pathname_md5[0] = stencil_.uint_values[md5_tag_base + ".md5_0"]
        _pathname_md5[1] = stencil_.uint_values[md5_tag_base + ".md5_1"]
        _pathname_md5[2] = stencil_.uint_values[md5_tag_base + ".md5_2"]
        _pathname_md5[3] = stencil_.uint_values[md5_tag_base + ".md5_3"]

        file = model.File.nodes.first_or_none(pathname_md5 = _pathname_md5)
        if file == None:
            file = model.File(pathname_md5 = _pathname_md5, hostname = hostname_,
                                                es_message_version = es_message_version_,
                                                target_path = target_path_).save()
        file_mutex.release()
        return file

    def create_process(self, stencil_, hostname_, es_message_version_, executable_path_, filename_,
                       pid_, ppid_, original_ppid_, is_platform_binary_, is_es_client_, audit_tag_base, md5_tag_base):   
        mutex.acquire()
        _audit_md5_token = [0]*12
        _audit_md5_token[0] = stencil_.uint_values[audit_tag_base + "0"]
        _audit_md5_token[1] = stencil_.uint_values[audit_tag_base + "1"]
        _audit_md5_token[2] = stencil_.uint_values[audit_tag_base + "2"]
        _audit_md5_token[3] = stencil_.uint_values[audit_tag_base + "3"]
        _audit_md5_token[4] = stencil_.uint_values[audit_tag_base + "4"]
        _audit_md5_token[5] = stencil_.uint_values[audit_tag_base + "5"]
        _audit_md5_token[6] = stencil_.uint_values[audit_tag_base + "6"]
        _audit_md5_token[7] = stencil_.uint_values[audit_tag_base + "7"]
        _audit_md5_token[8] =  stencil_.uint_values[md5_tag_base + ".md5_0"]
        _audit_md5_token[9] =  stencil_.uint_values[md5_tag_base + ".md5_1"]
        _audit_md5_token[10] = stencil_.uint_values[md5_tag_base + ".md5_2"]
        _audit_md5_token[11] = stencil_.uint_values[md5_tag_base + ".md5_3"]

        proc = model.Process.nodes.first_or_none(audit_md5_token = _audit_md5_token)
        if proc == None:
            proc = model.Process(audit_md5_token = _audit_md5_token, 
                                    hostname = hostname_,
                                    es_message_version= es_message_version_,
                                    executable_path = stencil_.string_values[executable_path_],
                                    pid = stencil_.int_values[pid_], 
                                    ppid = stencil_.int_values[ppid_], 
                                    original_ppid = stencil_.int_values[original_ppid_], 
                                    is_platform_binary = stencil_.bool_values[is_platform_binary_], 
                                    is_es_client = stencil_.bool_values[is_es_client_],
                                    filename = stencil_.string_values[filename_]).save()
        mutex.release()
        return proc

    def create_file(self, stencil_, hostname_, es_message_version_, target_path_, md5_tag_base):
        file_mutex.acquire()
        _pathname_md5= [0]*4
        _pathname_md5[0] = stencil_.uint_values[md5_tag_base + ".md5_0"]
        _pathname_md5[1] = stencil_.uint_values[md5_tag_base + ".md5_1"]
        _pathname_md5[2] = stencil_.uint_values[md5_tag_base + ".md5_2"]
        _pathname_md5[3] = stencil_.uint_values[md5_tag_base + ".md5_3"]

        file = model.File.nodes.first_or_none(pathname_md5 = _pathname_md5)
        if file == None:
            file = model.File(pathname_md5 = _pathname_md5, hostname = hostname_,
                                                es_message_version = es_message_version_,
                                                target_path = target_path_).save()
        file_mutex.release()
        return file

    def create_kext(self, stencil_, hostname_, es_message_version_, identifier_):
        kext = model.Kext.nodes.first_or_none(hostname = hostname_,
                                                es_message_version = es_message_version_,
                                                identifier = identifier_)
        if kext == None:
            kext = model.Kext(hostname = hostname_,
                                                es_message_version = es_message_version_,
                                                identifier = identifier_).save()
        return kext

    def do_proc_create(self, stencil_, hn, ev_ver, audit_tag_base, md5_tag_base):
        proc = self.create_process(stencil_,
                                    hostname_ = hn,
                                    es_message_version_ = ev_ver,
                                    executable_path_ = "process->executable->path",
                                    filename_ = "process->executable->filename",
                                    pid_ = "process->pid",
                                    ppid_ = "process->ppid",
                                    original_ppid_ = "process->original_ppid",
                                    is_platform_binary_ = "process->is_platform_binary",
                                    is_es_client_ = "process->is_es_client",
                                    audit_tag_base = audit_tag_base,
                                    md5_tag_base = md5_tag_base)
        return proc

    def do_event(self, evt, hn):
        processed = True
        stencil_ = stencil_pb2.Stencil()
        evt.Unpack(stencil_)

        event_type = stencil_.int_values["event_type"]
        es_message_version = stencil_.int_values["es_message->version"]
        gsn = stencil_.int_values["global_seq_num"]

        if event_type == es_event_type_t.ES_EVENT_TYPE_NOTIFY_EXEC:
            proc = self.do_proc_create(stencil_, hn = hn, ev_ver = es_message_version, audit_tag_base = "process->audit_token", md5_tag_base = "process->executable->path")
            exec_proc = self.create_process(stencil_,
                                    hostname_ = hn,
                                    es_message_version_ = es_message_version,
                                    executable_path_ = "exec.target->executable->path",
                                    filename_ = "exec.target->executable->filename",
                                    pid_ = "exec.target->pid",
                                    ppid_ = "exec.target->ppid",
                                    original_ppid_ = "exec.target->original_ppid",
                                    is_platform_binary_ = "exec.target->is_platform_binary",
                                    is_es_client_ = "exec.target->is_es_client",
                                    audit_tag_base = "exec.target->audit_token",
                                    md5_tag_base = "exec.target->executable->path")

            proc.exec.connect(exec_proc, {'pid': stencil_.int_values["exec.target->pid"], 
                        'ppid': stencil_.int_values["exec.target->ppid"], 'global_seq_num': gsn})
            return processed

        if event_type == es_event_type_t.ES_EVENT_TYPE_NOTIFY_FORK:
            proc = self.do_proc_create(stencil_, hn = hn, ev_ver = es_message_version, audit_tag_base = "process->audit_token", md5_tag_base = "process->executable->path")
            corp = self.create_process(stencil_,
                                    hostname_ = hn,
                                    es_message_version_ = es_message_version,
                                    executable_path_ = "fork.child->executable->path", 
                                    filename_ = "fork.child->executable->filename",
                                    pid_ = "fork.child->pid",
                                    ppid_ = "fork.child->ppid",
                                    original_ppid_ = "fork.child->original_ppid",
                                    is_platform_binary_ = "fork.child->is_platform_binary",
                                    is_es_client_ = "fork.child->is_es_client",
                                    audit_tag_base = "fork.child->audit_token",
                                    md5_tag_base = "fork.child->executable->path")

            proc.fork.connect(corp, {'fork_pid': stencil_.int_values["fork.child->pid"], 'global_seq_num': gsn})
            return processed

        if event_type == es_event_type_t.ES_EVENT_TYPE_NOTIFY_SIGNAL:
            proc = self.do_proc_create(stencil_, hn = hn, ev_ver = es_message_version, audit_tag_base = "process->audit_token", md5_tag_base = "process->executable->path")
            sig_proc = self.create_process(stencil_,
                                    hostname_ = hn,
                                    es_message_version_ = es_message_version,
                                    executable_path_ = "signal.target->executable->path",
                                    filename_ = "signal.target->executable->filename",
                                    pid_ = "signal.target->pid",
                                    ppid_ = "signal.target->ppid",
                                    original_ppid_ = "signal.target->original_ppid",
                                    is_platform_binary_ = "signal.target->is_platform_binary",
                                    is_es_client_ = "signal.target->is_es_client",
                                    audit_tag_base = "signal.target->audit_token",
                                    md5_tag_base = "signal.target->executable->path")

            sig = stencil_.int_values["signal.sig"]
            proc.signal.connect(sig_proc, {'signal': sig, 'global_seq_num': gsn})
            return processed

        if event_type == es_event_type_t.ES_EVENT_TYPE_NOTIFY_GET_TASK:
            proc = self.do_proc_create(stencil_, hn = hn, ev_ver = es_message_version, audit_tag_base = "process->audit_token", md5_tag_base = "process->executable->path")
            tgt_proc = self.create_process(stencil_,
                                    hostname_ = hn,
                                    es_message_version_ = es_message_version,
                                    executable_path_ = "get_task.target->executable->path",
                                    filename_ = "get_task.target->executable->filename",
                                    pid_ = "get_task.target->pid",
                                    ppid_ = "get_task.target->ppid",
                                    original_ppid_ = "get_task.target->original_ppid",
                                    is_platform_binary_ = "get_task.target->is_platform_binary",
                                    is_es_client_ = "get_task.target->is_es_client",
                                    audit_tag_base = "get_task.target->audit_token",
                                    md5_tag_base = "get_task.target->executable->path")

            tgt_pid = stencil_.int_values["get_task.target->pid"]
            proc.gettask.connect(tgt_proc, {'tgt_pid': tgt_pid, 'global_seq_num': gsn})
            return processed

        if event_type == es_event_type_t.ES_EVENT_TYPE_NOTIFY_PROC_SUSPEND_RESUME:
            proc = self.do_proc_create(stencil_, hn = hn, ev_ver = es_message_version, audit_tag_base = "process->audit_token", md5_tag_base = "process->executable->path")
            sr_pid = stencil_.int_values["proc_suspend_resume.target->pid"]

            child_proc = self.create_process(stencil_,
                                    hostname_ = hn,
                                    es_message_version_ = es_message_version,
                                    executable_path_ = "proc_suspend_resume.target->executable->path",
                                    filename_ = "proc_suspend_resume.target->executable->filename",
                                    pid_ = "proc_suspend_resume.target->pid",
                                    ppid_ = "proc_suspend_resume.target->ppid",
                                    original_ppid_ = "proc_suspend_resume.target->original_ppid",
                                    is_platform_binary_ = "proc_suspend_resume.target->is_platform_binary",
                                    is_es_client_ = "proc_suspend_resume.target->is_es_client",
                                    audit_tag_base = "proc_suspend_resume.target->audit_token",
                                    md5_tag_base = "proc_suspend_resume.target->executable->path")
 
            if stencil_.int_values["proc_suspend_resume.type"] == es_proc_suspend_resume_type_t.ES_PROC_SUSPEND_RESUME_TYPE_RESUME:
                proc.resume.connect(child_proc, {'sr_pid': sr_pid, 'global_seq_num': gsn})
            elif stencil_.int_values["proc_suspend_resume.type"] == es_proc_suspend_resume_type_t.ES_PROC_SUSPEND_RESUME_TYPE_SUSPEND:
                proc.suspend.connect(child_proc, {'sr_pid': sr_pid, 'global_seq_num': gsn})
            elif stencil_.int_values["proc_suspend_resume.type"] == es_proc_suspend_resume_type_t.ES_PROC_SUSPEND_RESUME_TYPE_SHUTDOWN_SOCKETS:
                proc.socks.connect(child_proc, {'sr_pid': sr_pid, 'global_seq_num': gsn})
            return processed

        if event_type == es_event_type_t.ES_EVENT_TYPE_NOTIFY_CREATE:
            proc = self.do_proc_create(stencil_, hn = hn, ev_ver = es_message_version, audit_tag_base = "process->audit_token", md5_tag_base = "process->executable->path")
            if "create.destination.existing_file->path" in stencil_.string_values:
                tgt = stencil_.string_values["create.destination.existing_file->path"]
            else:
                tgt = stencil_.string_values["create.destination.new_path.dir->path"] + \
                "\\" + stencil_.string_values["create.destination.new_path.filename"]

            unix_time = int(stencil_.string_values["Unix Time"])

            tgt_file = self.create_file(stencil_,
                                        hn,
                                        es_message_version_ = es_message_version,
                                        target_path_ = tgt,
                                        md5_tag_base = "create.destination.new_path.dir->path")

            rel = tgt_file.creator.relationship(proc)

            if rel == None:
                tgt_file.creator.connect(proc, {'op': 'CREATED', 'unix_time' : unix_time, 'global_seq_num': gsn })
            else:
                rel.unix_time = unix_time
            return processed

        if event_type == es_event_type_t.ES_EVENT_TYPE_NOTIFY_CLOSE:
            proc = self.do_proc_create(stencil_, hn = hn, ev_ver = es_message_version, audit_tag_base = "process->audit_token", md5_tag_base = "process->executable->path")
            unix_time = int(stencil_.string_values["Unix Time"])

            tgt_file = self.create_file(stencil_,
                                        hn,
                                        es_message_version_ = es_message_version,
                                        target_path_ = stencil_.string_values["close.target->path"],
                                        md5_tag_base = "close.target->path")

            rel = tgt_file.closer.relationship(proc)

            if rel == None:
                tgt_file.closer.connect(proc, {'op': 'CLOSED', 'unix_time' : unix_time, 'global_seq_num': gsn })
            else:
                rel.unix_time = unix_time
            return processed

        if event_type == es_event_type_t.ES_EVENT_TYPE_NOTIFY_OPEN:
            proc = self.do_proc_create(stencil_, hn = hn, ev_ver = es_message_version, audit_tag_base = "process->audit_token", md5_tag_base = "process->executable->path")
            unix_time = int(stencil_.string_values["Unix Time"])

            tgt_file = self.create_file(stencil_,
                                        hn,
                                        es_message_version_ = es_message_version,
                                        target_path_ = stencil_.string_values["open.file->path"],
                                        md5_tag_base = "open.file->path")

            rel = tgt_file.opener.relationship(proc)

            if rel == None:
                tgt_file.opener.connect(proc, {'op': 'OPENED', 'unix_time' : unix_time, 'global_seq_num': gsn })
            else:
                rel.unix_time = unix_time
            return processed

        if event_type == es_event_type_t.ES_EVENT_TYPE_NOTIFY_WRITE:
            proc = self.do_proc_create(stencil_, hn = hn, ev_ver = es_message_version, audit_tag_base = "process->audit_token", md5_tag_base = "process->executable->path")
            unix_time = int(stencil_.string_values["Unix Time"])

            tgt_file = self.create_file(stencil_,
                                        hn,
                                        es_message_version_ = es_message_version,
                                        target_path_ = stencil_.string_values["write.file->path"],
                                        md5_tag_base = "write.file->path")

            rel = tgt_file.opener.relationship(proc)

            if rel == None:
                tgt_file.opener.connect(proc, {'op': 'WROTE', 'unix_time' : unix_time, 'global_seq_num': gsn })
            else:
                rel.unix_time = unix_time
            return processed

        if event_type == es_event_type_t.ES_EVENT_TYPE_NOTIFY_MOUNT:
            proc = self.do_proc_create(stencil_, hn = hn, ev_ver = es_message_version, audit_tag_base = "process->audit_token", md5_tag_base = "process->executable->path")

            tgt_file = self.create_file(stencil_,
                                        hn,
                                        es_message_version_ = es_message_version,
                                        target_path_ = stencil_.string_values["mount.statfs->f_mntonname"],
                                        md5_tag_base = "mount.statfs->f_mntonname")

            rel = tgt_file.mount.relationship(proc)

            frm = stencil_.string_values["mount.statfs->f_mntfromname"]
            if rel == None:

                tgt_file.mount.connect(proc, {'global_seq_num': gsn, 'frm' : frm })
            else:
                rel.global_seq_num = gsn

            return processed

        if event_type == es_event_type_t.ES_EVENT_TYPE_NOTIFY_UNMOUNT:
            proc = self.do_proc_create(stencil_, hn = hn, ev_ver = es_message_version, audit_tag_base = "process->audit_token", md5_tag_base = "process->executable->path")
            # = int(stencil_.string_values["Unix Time"])

            tgt_file = self.create_file(stencil_,
                                        hn,
                                        es_message_version_ = es_message_version,
                                        target_path_ = stencil_.string_values["unmount.statfs->f_mntonname"],
                                        md5_tag_base = "unmount.statfs->f_mntonname")

            rel = tgt_file.unmount.relationship(proc)

            frm = stencil_.string_values["unmount.statfs->f_mntfromname"]
            if rel == None:
                tgt_file.unmount.connect(proc, {'global_seq_num': gsn, 'frm' : frm })
            else:
                rel.global_seq_num = gsn

            return processed

        if event_type == es_event_type_t.ES_EVENT_TYPE_NOTIFY_KEXTLOAD:
            proc = self.do_proc_create(stencil_, hn = hn, ev_ver = es_message_version, audit_tag_base = "process->audit_token", md5_tag_base = "process->executable->path")
            unix_time = int(stencil_.string_values["Unix Time"])

            tgt_kext = self.create_kext(stencil_,
                                        hn,
                                        es_message_version_ = es_message_version,
                                        identifier_ = stencil_.string_values["kextload.identifier.data"])

            tgt_kext.load.connect(proc, { 'unix_time' : unix_time, 'global_seq_num': gsn })
            return processed

        if event_type == es_event_type_t.ES_EVENT_TYPE_NOTIFY_KEXTUNLOAD:
            proc = self.do_proc_create(stencil_, hn = hn, ev_ver = es_message_version, audit_tag_base = "process->audit_token", md5_tag_base = "process->executable->path")
            unix_time = int(stencil_.string_values["Unix Time"])

            tgt_kext = self.create_kext(stencil_,
                                        hn,
                                        es_message_version_ = es_message_version,
                                        identifier_ = stencil_.string_values["kextload.identifier.data"])

            tgt_kext.unload.connect(proc, { 'unix_time' : unix_time, 'global_seq_num': gsn })
            return processed

        if event_type == es_event_type_t.ES_EVENT_TYPE_NOTIFY_EXIT:
            proc = self.do_proc_create(stencil_, hn = hn, ev_ver = es_message_version, audit_tag_base = "process->audit_token", md5_tag_base = "process->executable->path")
            unix_time = int(stencil_.string_values["Unix Time"])

            exit_ = model.Exit(hostname = hn,
                                        es_message_version = es_message_version,
                                        unix_time = unix_time,
                                        pid = proc.pid).save()

            stat_ = stencil_.int_values["exit.stat"]
            exit_.proc.connect(proc, { 'global_seq_num': gsn, 'stat': stat_ })
            return processed

        if event_type == es_event_type_t.ES_EVENT_TYPE_NOTIFY_MMAP:
            proc = self.do_proc_create(stencil_, hn = hn, ev_ver = es_message_version, audit_tag_base = "process->audit_token", md5_tag_base = "process->executable->path")
            unix_time = int(stencil_.string_values["Unix Time"])

            tgt_file = self.create_file(stencil_,
                                        hn,
                                        es_message_version_ = es_message_version,
                                        target_path_ = stencil_.string_values["mmap.source->path"],
                                        md5_tag_base = "mmap.source->path")

            rel = tgt_file.mmap.relationship(proc)

            if rel == None:
                tgt_file.mmap.connect(proc, {'op': 'MMAP', 'unix_time' : unix_time, 'global_seq_num': gsn })
            else:
                rel.unix_time = unix_time
            return processed

        processed = False
        return processed

    def process(self, request):
        hn = request.meta.data.string_values["Hostname"]
        reqid = request.meta.data.int_values["Req id"]

        count = 0

        start = timer()

        for evt in request.impl:
            if self.do_event(evt, hn):
                count = count + 1

        end = timer()

        bs = len(request.impl)
        elapsed = end - start
        rate = 0
        if elapsed > 0:
            rate = count / elapsed

        print("Host: " + hn + " Request ID: " + str(reqid) + " done " + \
            " Batch Size: " + str(bs) + \
            " in " + "{:.3f}".format(elapsed) + " seconds" + \
            " Processed: " + str(count)
            + \
            " Rate: " + "{:.3f}".format(rate) + " per second")

class TransportServicer(transport_pb2_grpc.TransportServicer):
    """Provides methods that implement functionality of route guide server."""
    def __init__(self, txid):
        self.notify_exec = True
        self.notify_create = True
        self.notify_close = True
        self.notify_open = True
        self.notify_write = True
        self.notify_signal = True
        self.notify_get_task = False
        self.notify_fork = True
        self.notify_mount = True 
        self.notify_unmount = True
        self.notify_suspend_resume = False
        self.notify_kextload = True
        self.notify_kextunload = True
        self.notify_exit = True
        self.notify_mmap = True
        self.txid = txid
        #self.n4jclient = Neo4jClient()
        self.requestq = queue.Queue()
        self.running = True
        self.sleepCount = 0

        threading.setprofile(self.trace_dothread())

        self.t1 = threading.Thread(target = self.dothread, args =())
        self.t1.start()

        self.t2 = threading.Thread(target = self.dothread, args =())
        self.t2.start()

        self.t3 = threading.Thread(target = self.dothread, args =())
        self.t3.start()

        self.t4 = threading.Thread(target = self.dothread, args =())
        self.t4.start()

    def trace_dothread(self):
        return
        #print("Current thread's profile")
        #print("Name:", str(threading.current_thread().getName()))
        #print("Thread id:", threading.get_ident())

    def dothread(self):
        #threading.setprofile(self.trace_dothread())
        n4jclient = Neo4jClient()
        while self.running:
            r = self.requestq.get()
            #jstr = MessageToJson(r)
            #print(jstr)

            n4jclient.process(r)

    def DoPathMutes(self, res, stencil, type, path):
            stencil.string_values[type] = path
            any_message = Any()
            any_message.Pack(stencil)
            res.impl.append(any_message)

    def DoSubs(self, res, stencil, flag, value):
        if flag == True:
            stencil.int_values["subscribe"] = value
            any_message = Any()
            any_message.Pack(stencil)
            res.impl.append(any_message)
        else:
            stencil.int_values["unsubscribe"] = value
            any_message = Any()
            any_message.Pack(stencil)
            res.impl.append(any_message)

    def Exchange(self, request, context):

        self.requestq.put(request)

        #bytes = request.ByteSize()
        #print("Queue size: " +str(self.requestq.qsize()))

        res = transport_pb2.Response()

        stencil_ = stencil_pb2.Stencil()
        self.DoSubs(res, stencil_, self.notify_exec, es_event_type_t.ES_EVENT_TYPE_NOTIFY_EXEC)
        self.DoSubs(res, stencil_, self.notify_create, es_event_type_t.ES_EVENT_TYPE_NOTIFY_CREATE)
        self.DoSubs(res, stencil_, self.notify_close, es_event_type_t.ES_EVENT_TYPE_NOTIFY_CLOSE)
        self.DoSubs(res, stencil_, self.notify_open, es_event_type_t.ES_EVENT_TYPE_NOTIFY_OPEN)
        self.DoSubs(res, stencil_, self.notify_signal, es_event_type_t.ES_EVENT_TYPE_NOTIFY_SIGNAL)
        self.DoSubs(res, stencil_, self.notify_get_task, es_event_type_t.ES_EVENT_TYPE_NOTIFY_GET_TASK)
        self.DoSubs(res, stencil_, self.notify_fork, es_event_type_t.ES_EVENT_TYPE_NOTIFY_FORK)
        self.DoSubs(res, stencil_, self.notify_mount, es_event_type_t.ES_EVENT_TYPE_NOTIFY_MOUNT)
        self.DoSubs(res, stencil_, self.notify_unmount, es_event_type_t.ES_EVENT_TYPE_NOTIFY_UNMOUNT)
        self.DoSubs(res, stencil_, self.notify_suspend_resume, es_event_type_t.ES_EVENT_TYPE_NOTIFY_PROC_SUSPEND_RESUME)
        self.DoSubs(res, stencil_, self.notify_kextload, es_event_type_t.ES_EVENT_TYPE_NOTIFY_KEXTLOAD)
        self.DoSubs(res, stencil_, self.notify_kextunload, es_event_type_t.ES_EVENT_TYPE_NOTIFY_KEXTUNLOAD)
        self.DoSubs(res, stencil_, self.notify_exit, es_event_type_t.ES_EVENT_TYPE_NOTIFY_EXIT)
        self.DoSubs(res, stencil_, self.notify_mmap, es_event_type_t.ES_EVENT_TYPE_NOTIFY_MMAP)
        self.DoSubs(res, stencil_, self.notify_write, es_event_type_t.ES_EVENT_TYPE_NOTIFY_WRITE)

        mutee = "/System/Library/Frameworks/CoreServices.framework/Versions/A/Frameworks/Metadata.framework/Versions/A/Support/"
        self.DoPathMutes(res, stencil_, "mute prefix", mutee)

        self.sleepCount += 1
        if self.sleepCount > 10:
            self.sleepCount = 0
            time.sleep(0.0001)

        return res

@contextlib.contextmanager
def _reserve_port():
    #Find and reserve a port for all subprocesses to use.
    sock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
    if sock.getsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT) == 0:
        raise RuntimeError("Failed to set SO_REUSEPORT.")
    sock.bind(('', 1967))
    try:
        yield sock.getsockname()[1]
    finally:
        sock.close()

def run_server(bind_address, txid):
    url = os.environ["NEO4J_BOLT_URL"]
    config.DATABASE_URL = url

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=multiprocessing.cpu_count()), maximum_concurrent_rpcs=10)
    transport_pb2_grpc.add_TransportServicer_to_server(
        TransportServicer(txid), server)
    server.add_insecure_port(bind_address)
    server.start()
    server.wait_for_termination()

def main_new_multi():
    with _reserve_port() as port:
        bind_address = '[::]:{}'.format(port)
        #print()
        #_LOGGER.info("Binding to '%s'", bind_address)
        #sys.stdout.flush()
        workers = []
        for id in range(multiprocessing.cpu_count()):
            # NOTE: It is imperative that the worker subprocesses be forked before
            # any gRPC servers start up. See
            # https://github.com/grpc/grpc/issues/16001 for more details.
            worker = multiprocessing.Process(target=run_server, args=(bind_address,id))
            worker.start()
            workers.append(worker)
        for worker in workers:
            worker.join()

def main_org():
    url = os.environ["NEO4J_BOLT_URL"]
    config.DATABASE_URL = url

    num_workers = 4 #* multiprocessing.cpu_count()
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=num_workers))
    transport_pb2_grpc.add_TransportServicer_to_server(
        TransportServicer(0), server)
    server.add_insecure_port('[::]:1967')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    #main_new_multi()
    main_org()
