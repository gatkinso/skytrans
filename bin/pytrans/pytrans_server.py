from concurrent import futures
from logging import FileHandler
from timeit import default_timer as timer
from google.protobuf.json_format import MessageToJson

from neo4j import GraphDatabase
from neomodel import config

import os
import multiprocessing
import grpc
import transport_pb2
import transport_pb2_grpc
import stencil_pb2
import model

import contextlib
import socket
from estypes import es_event_type_t, es_proc_suspend_resume_type_t

class Neo4jClient:
    def __init__(self):
        self.notify_exec = True
        self.notify_create = True
        self.notify_close = True
        self.notify_open = True
        self.notify_signal = True
        self.notify_get_task = True
        self.notify_fork = True
        self.notify_mount = True
        self.notify_unmount = True
        self.notify_suspend_resume = True
        self.notify_kextload = True
        self.notify_kext_unload = True

        self.processed = False

    def create_process(self, stencil_, hostname_, es_message_version_, executable_path_,
                       pid_, ppid_, original_ppid_, is_platform_binary_, is_es_client_):    
        _1 = hostname_
        _2 = es_message_version_
        _3 = stencil_.string_values[executable_path_]
        _4 = stencil_.int_values[pid_]
        _5 = stencil_.int_values[ppid_]
        _6 = stencil_.int_values[original_ppid_]
        _7 = stencil_.bool_values[is_platform_binary_]
        _8 = stencil_.bool_values[is_es_client_]

        proc = model.Process.nodes.first_or_none(hostname = _1, es_message_version= _2, executable_path = _3,
            pid = _4, ppid = _5, original_ppid = _6, is_platform_binary = _7, is_es_client = _8)
        if proc == None:
            proc = model.Process(hostname = _1, es_message_version= _2, executable_path = _3,
                pid = _4, ppid = _5, original_ppid = _6, is_platform_binary = _7, is_es_client = _8)
        return proc

    def create_file(self, stencil_, hostname_, es_message_version_, target_path_):
        file = model.File.nodes.first_or_none(hostname = hostname_,
                                                es_message_version = es_message_version_,
                                                target_path = target_path_)
        if file == None:
            file = model.File(hostname = hostname_,
                                                es_message_version = es_message_version_,
                                                target_path = target_path_)
        return file

    def do_proc_create(self, stencil_, hn, ev_ver):
        proc = self.create_process(stencil_,
                                    hostname_ = hn,
                                    es_message_version_ = ev_ver,
                                    executable_path_ = "process->executable->path", 
                                    pid_ = "process->pid",
                                    ppid_ = "process->ppid",
                                    original_ppid_ = "process->original_ppid",
                                    is_platform_binary_ = "process->is_platform_binary",
                                    is_es_client_ = "process->is_es_client").save()
        return proc

    def do_event(self, evt, hn):
        processed = True
        stencil_ = stencil_pb2.Stencil()
        evt.Unpack(stencil_)

        event_type = stencil_.int_values["event_type"]
        es_message_version = stencil_.int_values["es_message->version"]

        if self.notify_exec and event_type == es_event_type_t.ES_EVENT_TYPE_NOTIFY_EXEC:
            proc = self.do_proc_create(stencil_, hn = hn, ev_ver = es_message_version)
            exec_proc = self.create_process(stencil_,
                                    hostname_ = hn,
                                    es_message_version_ = es_message_version,
                                    executable_path_ = "exec.target->executable->path", 
                                    pid_ = "exec.target->pid",
                                    ppid_ = "exec.target->ppid",
                                    original_ppid_ = "exec.target->original_ppid",
                                    is_platform_binary_ = "exec.target->is_platform_binary",
                                    is_es_client_ = "exec.target->is_es_client").save()

            proc.exec.connect(exec_proc, {'pid': stencil_.int_values["exec.target->pid"], 'ppid': stencil_.int_values["exec.target->ppid"]})
            return processed

        if self.notify_create and event_type == es_event_type_t.ES_EVENT_TYPE_NOTIFY_CREATE:
            proc = self.do_proc_create(stencil_, hn = hn, ev_ver = es_message_version)
            if "create.destination.existing_file->path" in stencil_.string_values:
                tgt = stencil_.string_values["create.destination.existing_file->path"]
            else:
                tgt = stencil_.string_values["create.destination.new_path.dir->path"] + \
                "\\" + stencil_.string_values["create.destination.new_path.filename"]

            unix_time = int(stencil_.string_values["Unix Time"])

            tgt_file = self.create_file(stencil_,
                                        hn,
                                        es_message_version_ = es_message_version,
                                        target_path_ = tgt).save()

            rel = tgt_file.creator.relationship(proc)

            if rel == None:
                tgt_file.creator.connect(proc, {'op': 'CREATED', 'unix_time' : unix_time })
            else:
                rel.unix_time = unix_time
            return processed

        if self.notify_close and event_type == es_event_type_t.ES_EVENT_TYPE_NOTIFY_CLOSE:
            unix_time = int(stencil_.string_values["Unix Time"])

            tgt_file = self.create_file(stencil_,
                                        hn,
                                        es_message_version_ = es_message_version,
                                        target_path_ = "close.target->path").save()

            rel = tgt_file.closer.relationship(proc)

            if rel == None:
                tgt_file.closer.connect(proc, {'op': 'CLOSED', 'unix_time' : unix_time })
            else:
                rel.unix_time = unix_time
            return processed

        if self.notify_open and event_type == es_event_type_t.ES_EVENT_TYPE_NOTIFY_OPEN:
            unix_time = int(stencil_.string_values["Unix Time"])

            tgt_file = self.create_file(stencil_,
                                        hn,
                                        es_message_version_ = es_message_version,
                                        target_path_ = "open.file->path").save()

            rel = tgt_file.opener.relationship(proc)

            if rel == None:
                tgt_file.opener.connect(proc, {'op': 'OPENED', 'unix_time' : unix_time })
            else:
                rel.unix_time = unix_time
            return

        if self.notify_signal and event_type == es_event_type_t.ES_EVENT_TYPE_NOTIFY_SIGNAL:
            proc = self.do_proc_create(stencil_, hn = hn, ev_ver = es_message_version)
            sig_proc = self.create_process(stencil_,
                                    hostname_ = hn,
                                    es_message_version_ = es_message_version,
                                    executable_path_ = "signal.target->executable->path", 
                                    pid_ = "signal.target->pid",
                                    ppid_ = "signal.target->ppid",
                                    original_ppid_ = "signal.target->original_ppid",
                                    is_platform_binary_ = "signal.target->is_platform_binary",
                                    is_es_client_ = "signal.target->is_es_client").save()

            sig = stencil_.int_values["signal.sig"]
            proc.signal.connect(sig_proc, {'signal': sig})
            return processed

        if self.notify_get_task and event_type == es_event_type_t.ES_EVENT_TYPE_NOTIFY_GET_TASK:
            proc = self.do_proc_create(stencil_, hn = hn, ev_ver = es_message_version)
            tgt_proc = self.create_process(stencil_,
                                    hostname_ = hn,
                                    es_message_version_ = es_message_version,
                                    executable_path_ = "get_task.target->executable->path", 
                                    pid_ = "get_task.target->pid",
                                    ppid_ = "get_task.target->ppid",
                                    original_ppid_ = "get_task.target->original_ppid",
                                    is_platform_binary_ = "get_task.target->is_platform_binary",
                                    is_es_client_ = "get_task.target->is_es_client").save()

            tgt_pid = stencil_.int_values["get_task.target->pid"]
            proc.gettask.connect(tgt_proc, {'tgt_pid': tgt_pid})
            return processed

        if self.notify_fork and event_type == es_event_type_t.ES_EVENT_TYPE_NOTIFY_FORK:
            proc = self.do_proc_create(stencil_, hn = hn, ev_ver = es_message_version)
            child_proc = self.create_process(stencil_,
                                    hostname_ = hn,
                                    es_message_version_ = es_message_version,
                                    executable_path_ = "fork.child->executable->path", 
                                    pid_ = "fork.child->pid",
                                    ppid_ = "fork.child->ppid",
                                    original_ppid_ = "fork.child->original_ppid",
                                    is_platform_binary_ = "fork.child->is_platform_binary",
                                    is_es_client_ = "fork.child->is_es_client").save()

            proc.fork.connect(child_proc, {'fork_pid': stencil_.int_values["fork.child->pid"]})
            return processed

        if self.notify_mount and event_type == es_event_type_t.ES_EVENT_TYPE_NOTIFY_MOUNT:
            proc = self.do_proc_create(stencil_, hn = hn, ev_ver = es_message_version)
            m_from = stencil_.string_values["mount.statfs->f_mntfromname"]
            m_to = stencil_.string_values["mount.statfs->f_mntonname"]

            mnt_from = model.FileMount.nodes.first_or_none(hostname = hn, dir = m_from)
            if mnt_from == None:
                mnt_from = model.FileMount(hostname = hn, dir = m_from).save()

            mnt_to = model.FileMount.nodes.first_or_none(hostname = hn, dir = m_to)
            if mnt_to == None:
                mnt_to = model.FileMount(hostname = hn, dir = m_to).save()

            mnt_to.mounted.connect(mnt_from)
            mnt_from.actor.connect(proc)
            return processed

        if self.notify_unmount and event_type == es_event_type_t.ES_EVENT_TYPE_NOTIFY_UNMOUNT:
            proc = self.do_proc_create(stencil_, hn = hn, ev_ver = es_message_version)
            m_from = stencil_.string_values["unmount.statfs->f_mntfromname"]
            m_to = stencil_.string_values["unmount.statfs->f_mntonname"]

            mnt_from = model.FileMount.nodes.first_or_none(hostname = hn, dir = m_from)
            if mnt_from == None:
                mnt_from = model.FileMount(hostname = hn, dir = m_from).save()

            mnt_to = model.FileUnmount.nodes.first_or_none(hostname = hn, dir = m_to)
            if mnt_to == None:
                mnt_to = model.FileUnmount(hostname = hn, dir = m_to).save()

            mnt_to.mounted.connect(mnt_from)
            mnt_from.actor.connect(proc)
            return processed

        if self.notify_suspend_resume and event_type == es_event_type_t.ES_EVENT_TYPE_NOTIFY_PROC_SUSPEND_RESUME:
            proc = self.do_proc_create(stencil_, hn = hn, ev_ver = es_message_version)
            sr_pid = stencil_.int_values["proc_suspend_resume.target->pid"]

            child_proc = self.create_process(stencil_,
                                    hostname_ = hn,
                                    es_message_version_ = es_message_version,
                                    executable_path_ = "proc_suspend_resume.target->executable->path", 
                                    pid_ = "proc_suspend_resume.target->pid",
                                    ppid_ = "proc_suspend_resume.target->ppid",
                                    original_ppid_ = "proc_suspend_resume.target->original_ppid",
                                    is_platform_binary_ = "proc_suspend_resume.target->is_platform_binary",
                                    is_es_client_ = "proc_suspend_resume.target->is_es_client").save()
 
            if stencil_.int_values["proc_suspend_resume.type"] == es_proc_suspend_resume_type_t.ES_PROC_SUSPEND_RESUME_TYPE_RESUME:
                proc.resume.connect(child_proc, {'sr_pid': sr_pid})
            elif stencil_.int_values["proc_suspend_resume.type"] == es_proc_suspend_resume_type_t.ES_PROC_SUSPEND_RESUME_TYPE_SUSPEND:
                proc.suspend.connect(child_proc, {'sr_pid': sr_pid})
            elif stencil_.int_values["proc_suspend_resume.type"] == es_proc_suspend_resume_type_t.ES_PROC_SUSPEND_RESUME_TYPE_SHUTDOWN_SOCKETS:
                proc.socks.connect(child_proc, {'sr_pid': sr_pid})
            return processed

        processed = False
        return processed

class TransportServicer(transport_pb2_grpc.TransportServicer):
    """Provides methods that implement functionality of route guide server."""
    def __init__(self):
        return

    def Exchange(self, request, context):
        hn = request.meta.data.string_values["Hostname"]

        count = 0
        n4jclient = Neo4jClient()

        start = timer()

        for evt in request.impl:
            if n4jclient.do_event(evt, hn):
                count = count + 1

        end = timer()

        bs = len(request.impl)
        elapsed = end - start
        if elapsed > 0:
            rate = count / elapsed
 
        print("Host: " + hn + " Request ID: " + str(request.meta.data.int_values["Req id"]) + \
            " Batch Size: " + str(bs) + " in " + "{:.3f}".format(elapsed) + " seconds" + \
            " Processed: " + str(count) + \
            " Rate: " + "{:.3f}".format(rate) + " per second")

        res = transport_pb2.Response()

        res.meta.data.string_values["Hostname"] = hn
        res.meta.data.int_values["Req id"] = request.meta.data.int_values["Req id"]
        res.meta.data.int_values["Event Count"] = bs

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

def run_server(bind_address):
    url = os.environ["NEO4J_BOLT_URL"]
    config.DATABASE_URL = url

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=multiprocessing.cpu_count()), maximum_concurrent_rpcs=10)
    transport_pb2_grpc.add_TransportServicer_to_server(
        TransportServicer(), server)
    #server.add_insecure_port('[::]:1967')
    server.add_insecure_port(bind_address)
    server.start()
    server.wait_for_termination()

def main_new_multi():
    with _reserve_port() as port:
        bind_address = '[::]:{}'.format(port)
        print()
        #_LOGGER.info("Binding to '%s'", bind_address)
        #sys.stdout.flush()
        workers = []
        for _ in range(multiprocessing.cpu_count()):
            # NOTE: It is imperative that the worker subprocesses be forked before
            # any gRPC servers start up. See
            # https://github.com/grpc/grpc/issues/16001 for more details.
            worker = multiprocessing.Process(target=run_server, args=(bind_address,))
            worker.start()
            workers.append(worker)
        for worker in workers:
            worker.join()

def main_org():
    url = os.environ["NEO4J_BOLT_URL"]
    config.DATABASE_URL = url

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=15))
    transport_pb2_grpc.add_TransportServicer_to_server(
        TransportServicer(), server)
    server.add_insecure_port('[::]:1967')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    main_new_multi()
