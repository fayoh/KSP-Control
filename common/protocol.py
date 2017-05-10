from common.autonumber import AutoNumber
from common.autonumber import Enumerator

enumeration_enumerator = Enumerator()

# Message structure
# (MessageType.LED_MSG, [(LED, state=LEDStates, blink=True|False)])
# (MessageType.BARGRAPH_MSG, [(BarGraph, state=0..100)])
# (MessageType.ACTION_MSG, (Action, data))
# (MessageType.STATUS_MSG, Status)
# (MessageType.KRPC_INFO_MSG [(KrpcInfo, data)])

class MessageType(AutoNumber):
    LED_MSG = ()
    BARGRAPH_MSG = ()
    ACTION_MSG = ()
    STATUS_MSG = ()
    KRPC_INFO_MSG = ()

enumeration_enumerator.reset()
MSGTYPE_DICT = {v: enumeration_enumerator.next()
                   for v in MessageType.__members__.values()}
MSGTYPE_REVERSE_DICT = {v:k  for k,v in MSGTYPE_DICT.items()}


class Status(AutoNumber):
    OK = ()
    DEGRADED = ()
    CONNECTION_LOST = ()

enumeration_enumerator.reset()
STATUS_DICT = {v: enumeration_enumerator.next()
                   for v in Status.__members__.values()}
STATUS_REVERSE_DICT = {v:k  for k,v in STATUS_DICT.items()}


class KrpcInfo(AutoNumber):
    GAME_SCENE = ()
    SAS_ENABLED = ()
    SAS_MODE = ()
    LANDING_GEAR = ()
    CONNECT_REMOTE_SERVER = ()
    WARP_MODE = ()
    WARP_MODE_MAX = ()
    STALL_MODE = ()
    EXPERIMENT_AVAILABLE = ()
    COMM_STATUS = ()
    TRANSMIT_SCIENCE_STATUS = ()
    CONTROL_STATE = ()
    BREAKS_ENABLED = ()
    RCS_ENABLED = ()
    REACTION_WHEELS_ENABLED = ()
    ENGINES_ENABLED = ()
    SHOW_UI = ()
    CRUISE_CONTROL = ()
    POWERSAVE = ()
    ACTION_GROUP = ()


enumeration_enumerator.reset()
KRPCINFO_DICT = {v: enumeration_enumerator.next()
                   for v in KrpcInfo.__members__.values()}
KRPCINFO_REVERSE_DICT = {v:k  for k,v in KRPCINFO_DICT.items()}


class DeploymentStatus(AutoNumber):
    RETRACTED = ()
    EXTENDED = ()
    MOVING = ()


enumeration_enumerator.reset()
DEPLOYMENT_STATUS_DICT = {v: enumeration_enumerator.next()
                   for v in DeploymentStatus.__members__.values()}
DEPLOYMENT_STATUS_REVERSE_DICT = {v:k  for k,v in DEPLOYMENT_STATUS_DICT.items()}


class Action(AutoNumber):
    LANDING_GEAR = ()
    LIGHTS = ()
    BREAKS = ()
    SAS_ENABLE = ()
    SAS_MODE = ()
    RCS = ()
    REACTION_WHEELS = ()
    PRECISION_MODE = ()
    ENGINES_ENABLED = ()
    SHOW_UI = ()
    ALL_EXTENDABLE_GEAR = ()
    CRUISE_CONTROL = ()
    POWERSAVE = ()
    ACTION_GROUP = ()
    STAGE = ()
    LIGHTTEST = ()
    ABORT = ()
    QUICK_SAVE = ()
    LOAD_QUICK_SAVE = ()
    RECOVER = ()
    DO_SCIENCE = ()
    WARP_TO_MANEUVER_NODE = ()
    JETTISON_FAIRING = ()
    FOCUS_NEXT_VEHICLE = ()
    FOCUS_PREVIOUS_VEHICLE = ()
    CAMERA_MODE = ()
    WARP_MODE_CHANGE = ()


enumeration_enumerator.reset()
ACTION_DICT = {v: enumeration_enumerator.next()
                   for v in Action.__members__.values()}
ACTION_REVERSE_DICT = {v:k  for k,v in ACTION_DICT.items()}
