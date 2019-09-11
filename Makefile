PCAP_DIR=$(shell pwd)/pcaps
BIN_DIR=$(shell pwd)/bin

pcaps:
	mkdir -p $(PCAP_DIR)
	cd $(PCAP_DIR) && git lfs clone https://github.com/automayt/ICS-pcap.git automayt-ics-pcaps \
	  && find $(PCAP_DIR)/automayt-ics-pcaps -name '*.pcap' -print0 | xargs -0 mv -S _ --backup=numbered -ft $(PCAP_DIR) \
	  && rm -rf $(PCAP_DIR)/automayt-ics-pcaps
	cd $(PCAP_DIR) && git clone https://github.com/elcabezzonn/Pcaps elcabezzonn-pcaps \
	  && cd elcabezzonn-pcaps \
	  && gunzip -f *.gz \
	  && find $(PCAP_DIR)/elcabezzonn-pcaps -name '*.pcap' | xargs mv -S _ --backup=numbered -ft $(PCAP_DIR) \
	  && rm -rf $(PCAP_DIR)/elcabezzonn-pcaps
	cd $(PCAP_DIR) && git clone https://github.com/chrissanders/packets.git chrissanders-packets \
	  && find $(PCAP_DIR)/chrissanders-packets -name '*.pcapng' | xargs mv -S _ --backup=numbered -ft $(PCAP_DIR) \
	  && rm -rf $(PCAP_DIR)/chrissanders-packets
	# http://www.ll.mit.edu/mission/communications/cyber/CSTcorpora/ideval/data/ is down
	# these are huge
	#cd $(PCAP_DIR) && wget -nd -P . -r -l 2 --no-parent -A '*.pcap.gz' 'https://download.netresec.com/pcap/'
	#cd $(PCAP_DIR) && wget --no-check-certificate -nd -P . -r -l 3 --no-parent -A '*.pcap' 'https://mcfp.felk.cvut.cz/publicDatasets/'
	cd $(PCAP_DIR) && python $(BIN_DIR)/scrape_ws.py
	cd $(PCAP_DIR) \
	   && wget https://github.com/zeek/zeek/archive/master.zip \
	   && unzip -qq master.zip \
	   && find $(PCAP_DIR)/zeek-master -name '*.pcap' | xargs mv -S _ --backup=numbered -ft $(PCAP_DIR) \
	   && rm master.zip \
	   && rm -rf zeek-master
	find $(PCAP_DIR) -name '*.pcap.gz' -exec gunzip {} \;
	find $(PCAP_DIR) -name '*.pcapng' -exec editcap -F libpcap {} {}.pcap \;
	find $(PCAP_DIR) -name '*.pcapng' -delete
	chmod -R 0755 $(PCAP_DIR)

clean:
	rm -rf pcaps/
