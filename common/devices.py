from common.autonumber import AutoNumber
from common.autonumber import Enumerator

enumeration_enumerator = Enumerator()

class LED(AutoNumber):
    ALL = ()
    STARTUP_LOCAL = ()
    CONNECT_REMOTE_SERVER = ()
    SAS_MODE_STABILITY_ASSIST = ()
    SAS_MODE_MANEUVER = ()
    SAS_MODE_PROGRADE = ()
    SAS_MODE_RETROGRADE = ()
    SAS_MODE_NORMAL = ()
    SAS_MODE_ANTI_NORMAL = ()
    SAS_MODE_RADIAL = ()
    SAS_MODE_ANTI_RADIAL = ()
    SAS_MODE_TARGET = ()
    SAS_MODE_ANTI_TARGET = ()
    WARP_MODE_0 = ()
    WARP_MODE_1 = ()
    WARP_MODE_2 = ()
    WARP_MODE_3 = ()
    WARP_MODE_4 = ()
    WARP_MODE_5 = ()
    WARP_MODE_6 = ()
    WARP_MODE_7 = ()
    STALL = ()
    EXPERIMENT_AVAILABLE = ()
    COMM_STATUS = ()
    TRANSMIT_SCIENCE_STATUS = ()
    CONTROL_STATE = ()
    # Button leds
    LANDING_GEAR = ()
    LIGHTS = ()
    BREAKS = ()
    SAS = ()
    RCS = ()
    REACTION_WHEELS = ()
    PRECISION_MODE = ()
    ENGINES_ENABLED = ()
    SHOW_UI = ()
    ALL_EXTENDABLE_GEAR = ()
    CRUISE_CONTROL = ()
    POWERSAVE = ()
    ACTION_GROUP_1 = ()
    ACTION_GROUP_2 = ()
    ACTION_GROUP_3 = ()
    ACTION_GROUP_4 = ()
    ACTION_GROUP_5 = ()

LED_DICT = {v: enumeration_enumerator.next() for v in LED.__members__.values()}
LED_REVERSE_DICT = {v:k  for k,v in LED_DICT.items()}

class LEDStates(AutoNumber):
    RED = ()
    GREEN = ()
    BLUE = ()
    ORANGE = ()


enumeration_enumerator.reset()
LED_STATES_DICT = {v: enumeration_enumerator.next()
                   for v in LEDStates.__members__.values()}
LED_STATES_REVERSE_DICT = {v:k  for k,v in LED_STATES_DICT.items()}

class BarGraph(AutoNumber):
    ELECTRICAL_CHARGE = ()
    VSI = ()


enumeration_enumerator.reset()
BARGRAPH_DICT = {v: enumeration_enumerator.next()
                   for v in BarGraph.__members__.values()}
BARGRAPH_REVERSE_DICT = {v:k  for k,v in BARGRAPH_DICT.items()}
