from scapy.all import rdpcap

# read_pcap will read and extract information from a layer
# of a packet that has layers

def read_pcap(file_path):
    packets = rdpcap(file_path)
    packet_details = []
    alerts = []
    for packet in packets:
        if packet.haslayer('IP'):
            details = {
                'timestamp': packet.time,
                'source_ip': packet['IP'].src,
                'destination_ip': packet['IP'].dst,
                'protocol': packet['IP'].proto,
                'payload': str(packet['IP'].payload)
            }
            packet_details.append(details)

            # Initilize alerts
            # Example IDS Rules
            if packet['IP'].src == '192.168.1.1':
                alerts.append(f"Suspicious activity detected from {packet['IP'].src}")
            if packet['IP'].proto == 6 and packet.sport == 23:
                alerts.append(f"Telnet traffic detected from {packet['IP'].src} to {packet['IP'].dst}")
    
    return packet_details, alerts

