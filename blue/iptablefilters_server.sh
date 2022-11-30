GATEWAY="gateway.secure-g3.offtech"
ssh $GATEWAY<<EOF
sudo su -
iptables -t mangle -A PREROUTING -s 10.1.1.2 -j ACCEPT
iptables -t mangle -A INPUT -s 10.1.1.2 -j ACCEPT
iptables -t mangle -A FORWARD -s 10.1.1.2 -j ACCEPT

iptables -A INPUT -i ethx -j ACCEPT
iptables -A OUTPUT -o ethx -j ACCEPT
iptables -A INPUT -p icmp --icmp-type echo-request -j ACCEPT --match limit --limit 30/minute
iptables -A INPUT -p tcp -s 10.1.3.2 --dport ssh -j DROP
iptables -A INPUT -p tcp -s 10.1.4.2 --dport ssh -j DROP
iptables -A INPUT -p tcp -s 10.1.2.2 --dport ssh -j DROP
#block furtive port scanning(check closed ports to detect open ones)
iptables -N port-scan
iptables -A port-scan -p tcp --tcp-flags SYN,ACK,FIN,RST RST -m limit --limit 1/s -j RETURN
iptables -A port-scan -j DROP
EOF