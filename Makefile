PCAP_DIR=$(shell pwd)/pcaps

pcaps:
	mkdir -p $(PCAP_DIR)
	cd $(PCAP_DIR) && git lfs clone https://github.com/automayt/ICS-pcap.git automayt-ics-pcaps
	cd $(PCAP_DIR) && git clone https://github.com/elcabezzonn/Pcaps elcabezzonn-pcaps && cd elcabezzonn-pcaps && gunzip -f *.gz
	cd $(PCAP_DIR) && git clone https://github.com/chrissanders/packets.git chrissanders-packets
	#add those from Suricata: https://suricata.readthedocs.io/en/latest/public-data-sets.html
	#add Wireshark pcaps
	#clean all files that are not pcaps afterwards

clean:
	rm -rf pcaps/
