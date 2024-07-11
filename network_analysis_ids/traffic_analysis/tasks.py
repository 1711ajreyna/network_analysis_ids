from __future__ import absolute_import, unicode_literals
from celery import shared_task
from .models import PcapFile
from .utils import read_pcap
import logging

logger = logging.getLogger(__name__)

@shared_task
def analyze_pcap_file(file_path):
    logger.info(f"Analyzing pcap file at: {file_path}")

    try:
        # Read the pcap file using read_pcap from utils.py
        packet_details, alerts = read_pcap(file_path)

        if not packet_details or not alerts:
            logger.error("No packet details or alerts found")
            return {'error': 'No packet details or alerts found'}

        # Attempt to fetch the PcapFile object from the database
        try:
            pcap_file = PcapFile.objects.get(file=file_path)
        except PcapFile.DoesNotExist:
            logger.error(f"Pcap file does not exist in database: {file_path}")
            return {'error': 'Pcap file does not exist'}

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

        logger.info(f"Analysis result: {result}")
        
        return result

    except Exception as e:
        logger.exception(f"Exception occurred during pcap analysis: {e}")
        return {'error': f'Exception occurred: {str(e)}'}


