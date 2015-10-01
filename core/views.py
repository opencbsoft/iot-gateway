from django.shortcuts import render, redirect
from django.http import HttpResponse

from core.models import Device


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def index(request):
    data = dict()
    data['ip'] = get_client_ip(request)
    data['devices'] = Device.objects.all()
    if request.method == 'POST':
        if request.POST.get('action') == 'disable':
            dev = Device.objects.get(id=request.POST.get('id'))
            dev.enabled = False
            dev.save()
            return redirect('index')
        elif request.POST.get('action') == 'enable':
            dev = Device.objects.get(id=request.POST.get('id'))
            dev.enabled = True
            dev.save()
            return redirect('index')
    return render(request, 'index.html', data)


def device(request, url):
    data = dict()
    ip = get_client_ip(request)
    if url not in ['0', '1', '2']:
        error = 'The type of the client should be one of these "0" "1" "2".'
    else:
        dev, dev_created = Device.objects.get_or_create(ip=get_client_ip(request), type=url)
        """
            PROCESS DEVICE LOGIC
        """

    if error:
        return HttpResponse(status=404, content=error)
    else:
        return HttpResponse(status=200)
