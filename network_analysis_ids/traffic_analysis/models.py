from django.db import models

class PcapFile(models.Model):
    file = models.FileField(upload_to='pcap_files/')    # Stores uploaded pcap files
    upload_at = models.DateTimeField(auto_now_add=True) # stores the time of uppload

    def __str__(self):
        return self.file.name
    
class AnalysisResult(models.Model):
    pcap_file = models.OneToOneField(PcapFile, on_delete=models.CASCADE)
    packets = models.JSONField()  