from scapy.all import rdpcap

def read_pcap(file_path):
    try:
        packets = rdpcap(file_path)
    except Exception as e:
        # Log the exception and return empty results
        print(f"Error reading pcap file '{file_path}': {e}")
        return [], []

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

            # Example IDS Rules
            if packet['IP'].src == '192.168.1.1':
                alerts.append(f"Suspicious activity detected from {packet['IP'].src}")
            if packet['IP'].proto == 6 and packet.sport == 23:
                alerts.append(f"Telnet traffic detected from {packet['IP'].src} to {packet['IP'].dst}")

    if not packet_details and not alerts:
        print(f"No packet details or alerts found in pcap file '{file_path}'")

    return packet_details, alerts


