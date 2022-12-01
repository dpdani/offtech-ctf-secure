#!/usr/bin/env bash

sudo nmap -v server -oN out-nmap-ports.txt &
sudo nmap -A -v -T4 server -oN out-nmap-os.txt &
sudo nmap -sT -v server -oN out-nmap-tcp.txt &
#sudo nmap -sU -v server -oN out-nmap-udp.txt &
sudo nmap -Pn --script vuln server -oN out-nmap-vuln.txt &

wait
