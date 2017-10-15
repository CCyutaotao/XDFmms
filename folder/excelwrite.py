
# -*- coding:utf-8 -*-
import os
import xlwt
import decimal

from datetime import datetime 


def student(jsondata):
    book = xlwt.Workbook(encoding = 'utf-8', style_compression = 0)
    sheet = book.add_sheet('output', cell_overwrite_ok = True)
    firstlinestyle = xlwt.easyxf('pattern:pattern solid, fore_colour blue; align: vertical center, horizontal center; font: height 300, bold true, colour white; borders: top double, bottom double, left double, right double;')
    contentstyle = xlwt.easyxf('pattern:pattern solid, fore_colour white; align: wrap on, vertical center, horizontal center; font: bold true, colour black; borders: top double, bottom double, left double, right double;')
    for colIndex in range(0, 22):
   	 sheet.col(colIndex).width = 4000 
            
    sheet.write(0, 0, u'日期', firstlinestyle)
    sheet.write(0, 1, u'来源', firstlinestyle)
    sheet.write(0, 2, u'来源说明', firstlinestyle)
    sheet.write(0, 3, u'校区', firstlinestyle)
    sheet.write(0, 4, u'店长/店长助理', firstlinestyle)
    sheet.write(0, 5, u'学生姓名', firstlinestyle)
    sheet.write(0, 6, u'性别', firstlinestyle)
    sheet.write(0, 7, u'年级', firstlinestyle)
    sheet.write(0, 8, u'学校', firstlinestyle)
    sheet.write(0, 9, u'电话',firstlinestyle)
    sheet.write(0, 10, u'是否加微信',firstlinestyle)
    sheet.write(0, 11, u'是否报名',firstlinestyle)
    sheet.write(0, 12, u'报名日期',firstlinestyle)
    sheet.write(0, 13, u'科目数',firstlinestyle)
    sheet.write(0, 14, u'数', firstlinestyle)
    sheet.write(0, 15, u'语', firstlinestyle)
    sheet.write(0, 16, u'英', firstlinestyle)
    sheet.write_merge(0, 0, 17, 22, u'学生追踪情况', firstlinestyle)                
    sumline = 0

    for index, data in enumerate(jsondata):
        used = 0
        startline = sumline +1   
        if data.get("firstfollow",''):
	    dic =eval(data["firstfollow"])
	    col = 17
            for key in dic :
                sheet.write(startline, col, key)
                sheet.write(startline+1, col, dic[key])
	    	col+=1
    	endline = sumline = startline + 1
        sheet.write_merge(startline, endline, 0, 0, data.get("recordtime",u''), contentstyle)
        sheet.write_merge(startline, endline, 1, 1, data.get("infosource",u''), contentstyle)
        sheet.write_merge(startline, endline, 2, 2, data.get("infosourceintroduction",u''), contentstyle)
        sheet.write_merge(startline, endline, 3, 3, data.get("campusname",u''), contentstyle)
        sheet.write_merge(startline, endline, 4, 4, data.get("recordername",u''), contentstyle)
        sheet.write_merge(startline, endline, 5, 5, data.get("studentname",u''), contentstyle)
        sheet.write_merge(startline, endline, 6, 6, data.get("sex",u'') , contentstyle)
        sheet.write_merge(startline, endline, 7, 7, data.get("grade",u''), contentstyle)
    	sheet.write_merge(startline, endline, 8, 8, data.get("schoolname",u''), contentstyle)
        sheet.write_merge(startline, endline, 9, 9, data.get("phone",u''), contentstyle)
        sheet.write_merge(startline, endline, 10, 10, data.get("wechatornot",u''), contentstyle)
        sheet.write_merge(startline, endline, 11, 11, data.get("registornot",u''), contentstyle)
        sheet.write_merge(startline, endline, 12, 12, data.get("registtime",u''), contentstyle) 
        sheet.write_merge(startline, endline, 13, 13, xlwt.Formula("O{}+P{}+Q{}".format(startline+1, startline+1, startline+1)), contentstyle)
        sheet.write_merge(startline, endline, 14, 14, data.get("math",u''), contentstyle)
        sheet.write_merge(startline, endline, 15, 15, data.get("chinese",u''), contentstyle)
        sheet.write_merge(startline, endline, 16, 16, data.get("english",u''), contentstyle)

    filename = 'stafflog{0}__{1}.xls'.format(datetime.now().strftime("_%Y_%m_%d"), data.get("recordername",u''))
    filefullpath = '{}/{}'.format(os.path.dirname(__file__), filename)
    book.save(filefullpath)
    return filefullpath


def count(jsondata):
	jsondata = {}
	book = xlwt.Workbook(encoding = 'utf-8', style_compression = 0)
    	sheet = book.add_sheet('output', cell_overwrite_ok = True)
	filename = 'statistics{0}__{1}.xls'.format(datetime.now().strftime("_%Y_%m_%d"), jsondata.get("recordername",u''))
    	filefullpath = '{}/{}'.format(os.path.dirname(__file__), filename)
    	book.save(filefullpath)
    	return filefullpath
				
