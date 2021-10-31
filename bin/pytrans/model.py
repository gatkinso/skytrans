
from neomodel import StructuredNode, StructuredRel, StringProperty, IntegerProperty, RelationshipTo, RelationshipFrom, config
from neomodel.properties import BooleanProperty

class Signal(StructuredRel):
    signal = IntegerProperty(unique_index=False, required=True)
    global_seq_num = IntegerProperty(unique_index=False, required=False)

class Fork(StructuredRel):
    fork_pid = IntegerProperty(unique_index=False, required=False)
    global_seq_num = IntegerProperty(unique_index=False, required=False)

class Exec(StructuredRel):
    pid = IntegerProperty(unique_index=False)
    ppid = IntegerProperty(unique_index=False)
    global_seq_num = IntegerProperty(unique_index=False, required=False)

class SuspendResume(StructuredRel):
    pid = IntegerProperty(unique_index=False)
    global_seq_num = IntegerProperty(unique_index=False, required=False)

class GetTask(StructuredRel):
    tgt_pid = IntegerProperty(unique_index=False)
    global_seq_num = IntegerProperty(unique_index=False, required=False)

class Mount(StructuredRel):
    global_seq_num = IntegerProperty(unique_index=False, required=False)
    frm = StringProperty(unique_index=False, required=True)

class Unmount(StructuredRel):
    global_seq_num = IntegerProperty(unique_index=False, required=False)
    frm = StringProperty(unique_index=False, required=True)

class Exited(StructuredRel):
    global_seq_num = IntegerProperty(unique_index=False, required=False)
    stat = IntegerProperty(unique_index=False, required=False)

class Exit(StructuredNode):
    hostname = StringProperty(unique_index=False, required=True)
    es_message_version = IntegerProperty(unique_index=False)
    unix_time = IntegerProperty(unique_index=False, required=True)
    pid = IntegerProperty(unique_index=False)
    proc = RelationshipFrom("Process", "EXITED", model=Exited)

class Process(StructuredNode):
    hostname = StringProperty(unique_index=False, required=True)
    es_message_version = IntegerProperty(unique_index=False)
    executable_path = StringProperty(unique_index=False, required=True)
    pid = IntegerProperty(unique_index=False)
    ppid = IntegerProperty(unique_index=False)
    original_ppid = IntegerProperty(unique_index=False)
    is_platform_binary = BooleanProperty(unique_index=False)
    is_es_client = BooleanProperty(unique_index=False)

    signal = RelationshipTo("Process", "SIGNAL", model=Signal)
    exec = RelationshipTo("Process", "EXEC", model=Exec)
    fork = RelationshipTo("Process", "FORK", model=Fork)
    suspend = RelationshipTo("Process", "SUSPEND", model=SuspendResume)
    resume = RelationshipTo("Process", "RESUME", model=SuspendResume)
    socks = RelationshipTo("Process", "SHUT_SOCKS", model=SuspendResume)
    gettask = RelationshipTo("Process", "GETTASK", model=GetTask)

class FileOp(StructuredRel):
    op = StringProperty(unique_index=False, required=True)
    unix_time = IntegerProperty(unique_index=False, required=True)
    global_seq_num = IntegerProperty(unique_index=False, required=False)

class File(StructuredNode):
    hostname = StringProperty(unique_index=False, required=True)
    es_message_version = IntegerProperty(unique_index=False)
    target_path = StringProperty(unique_index=False, required=True)

    creator = RelationshipFrom(Process, "CREATED", model = FileOp)
    opener = RelationshipFrom(Process, "OPENED", model = FileOp)
    writer = RelationshipFrom(Process, "WROTE", model = FileOp)
    accessor = RelationshipFrom(Process, "ACCESSED", model = FileOp)
    closer = RelationshipFrom(Process, "CLOSED", model = FileOp)
    mount = RelationshipFrom(Process, "MOUNTED", model = Mount)
    unmount = RelationshipFrom(Process, "UNMOUNTED", model = Unmount)

class KextLoad(StructuredRel):
    unix_time = IntegerProperty(unique_index=False, required=True)
    global_seq_num = IntegerProperty(unique_index=False, required=False)

class KextUnload(StructuredRel):
    unix_time = IntegerProperty(unique_index=False, required=True)
    global_seq_num = IntegerProperty(unique_index=False, required=False)

class Kext(StructuredNode):
     hostname = StringProperty(unique_index=False, required=True)
     es_message_version = IntegerProperty(unique_index=False)
     identifier = StringProperty(unique_index=False, required=True)

     load = RelationshipFrom(Process, "LOADED", model = KextLoad)
     unload = RelationshipFrom(Process, "UNLOADED", model = KextUnload)

#class SendPointEvent(StructuredNode):
#    hostname = StringProperty(unique_index=False, required=True)
#    global_sequence_number = IntegerProperty(unique_index=False)
#    es_message_version = IntegerProperty(unique_index=False)