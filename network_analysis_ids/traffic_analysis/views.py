from django.shortcuts import render, redirect, get_object_or_404
from .forms import PcapFileForm
from .models import PcapFile, NetworkPacket
from .tasks import analyze_pcap_file
from celery.result import AsyncResult
from django.urls import reverse

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
    context = {
        'task': task
    }
    if task.state == 'SUCCESS' and task.result:
        context['result'] = task.result
        pcap_file_id = task.result['pcap_file_id']
        return redirect(reverse('results', kwargs={'pcap_file_id': pcap_file_id}))
    return render(request, 'task_status.html', context)

def analyze_traffic(request, pcap_file_id):
    pcap_file = PcapFile.objects.get(id=pcap_file_id)
    analyze_pcap_file.delay(pcap_file.file.path)
    return render(request, 'analyze_traffic.html', {'pcap_file': pcap_file})

def results_view(request, pcap_file_id):
    packets = NetworkPacket.objects.filter(pcap_file_id=pcap_file_id)
    context = {
        'packets': packets
    }
    return render(request, 'results.html', context)
