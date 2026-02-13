# Strike counter, memory wiper, and deadswitch
import ctypes  # wiping memory on low level
import random
import time

PARANOIA_THRESHOLD = 3  # Number of failed attempts before triggering the deadswitch
ON_TRIGGER = "wipe"  # Action to take on trigger
# possible values, sorted by severity of actions taken:
# - "self_destruct": Abandon all connections, wipe the application and rewrite random data over it, effectively rendering it non existent
# - "wipe": Wipe all sensitive data in memory, including keys, message buffers, and logs. The application remains operable but is a blank slate.
# - "dump_encrypted": Dump all sensitive data to a bundle file encrypted with PSK


class Monitor:
    def __init__(self):
        self.strike_count = 0
