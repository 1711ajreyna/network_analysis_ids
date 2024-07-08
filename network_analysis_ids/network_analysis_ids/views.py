from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from traffic_analysis.forms import PcapFileForm
from traffic_analysis.models import PcapFile
from traffic_analysis.tasks import analyze_pcap_file
from celery.result import AsyncResult

def index(request):
    return render(request, 'base.html')

def upload_view(request):
    form = PcapFileForm()
    return render(request, 'upload.html', {'form':form})

def results_view(request, task_id):
    pcap_file = PcapFile.objects.get(id=pcap_file_id)
    file_path = pcap_file.file.path
    packets = analyze_pcap_file(file_path)
    return render(request, 'results.html', {'packets': packets})

def upload_file(request):
    if request.method == 'POST':
        form = PcapFileForm(request.POST, request.FILES)
        if form.is_valid():
            pcap_file = form.save()
            task = analyze_pcap_file.delay(pcap_file.file.path)
            return redirect('task_status', task_id=task.id)
    else:
        form = PcapFileForm()
    return  render(request, 'upload.html', {'form': form})

def task_status(request, task_id):
    task = AsyncResult(task_id)
    if task.state =='SUCCESS':
        return redirect('results', pcap_file_id=task.result)
    return render(request, 'task_status.html', {'task': task})

def analyze_traffic(request, pcap_file_id):
    pcap_file = get_object_or_404(PcapFile, pk=pcap_file_id)
    analyze_pcap_file.delay(pcap_file.file_path)
    return render(request, 'analyze_traffic.html', {'pcap_file': pcap_file})
