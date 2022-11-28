import enum


class Attack(str, enum.Enum):
    asd = 'asd'
    http = 'http'
    icmp = 'icmp'
    ping = 'ping'
    syn = 'syn'
    rst = 'rst'
    time_moves_slow = 'time-moves-slow'
    time_moves_spoof = 'time-moves-spoof'
    rate_limit = "rate-limit"
    shut_up = 'shut-up'

    def get_script(self):
        if self == "asd":
            from . import asd
            return asd
        elif self == "http":
            from . import http_flood
            return http_flood
        elif self == "icmp":
            from . import icmp_flood
            return icmp_flood
        elif self == "ping":
            from . import ping_of_death
            return ping_of_death
        elif self == "syn":
            from . import syn_flood
            return syn_flood
        elif self == "rst":
            from . import rst
            return rst
        elif self == "time-moves-slow":
            from . import time_moves_slow
            return time_moves_slow
        elif self == "shut-up":
            from . import shut_up
            return shut_up
        elif self == "rate-limit":
            from . import rate_limit
            return rate_limit
        elif self == "time-moves-spoof":
            from . import time_moves_spoof
            return time_moves_spoof
