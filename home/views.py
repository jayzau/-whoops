from django.http import HttpResponse
from django.shortcuts import render


# 登录
def login(request):
    if request.method == 'GET':
        return render(request, 'zau-login.html')


# 注册
def register(request):
    if request.method == 'GET':
        return render(request, 'zau-register.html')


def test(request):
    if request.method == 'GET':
        import time
        t = str(time.ctime())
        time.sleep(10)
        t += f'</br>{str(time.ctime())}'
        html = f"<html><body>{t}</body></html>"
        return HttpResponse(html)
