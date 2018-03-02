import os

import xlrd
import xlwt
from xlutils.copy import copy
from WordTo_Excel.settings import BASE_DIR

#------------------ 获得访问者ip
def get_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
#-----------------

def get_file_path(title):
    file_path = os.path.join(BASE_DIR, '{title}.{suffix}'.format(title=title, suffix='xls'))
    return file_path;

def new_excel(title,fields):
    try:
        file_path = get_file_path(title)
        if os.path.exists(file_path):
            print('{}-已存在'.format(file_path))
            return
        book = xlwt.Workbook()
        sheet1 = book.add_sheet('Sheet1')
        sheet1.write(0,0,title)
        column_count = 0
        for field in fields:
            sheet1.write(1,column_count,field)
            column_count += 1
        book.save(file_path)
        print('新建-{}-成功'.format(file_path))
    except Exception:
        print('新建-{}-失败'.format(file_path))

def open_excel(title):
    try:
        file_path = get_file_path(title)
        data = xlrd.open_workbook(file_path)
        return data
    except Exception as e:
        print(str(e),'打开excel发生错误')

def read_from_excel(title):
    file_path = get_file_path(title)
    if os.path.exists(file_path):
        data = open_excel(title)
        table = data.sheet_by_name('Sheet1')
        row_two = table.row_values(1) # 获得第二行内容
        results = []
        for rownum in range(2,table.nrows):
            row = table.row_values(rownum) # 根据行号获取行
            if row:
                rows = {}
                for i in range(len(row)):
                    key = row_two[i]
                    if isinstance(key,float):
                        key = int(key)
                    if key=='':
                        key=str(i)
                    rows[key] = row[i]
                results.append(rows)
        results.reverse() # 倒序传回前端页面显示
        return results
    else:
        return None

def read_one_row(title,row):
    file_path = get_file_path(title)
    if os.path.exists(file_path):
        data = open_excel(title)
        table = data.sheet_by_name('Sheet1')
        one_row = table.row_values(row) # 获得第row+1行的内容
        return one_row
    else:
        return None
def write_to_excel(title,results,rows):
    try:
        file_path = get_file_path(title)    # 根据标题找到文件地址
        data = open_excel(title)    # 打开excel文件
        table = data.sheet_by_name('Sheet1')    # 打开表
        nrows = table.nrows # 获得行数
        book = copy(data) # 将xlrd打开的excel文件转换成xlwt可读写的文件
        sheet1 = book.get_sheet(0)
        column_count = 0
        mark_row = nrows if rows==0 else rows
        for key,value in results:
            sheet1.write(mark_row,column_count,value)
            column_count += 1
        book.save(file_path)
        print('数据保存到excel成功!')
        return mark_row
    except Exception:
        print('保存数据到excel时发生错误-write_to_excel')

if __name__ == '__main__':
    title = '测试标题-test'
    results = read_one_row(title,2)
    print(results)







