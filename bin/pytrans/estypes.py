from enum import IntEnum

class action_type_t(IntEnum):
    ES_ACTION_TYPE_AUTH = 0
    ES_ACTION_TYPE_NOTIFY = 1

class set_or_clear_t(IntEnum):
    ES_SET = 0
    ES_CLEAR = 1

# /**
#  * The valid event types recognized by EndpointSecurity
#  *
#  * @discussion When a program subscribes to and receives an AUTH-related event, it must respond
#  * with an appropriate result indicating whether or not the operation should be allowed to continue.
#  * The valid API options are:
#  * - es_respond_auth_result
#  * - es_respond_flags_result
#  *
#  * Currently, only ES_EVENT_TYPE_AUTH_OPEN must use es_respond_flags_result. All other AUTH events
#  * must use es_respond_auth_result.
#  */
class es_event_type_t(IntEnum):
    # The following events are available beginning in macOS 10.15
    ES_EVENT_TYPE_AUTH_EXEC = 0
    ES_EVENT_TYPE_AUTH_OPEN = 1
    ES_EVENT_TYPE_AUTH_KEXTLOAD = 2
    ES_EVENT_TYPE_AUTH_MMAP = 3
    ES_EVENT_TYPE_AUTH_MPROTECT = 4
    ES_EVENT_TYPE_AUTH_MOUNT = 5
    ES_EVENT_TYPE_AUTH_RENAME = 6
    ES_EVENT_TYPE_AUTH_SIGNAL = 7
    ES_EVENT_TYPE_AUTH_UNLINK = 8
    ES_EVENT_TYPE_NOTIFY_EXEC = 9
    ES_EVENT_TYPE_NOTIFY_OPEN = 10
    ES_EVENT_TYPE_NOTIFY_FORK = 11
    ES_EVENT_TYPE_NOTIFY_CLOSE = 12
    ES_EVENT_TYPE_NOTIFY_CREATE = 13
    ES_EVENT_TYPE_NOTIFY_EXCHANGEDATA = 14
    ES_EVENT_TYPE_NOTIFY_EXIT = 15
    ES_EVENT_TYPE_NOTIFY_GET_TASK = 16
    ES_EVENT_TYPE_NOTIFY_KEXTLOAD = 17
    ES_EVENT_TYPE_NOTIFY_KEXTUNLOAD = 18
    ES_EVENT_TYPE_NOTIFY_LINK = 19
    ES_EVENT_TYPE_NOTIFY_MMAP = 20
    ES_EVENT_TYPE_NOTIFY_MPROTECT = 21
    ES_EVENT_TYPE_NOTIFY_MOUNT = 22
    ES_EVENT_TYPE_NOTIFY_UNMOUNT = 23
    ES_EVENT_TYPE_NOTIFY_IOKIT_OPEN = 24
    ES_EVENT_TYPE_NOTIFY_RENAME = 25
    ES_EVENT_TYPE_NOTIFY_SETATTRLIST = 26
    ES_EVENT_TYPE_NOTIFY_SETEXTATTR = 27
    ES_EVENT_TYPE_NOTIFY_SETFLAGS = 28
    ES_EVENT_TYPE_NOTIFY_SETMODE = 29
    ES_EVENT_TYPE_NOTIFY_SETOWNER = 30
    ES_EVENT_TYPE_NOTIFY_SIGNAL = 31
    ES_EVENT_TYPE_NOTIFY_UNLINK = 32
    ES_EVENT_TYPE_NOTIFY_WRITE = 33
    ES_EVENT_TYPE_AUTH_FILE_PROVIDER_MATERIALIZE = 34
    ES_EVENT_TYPE_NOTIFY_FILE_PROVIDER_MATERIALIZE = 35
    ES_EVENT_TYPE_AUTH_FILE_PROVIDER_UPDATE = 36
    ES_EVENT_TYPE_NOTIFY_FILE_PROVIDER_UPDATE = 37
    ES_EVENT_TYPE_AUTH_READLINK = 38
    ES_EVENT_TYPE_NOTIFY_READLINK = 39
    ES_EVENT_TYPE_AUTH_TRUNCATE = 40
    ES_EVENT_TYPE_NOTIFY_TRUNCATE = 41
    ES_EVENT_TYPE_AUTH_LINK = 42
    ES_EVENT_TYPE_NOTIFY_LOOKUP = 43
    ES_EVENT_TYPE_AUTH_CREATE = 44
    ES_EVENT_TYPE_AUTH_SETATTRLIST = 45
    ES_EVENT_TYPE_AUTH_SETEXTATTR = 46
    ES_EVENT_TYPE_AUTH_SETFLAGS = 47
    ES_EVENT_TYPE_AUTH_SETMODE = 48
    ES_EVENT_TYPE_AUTH_SETOWNER = 49
    # The following events are available beginning in macOS 10.15.1
    ES_EVENT_TYPE_AUTH_CHDIR = 50
    ES_EVENT_TYPE_NOTIFY_CHDIR = 51
    ES_EVENT_TYPE_AUTH_GETATTRLIST = 52
    ES_EVENT_TYPE_NOTIFY_GETATTRLIST = 53
    ES_EVENT_TYPE_NOTIFY_STAT = 54
    ES_EVENT_TYPE_NOTIFY_ACCESS = 55
    ES_EVENT_TYPE_AUTH_CHROOT = 56
    ES_EVENT_TYPE_NOTIFY_CHROOT = 57
    ES_EVENT_TYPE_AUTH_UTIMES = 58
    ES_EVENT_TYPE_NOTIFY_UTIMES = 59
    ES_EVENT_TYPE_AUTH_CLONE = 60
    ES_EVENT_TYPE_NOTIFY_CLONE = 61
    ES_EVENT_TYPE_NOTIFY_FCNTL = 62
    ES_EVENT_TYPE_AUTH_GETEXTATTR = 63 
    ES_EVENT_TYPE_NOTIFY_GETEXTATTR = 64
    ES_EVENT_TYPE_AUTH_LISTEXTATTR = 65
    ES_EVENT_TYPE_NOTIFY_LISTEXTATTR = 66
    ES_EVENT_TYPE_AUTH_READDIR = 67
    ES_EVENT_TYPE_NOTIFY_READDIR = 68
    ES_EVENT_TYPE_AUTH_DELETEEXTATTR = 69
    ES_EVENT_TYPE_NOTIFY_DELETEEXTATTR = 70
    ES_EVENT_TYPE_AUTH_FSGETPATH = 71
    ES_EVENT_TYPE_NOTIFY_FSGETPATH = 72
    ES_EVENT_TYPE_NOTIFY_DUP = 73
    ES_EVENT_TYPE_AUTH_SETTIME = 74
    ES_EVENT_TYPE_NOTIFY_SETTIME = 75
    ES_EVENT_TYPE_NOTIFY_UIPC_BIND = 76
    ES_EVENT_TYPE_AUTH_UIPC_BIND = 77
    ES_EVENT_TYPE_NOTIFY_UIPC_CONNECT = 78
    ES_EVENT_TYPE_AUTH_UIPC_CONNECT = 79
    ES_EVENT_TYPE_AUTH_EXCHANGEDATA = 80
    ES_EVENT_TYPE_AUTH_SETACL = 81
    ES_EVENT_TYPE_NOTIFY_SETACL = 82
    # The following events are available beginning in macOS 10.15.4
    ES_EVENT_TYPE_NOTIFY_PTY_GRANT = 83
    ES_EVENT_TYPE_NOTIFY_PTY_CLOSE = 84
    ES_EVENT_TYPE_AUTH_PROC_CHECK = 85
    ES_EVENT_TYPE_NOTIFY_PROC_CHECK = 86
    ES_EVENT_TYPE_AUTH_GET_TASK = 87
    # The following events are available beginning in macOS 11.0
    ES_EVENT_TYPE_AUTH_SEARCHFS = 88
    ES_EVENT_TYPE_NOTIFY_SEARCHFS = 89
    ES_EVENT_TYPE_AUTH_FCNTL = 90
    ES_EVENT_TYPE_AUTH_IOKIT_OPEN = 91
    ES_EVENT_TYPE_AUTH_PROC_SUSPEND_RESUME = 92
    ES_EVENT_TYPE_NOTIFY_PROC_SUSPEND_RESUME = 93
    ES_EVENT_TYPE_NOTIFY_CS_INVALIDATED = 94
    ES_EVENT_TYPE_NOTIFY_GET_TASK_NAME = 95
    ES_EVENT_TYPE_NOTIFY_TRACE = 96
    ES_EVENT_TYPE_NOTIFY_REMOTE_THREAD_CREATE = 97
    ES_EVENT_TYPE_AUTH_REMOUNT = 98
    ES_EVENT_TYPE_NOTIFY_REMOUNT = 99
    # The following events are available beginning in macOS 11.3
    ES_EVENT_TYPE_AUTH_GET_TASK_READ = 100
    ES_EVENT_TYPE_NOTIFY_GET_TASK_READ = 101
    ES_EVENT_TYPE_NOTIFY_GET_TASK_INSPECT = 102
    # ES_EVENT_TYPE_LAST is not a valid event type but a convenience
    # value for operating on the range of defined event types.
    # This value may change between releases and was available
    # beginning in macOS 10.15
    ES_EVENT_TYPE_LAST = 103

# /**
#  * @brief Valid authorization values to be used when responding to a es_message_t auth event
#  */
class es_auth_result_t(IntEnum):
    # The event is authorized and should be allowed to continue
    ES_AUTH_RESULT_ALLOW = 0
    # The event is not authorized and should be blocked
    ES_AUTH_RESULT_DENY = 1

# /**
#  * @brief Valid values for the result_type of es_result_t to indicate the appropriate union member to use
#  */
class es_result_type_t(IntEnum):
    # The result is an auth result
    ES_RESULT_TYPE_AUTH = 0
    # The result is a flags result
    ES_RESULT_TYPE_FLAGS = 1

# /**
#  @brief Return value for functions that can only fail in one way
#  */
class es_return_t(IntEnum):
    ES_RETURN_SUCCESS = 0
    ES_RETURN_ERROR = 1

# /**
#  @brief Error conditions for responding to a message
#  */
class es_respond_result_t(IntEnum):
    ES_RESPOND_RESULT_SUCCESS = 0
    # One or more invalid arguments were provided
    ES_RESPOND_RESULT_ERR_INVALID_ARGUMENT = 1
    # Communication with the ES subsystem failed
    ES_RESPOND_RESULT_ERR_INTERNAL = 2
    # The message being responded to could not be found
    ES_RESPOND_RESULT_NOT_FOUND = 3
    # The provided message has been responded to more than once
    ES_RESPOND_RESULT_ERR_DUPLICATE_RESPONSE = 4
    # Either an inappropriate response API was used for the event type (ensure using proper
    # es_respond_auth_result or es_respond_flags_result function) or the event is notification only.
    ES_RESPOND_RESULT_ERR_EVENT_TYPE = 5

# /**
#  @brief Error conditions for creating a new client
#  */
class es_new_client_result_t(IntEnum):
    ES_NEW_CLIENT_RESULT_SUCCESS = 0
    # One or more invalid arguments were provided
    ES_NEW_CLIENT_RESULT_ERR_INVALID_ARGUMENT = 1
    # Communication with the ES subsystem failed
    ES_NEW_CLIENT_RESULT_ERR_INTERNAL = 2
    # The caller is not properly entitled to connect
    ES_NEW_CLIENT_RESULT_ERR_NOT_ENTITLED = 3
    # The caller is not permitted to connect. They lack Transparency, Consent, and Control (TCC) approval form the user.
    ES_NEW_CLIENT_RESULT_ERR_NOT_PERMITTED = 4
    # The caller is not running as root
    ES_NEW_CLIENT_RESULT_ERR_NOT_PRIVILEGED = 5
    # The caller has reached the maximum number of allowed simultaneously connected clients
    ES_NEW_CLIENT_RESULT_ERR_TOO_MANY_CLIENTS = 6

# /**
#  @brief Error conditions for clearing the authorisation caches
#  */
class es_clear_cache_result_t(IntEnum):
    ES_CLEAR_CACHE_RESULT_SUCCESS = 0
    # Communication with the ES subsystem failed
    ES_CLEAR_CACHE_RESULT_ERR_INTERNAL = 1
    # Rate of calls is too high. Slow down.
    ES_CLEAR_CACHE_RESULT_ERR_THROTTLE = 2

# /**
#  * @brief This enum describes the type of suspend/resume operations that are currently used.
#  */
class es_proc_suspend_resume_type_t(IntEnum):
    ES_PROC_SUSPEND_RESUME_TYPE_SUSPEND = 0
    ES_PROC_SUSPEND_RESUME_TYPE_RESUME = 1
    ES_PROC_SUSPEND_RESUME_TYPE_SHUTDOWN_SOCKETS = 3


