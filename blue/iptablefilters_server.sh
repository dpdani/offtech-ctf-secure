SERVER="server.secure-g3.offtech"
DETERLAB=$(ssh $SERVER "ip addr | grep 192.168 | tail -c 5")

echo "Deterlab interface: $DETERLAB"

# Deleting already existing rules

ssh $SERVER "sudo iptables -F; sudo iptables -t nat -F; sudo iptables -t mangle -F"

# Inserting the new rules

ssh $SERVER<<EOF
sudo su -
iptables -t mangle -A PREROUTING -s 10.1.1.2 -j ACCEPT
iptables -t mangle -A INPUT -s 10.1.1.2 -j ACCEPT
iptables -t mangle -A FORWARD -s 10.1.1.2 -j ACCEPT

iptables -A INPUT -i $DETERLAB -j ACCEPT
iptables -A OUTPUT -o $DETERLAB -j ACCEPT
iptables -A INPUT -p icmp --icmp-type echo-request -j ACCEPT --match limit --limit 30/minute
iptables -A INPUT -p tcp -s 10.1.3.2 --dport ssh -j DROP
iptables -A INPUT -p tcp -s 10.1.4.2 --dport ssh -j DROP
iptables -A INPUT -p tcp -s 10.1.2.2 --dport ssh -j DROP
#block furtive port scanning(check closed ports to detect open ones)
iptables -N port-scan
iptables -A port-scan -p tcp --tcp-flags SYN,ACK,FIN,RST RST -m limit --limit 1/s -j RETURN
iptables -A port-scan -j DROP
EOF
