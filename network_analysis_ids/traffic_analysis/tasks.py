from __future__ import absolute_import, unicode_literals
from celery import shared_task
from .models import PcapFile
from .utils import read_pcap

@shared_task
def analyze_pcap_file(file_path):
    # Read the pcap file using read_pcap from utils.py
    packet_details, alerts = read_pcap(file_path)

    try:
        pcap_file = PcapFile.objects.get(file=file_path)  # Adjust based on your model's field
    except PcapFile.DoesNotExist:
        # Handle the case where the file doesn't exist in your database
        # This is just a placeholder
        return None
    
    # Combine the results from read_pcap and pyshark analysis
    combined_results = {
        'read_pcap_analysis': {
            'packet_details': packet_details,
            'alerts': alerts
        }
    }
    
    # Return a dictionary with 'pcap_file_id' and 'analysis'
    result = {
        'pcap_file_id': pcap_file.id,  # Ensure this is an integer ID
        'analysis': combined_results,  # The actual combined analysis results
    }
    
    return result

