from django.shortcuts import render, redirect
from .forms import PcapFileForm
from .models import PcapFile
from .tasks import analyze_pcap_file
from celery.result import AsyncResult

def upload_file(request):
    if request.method == 'POST':
        form = PcapFileForm(request.POST, request.FILES)
        if form.is_valid():
            pcap_file = form.save()
            task = analyze_pcap_file.delay(pcap_file.file.path)
            return redirect('task_status', task_id=task.id)
    else:
        form = PcapFileForm()
    return render(request, 'upload.html', {'form': form})

def task_status(request, task_id):
    task = AsyncResult(task_id)
    if task.state == 'SUCCESS':
        return redirect('results', pcap_file_id=task.result)
    return render(request, 'task_status.html', {'task': task})

def analyze_traffic(request, pcap_file_id):
    pcap_file = PcapFile.objects.get(id=pcap_file_id)
    analyze_pcap_file.delay(pcap_file.file.path)
    return render(request, 'analyze_traffic.html', {'pcap_file': pcap_file})
