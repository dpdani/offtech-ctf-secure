GATEWAY="gateway.secure-g3.offtech"
ssh $GATEWAY<<EOF
sudo su -
iptables -t mangle -A PREROUTING -s 10.1.1.2 -j ACCEPT
iptables -t mangle -A INPUT -s 10.1.1.2 -j ACCEPT
iptables -t mangle -A FORWARD -s 10.1.1.2 -j ACCEPT

iptables -A INPUT -i ethx -j ACCEPT
iptables -A OUTPUT -o ethx -j ACCEPT

iptables -t mangle -A PREROUTING -m conntrack --ctstate INVALID -j DROP
iptables -t mangle -A PREROUTING -p tcp ! --syn -m conntrack --ctstate NEW -j DROP
iptables -t mangle -A PREROUTING -p tcp --tcp-flags FIN,SYN FIN,SYN -j DROP
iptables -t mangle -A PREROUTING -p tcp --tcp-flags SYN,RST SYN,RST -j DROP
iptables -t mangle -A PREROUTING -p tcp --tcp-flags FIN,RST FIN,RST -j DROP
iptables -t mangle -A PREROUTING -p tcp --tcp-flags FIN,ACK FIN -j DROP
iptables -t mangle -A PREROUTING -p tcp --tcp-flags ACK,URG URG -j DROP
iptables -t mangle -A PREROUTING -p tcp --tcp-flags ACK,PSH PSH -j DROP
iptables -t mangle -A PREROUTING -p tcp --tcp-flags ALL NONE -j DROP
iptables -A INPUT -p icmp --icmp-type echo-request -j ACCEPT --match limit --limit 30/minute
iptables -A INPUT -p tcp -s 10.1.3.2 --dport ssh -j DROP
iptables -A INPUT -p tcp -s 10.1.4.2 --dport ssh -j DROP
iptables -A INPUT -p tcp -s 10.1.2.2 --dport ssh -j DROP
EOF