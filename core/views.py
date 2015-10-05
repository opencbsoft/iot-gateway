import os
from django.shortcuts import render, redirect
from django.http import HttpResponse

from importlib.machinery import SourceFileLoader

from core.models import Device

def import_file(full_path_to_module):
    try:
        import os
        module_dir, module_file = os.path.split(full_path_to_module)
        module_name, module_ext = os.path.splitext(module_file)
        save_cwd = os.getcwd()
        os.chdir(module_dir)
        module_obj = __import__(module_name)
        module_obj.__file__ = full_path_to_module
        globals()[module_name] = module_obj
        os.chdir(save_cwd)
    except:
        raise ImportError


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
    error = False
    if url not in ['0', '1', '2']:
        error = 'The type of the client should be one of these "0" "1" "2".'
    else:
        dev, dev_created = Device.objects.get_or_create(ip=get_client_ip(request), type=url)
        """
            PROCESS DEVICE LOGIC
        """
        if dev.action_file:
            if os.path.exists(dev.action_file):
                import_file('/home/pi/iot-gateway/scripts/'+dev.action_file)
                main(request.GET)
    if error:
        return HttpResponse(status=404, content=error)
    else:
        return HttpResponse(status=200)
