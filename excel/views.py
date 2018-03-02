import os
from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
from django.utils import timezone
from django.http import StreamingHttpResponse

from datetime import datetime
from urllib.parse import unquote
from random import randint

from . import models
from . import tools
from WordTo_Excel.settings import BASE_DIR

# Create your views here.


def index(request):
    return HttpResponse('Hello world!')


def get_excel(request, table_id=1):
    template = loader.get_template('excel/table.html')
    table = models.Table.objects.get(pk=table_id)
    #--------- 判断用户是否写入过数据
    ip = tools.get_ip(request)
    post_count = models.PostCount.objects.get_or_create(
        ip=ip, title=table.title)[0]
    row = post_count.rows
    row_value = tools.read_one_row(table.title, row) if row != 0 else None
    #-----------

    isShow = True if table.show == 1 else False
    exists_value = tools.read_from_excel(table.title) if isShow else None
    fields = table.field.split(',')
    if row_value:
        value_dict = dict(zip(fields, row_value))
    else:
        value_dict = dict()
        for key in fields:
            value_dict[key] = ''
    context = {
        'table_id': table_id,
        'title': table.title,
        'count': table.count,
        'isShow': isShow,
        'value_dict': value_dict,
        'exists_value': exists_value
    }
    return HttpResponse(template.render(context, request))


def form_action(request):
    template = loader.get_template('excel/result.html')
    #------------ 获得用户传过来的表
    items = request.POST.items()
    next(items)
    table_info_item = next(items)
    table_id, title = table_info_item[0], table_info_item[1]
    #------------ 从数据库中查询用户传过来的数据是否正确
    table = models.Table.objects.get(pk=table_id)
    if table.title == title:  # 表数据无误
        ip = tools.get_ip(request)  # 获得用户ip
        post_count = models.PostCount.objects.get_or_create(
            ip=ip, title=title)[0]
        rows = post_count.rows
        fields = table.field.split(',')
        tools.new_excel(title, fields)
        mark_rows = tools.write_to_excel(title, items, rows)
        result_info = '提交成功'
        post_count.rows = mark_rows  # 用户已插入数据,更新位置
        post_count.pub_time = timezone.now()
        post_count.save()
    else:
        result_info = '提交的表单信息与库中表不一致,请重新提交'
    context = {
        'result_info': result_info,
    }
    return HttpResponse(template.render(context, request))


def get_file(request):
    template = loader.get_template('excel/download.html')
    table = models.Table.objects.get(pk=1)
    context = {
        'file_name': '{}.xls'.format(table.title),
    }
    return HttpResponse(template.render(context, request))


def download_excel(request, file):
    file_path = os.path.join(BASE_DIR, file)

    def file_iterator(file_path, chunk_size=512):
        with open(file_path, 'rb') as f:
            while True:
                c = f.read(chunk_size)
                if c:
                    yield c
                else:
                    break

    response = StreamingHttpResponse(file_iterator(file_path))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename={0}'.format(file)
    return response


def article_page(request, article_id):
    pass
