import ipaddress
import random
import string
import struct

import netifaces

from red.config import config


def get_experiment_interface_and_ip():
    for iface in netifaces.interfaces():
        try:
            addr = netifaces.ifaddresses(iface)[netifaces.AF_INET][0]['addr']
        except KeyError:
            pass
        else:
            if addr.startswith('10.'):
                return iface, addr


def random_port():
    return random.randint(1025, 64000)


my_iface, my_ip = get_experiment_interface_and_ip()
my_network = str(ipaddress.ip_interface(f"{my_ip}/24").network)


def spoof_ip():
    def random_ip(network):
        network = ipaddress.IPv4Network(network)
        network_int, = struct.unpack("!I", network.network_address.packed)  # make network address into an integer
        rand_bits = network.max_prefixlen - network.prefixlen  # calculate the needed bits for the host part
        rand_host_int = random.randint(0, 2 ** rand_bits - 1)  # generate random host part
        ip_address = ipaddress.IPv4Address(network_int + rand_host_int)  # combine the parts
        return ip_address.exploded

    ip = random_ip(my_network)
    while ip in config.attack.spoof_blacklist:
        ip = random_ip(my_network)
    return ip


possible_string_values = str(string.ascii_letters + string.digits + string.punctuation)


def generate_random_string(length):
    return "".join(random.choices(possible_string_values, k=length))
