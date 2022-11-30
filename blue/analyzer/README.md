## Analyzer

First run the `./capture.sh <host>` script in the control server.

Then from your local machine launch:

```
ssh -T <username>@users.isi.deterlab.net ssh -T <host>.secure-g3.offtech "tail -f -n +1 ~/offtech-ctf-secure/blue/analyzer/pcap.pcap" | python3 analyze_pcap.py
```

NB: requires `pyshark` and `flask` installed on your local machine

