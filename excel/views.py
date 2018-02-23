from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader

from django.http.request import QueryDict

from . import models
from .tools import new_excel,write_to_excel,get_ip,read_from_excel

# Create your views here.


def index(request):
    return HttpResponse('Hello world!')

def get_excel(request):
    table = models.Table.objects.get(pk=1)
    template = loader.get_template('excel/table.html')
    isShow = True if table.show==1 else False
    exists_value = read_from_excel(table.title) if isShow else None

    fields = table.field.split(',')
    context = {
        'title': table.title,
        'count': table.count,
        'isShow':isShow,
        'fields': fields,
        'exists_value': exists_value
    }
    return HttpResponse(template.render(context,request))

def form_action(request):
    template = loader.get_template('excel/result.html')
    table = models.Table.objects.get(pk=1)
    ip = get_ip(request)
    post_count = models.PostCount.objects.get_or_create(ip=ip,title=table.title)[0]
    times = post_count.times
    print(times,type(times))
    if(times<2):
        fields = table.field.split(',')
        items = request.POST.items()
        next(items)
        title = next(items)[0]
        if table.title == title:
            new_excel(title,fields)
            write_to_excel(title,items)
            result_info = '提交成功'
            post_count.times += 1
            post_count.save()
        else:
            result_info = '提交的表单标题与库中表不一致,请重新提交'
    else:
        result_info = '提交失败,可能是因为提交次数过多,count={}'.format(times)
    context = {
        'result_info':result_info,
    }
    return HttpResponse(template.render(context,request))


def article_page(request,article_id):
    pass