
from neomodel import StructuredNode, StructuredRel, StringProperty, IntegerProperty, RelationshipTo, RelationshipFrom, config
from neomodel.properties import BooleanProperty

class Signal(StructuredRel):
    signal = IntegerProperty(unique_index=False, required=True)

class Fork(StructuredRel):
    fork_pid = IntegerProperty(unique_index=False, required=False)

class Exec(StructuredRel):
    pid = IntegerProperty(unique_index=False)
    ppid = IntegerProperty(unique_index=False)

class SuspendResume(StructuredRel):
    pid = IntegerProperty(unique_index=False)

class GetTask(StructuredRel):
    tgt_pid = IntegerProperty(unique_index=False)

#class SendPointEvent(StructuredNode):
#    hostname = StringProperty(unique_index=False, required=True)
#    global_sequence_number = IntegerProperty(unique_index=False)
#    es_message_version = IntegerProperty(unique_index=False)

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

class KextLoad(StructuredRel):
    actor = RelationshipFrom(Process, "LOADED")

class KextUnload(StructuredRel):
    actor = RelationshipFrom(Process, "UNLOADED")

class File(StructuredNode):
    hostname = StringProperty(unique_index=False, required=True)
    es_message_version = IntegerProperty(unique_index=False)

    target_path = StringProperty(unique_index=False, required=True)

    creator = RelationshipFrom(Process, "CREATED", model = FileOp)
    opener = RelationshipFrom(Process, "OPENED", model = FileOp)
    writer = RelationshipFrom(Process, "WROTE", model = FileOp)
    accessor = RelationshipFrom(Process, "ACCESSED", model = FileOp)
    closer = RelationshipFrom(Process, "CLOSED", model = FileOp)
    kext_load = RelationshipFrom(Process, "KEXT_LOAD", model = KextLoad)
    kext_unload = RelationshipFrom(Process, "KEXT_UNLOAD", model = KextUnload)

class FileMount(StructuredNode):
    hostname = StringProperty(unique_index=False, required=True)
    global_sequence_number = IntegerProperty(unique_index=False)
    es_message_version = IntegerProperty(unique_index=False)

    dir = StringProperty(unique_index=False, required=True)
    mounted = RelationshipFrom("FileMount", "MOUNTED")
    actor = RelationshipFrom(Process, "MOUNT")

class FileUnmount(StructuredNode):
    hostname = StringProperty(unique_index=False, required=True)
    global_sequence_number = IntegerProperty(unique_index=False)
    es_message_version = IntegerProperty(unique_index=False)

    dir = StringProperty(unique_index=False, required=True)
    mounted = RelationshipTo(FileMount, "UNMOUNTED")
    actor = RelationshipFrom(Process, "UNMOUNT")
