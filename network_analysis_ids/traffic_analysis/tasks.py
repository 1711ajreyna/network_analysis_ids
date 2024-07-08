from __future__ import absolute_import, unicode_literals
from celery import shared_task
from .models import PcapFile
from .utils import read_pcap


@shared_task
def analyze_pcap_file(file_path):
    return read_pcap(file_path)
