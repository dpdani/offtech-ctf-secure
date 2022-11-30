#! /usr/bin/env python

import sys
from flask import Flask, render_template
import json

from pyshark.capture.pipe_capture import PipeCapture
import threading
from collections import OrderedDict

app = Flask(__name__)

MAX_PKTS_IN_CAPTURE = "1000000"  # used to reset internal capture session when reached the specified number of packets
packets_categories_dict = {"TCP": 0, "UDP": 0, "TCP SYN": 0, "ICMP": 0, "Others": 0}  # numbers of packets per protocol
ip_dict = {}  # numbers of packets per ip
packets_timestamp_list = []
http_req_packets_list = []  # store the HTTP request packets
total_http_delay = 0.0
slow_http_responses = 0
date_dict = OrderedDict()


def thread_function(capture):
    print("Thread called")
    capture.apply_on_packets(analyze)


def analyze(pkt):
    # print(pkt)
    global total_http_delay
    global slow_http_responses
    global packets_timestamp_list
    global http_req_packets_list
    global total_http_delay

    # reset data structures if the capture reaches the upper limit of packets
    if len(packets_timestamp_list) > int(MAX_PKTS_IN_CAPTURE):
        print("Reached upper limit of packets in the capture session. Resetting the large data structures...")
        packets_timestamp_list = []
        http_req_packets_list = []
        total_http_delay = 0

    packets_timestamp_list.append(pkt.sniff_timestamp)

    # update the date_dict to be able to compute the packets per seconds
    key = str(pkt.sniff_time.replace(microsecond=0))
    if key in date_dict:
        date_dict[key] = date_dict[key]+1
    else:
        date_dict[key] = 1

    if 'ip' in pkt:
        if pkt.ip.src not in ip_dict:
            ip_dict[pkt.ip.src] = {"TCP": 0, "UDP": 0, "TCP SYN": 0, "ICMP": 0, "Others": 0}
        if 'tcp' in pkt:
            packets_categories_dict['TCP'] = packets_categories_dict["TCP"] + 1
            ip_dict[pkt.ip.src]["TCP"] = ip_dict[pkt.ip.src]["TCP"] + 1
            if pkt.tcp.flags_syn == "1" and pkt.tcp.flags_ack == "0":
                packets_categories_dict['TCP SYN'] = packets_categories_dict["TCP SYN"] + 1
                ip_dict[pkt.ip.src]["TCP SYN"] = ip_dict[pkt.ip.src]["TCP SYN"] + 1
            if 'http' in pkt:
                # print("HTTP")
                # print(pkt)
                if hasattr(pkt.http, 'request_line'):  # if it is a HTTP request
                    # print("HTTP REQUEST")
                    http_req_packets_list.append([str(pkt.sniff_time), pkt.ip.src, pkt.tcp.srcport,
                                                  pkt.http.request_method, pkt.http.request_uri,
                                                  pkt.http.request_version, pkt.http.host, pkt.http.user_agent])
                    #print(http_req_packets_list)
                    # print(pkt.http.field_names)
                if hasattr(pkt.http, 'request_in'):  # if it is a HTTP response
                    try:
                        req_timestamp = packets_timestamp_list[int(pkt.http.request_in) - 1]  # -1 because frame
                        # index start from 1
                        approximate_delay = float(pkt.sniff_timestamp) - float(req_timestamp)
                        if approximate_delay > 0.5:
                            slow_http_responses = slow_http_responses + 1
                        total_http_delay += approximate_delay
                    except:
                        print("Corresponding HTTP request not found during the calculation of the delay")

        elif 'udp' in pkt:
            packets_categories_dict["UDP"] = packets_categories_dict["UDP"] + 1
            ip_dict[pkt.ip.src]["UDP"] = ip_dict[pkt.ip.src]["UDP"] + 1
            # print("UDP: " + str(packets_categories_dict["UDP"]))
        elif 'icmp' in pkt:
            packets_categories_dict["ICMP"] = packets_categories_dict["ICMP"] + 1
            ip_dict[pkt.ip.src]["ICMP"] = ip_dict[pkt.ip.src]["ICMP"] + 1
            # print("ICMP: " + str(packets_categories_dict["ICMP"]))
    else:
        packets_categories_dict["Others"] = packets_categories_dict["Others"] + 1
        # ip_dict[pkt.ip.src]["Others"] = ip_dict[pkt.ip.src]["Others"] + 1 # NON IP protocol...


@app.route("/index.html")
@app.route("/")
def root():
    return render_template('index.html', total_pkts=len(packets_timestamp_list))


@app.route("/http.html")
def http():
    if len(http_req_packets_list) > 0:
        return render_template('http.html', avg_delay=(total_http_delay / len(http_req_packets_list)),
                               slow=slow_http_responses)
    else:
        return render_template('http.html', avg_delay=0)


@app.route("/ip.html")
def ip():
    return render_template('ip.html')


@app.route("/get_categories")
def get_categories():
    return json.dumps(packets_categories_dict)


@app.route("/get_http_req")
def get_http_req():
    ret = {"data": http_req_packets_list}
    return json.dumps(ret)


@app.route("/get_ips")
def get_ips():
    ip_dict.pop('10.1.5.2', None)  # do not count the server in the source IP statistics
    ret = []
    for key, data in ip_dict.items():
        ret.append([key, data["TCP"], data["UDP"], data["ICMP"], data["Others"]])

    return json.dumps({"data": ret})


@app.route("/get_pkt_sec")
def get_pkt_sec():
    ret = []
    for key, data in date_dict.items():
        ret.append({"x": key, "y": data})
    return json.dumps(ret[-31:-1])  # return the last 30 timestamp with packets excluding the last
    # because the current second it is still not expired


@app.route("/release_resources")
def release_resources():
    global ip_dict
    global http_req_packets_list
    global packets_timestamp_list
    global total_http_delay
    ip_dict = {}
    http_req_packets_list = []
    packets_timestamp_list = []
    total_http_delay = 0
    return render_template('index.html')


if __name__ == '__main__':

    cap = PipeCapture(pipe=sys.stdin, custom_parameters={"-M": MAX_PKTS_IN_CAPTURE})  # auto resets tshark cap session
    x = threading.Thread(target=thread_function, args=(cap,))
    x.start()

    app.run()
