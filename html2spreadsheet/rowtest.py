import re
import xlwt
import math
import pandas as pd

workbook = xlwt.Workbook()
worksheet = workbook.add_sheet('main')

worksheet.row(1).height_mismatch = True
worksheet.row(1).height = int(22*12) # 52px
worksheet.row(2).height_mismatch = True
worksheet.row(2).height = int(11*12) # 26px
worksheet.row(3).height_mismatch = True
worksheet.row(3).height = int(5*12)  # 11px

workbook.save('D:\\0-Common\\Smartbi-addons\\html2spreadsheet\\rowtest.xls')