import re
import xlwt
import math
import pandas as pd

## read html file to get all style data
filepath = "D:\\1-Projects\\dev\\html2spreadsheet\\css-template.html"
file = open(filepath, 'r', encoding='utf-8')
text = file.read()
file.close()
df = pd.DataFrame(columns=['divno','left','top','width','height'])

## get style data into DataFrame
reg = r'left:[0-9]*px;\n[\s]top:[0-9]*px;\n[\s]width:[0-9]*px;\n[\s]height:[0-9]*px;'
pattern = re.compile(reg)
style_all = re.findall(pattern, text)
i = 1

for style in style_all:
	reg = r'left:[0-9]*'
	pattern = re.compile(reg)
	left = int(re.findall(pattern, style)[0][5:])
	reg = r'top:[0-9]*'
	pattern = re.compile(reg)
	top = int(re.findall(pattern, style)[0][4:])
	reg = r'width:[0-9]*'
	pattern = re.compile(reg)
	width = int(re.findall(pattern, style)[0][6:])
	reg = r'height:[0-9]*'
	pattern = re.compile(reg)
	height = int(re.findall(pattern, style)[0][7:])
	line = {'divno':i,'left':left,'top':top,'width':width,'height':height}
	df = df.append(line, ignore_index=True)
	i=i+1

div_total = len(df)
## combine left & width data into one column
## Excel column default 80px 80*1000/35=2285.714
## worksheet.col(0).width = 1000  ##35px
## worksheet.col(2).width = 2000  ##70px

#sleft = df['left']
#df_left = pd.DataFrame(columns=['leftwidth'])
#df_left['leftwidth']=sleft
#for i in range(len(sleft)):
#	df_left = df_left.append({'leftwidth': df['left'][i]+df['width'][i]}, ignore_index=True)
#sleft = df.loc[:,['divno','left','width']]
sleft = df.loc[:,['divno','left']]
df_left = pd.DataFrame(columns=['divno','leftwidth'])
df_left['divno']=sleft['divno']
df_left['leftwidth']=sleft['left']
df_left_colno = pd.DataFrame(columns=['divno', 'colno'])
for i in range(len(sleft)):
	df_left = df_left.append({'divno': df['divno'][i], 'leftwidth': df['left'][i]+df['width'][i]}, ignore_index=True)

df_left = df_left.sort_values(by='leftwidth', ascending=True)

#setop = df['top']
#df_top = pd.DataFrame(columns=['topheight'])
#df_top['topheight']=setop
#for i in range(len(setop)):
#	df_top = df_top.append({'topheight': df['top'][i]+df['height'][i]}, ignore_index=True)
setop = df.loc[:,['divno','top']]
df_top = pd.DataFrame(columns=['divno','topheight'])
df_top['divno']=setop['divno']
df_top['topheight']=setop['top']
df_top_rowno = pd.DataFrame(columns=['divno', 'rowno'])
for i in range(len(setop)):
	df_top = df_top.append({'divno': df['divno'][i], 'topheight': df['top'][i]+df['height'][i]}, ignore_index=True)

df_top = df_top.sort_values(by='topheight', ascending=True)

## write into Excel
i = 0
workbook = xlwt.Workbook()
worksheet = workbook.add_sheet('main')
for l in range(len(df_left)):
	if df_left.iloc[l]['leftwidth'] > 0:
		i = i + 1
		element_left = df_left.iloc[l]['leftwidth']
		cell = math.modf(element_left/80)
		cell_number = int(cell[1])
		cell_slice = int(cell[0]*80*1000/35)
		if i == 1:
			prev_distance = element_left
			used_cell_number = cell_number + 1
			print("Setting Column %s's width as %d" %(cell_number, cell_slice))
			worksheet.col(cell_number).width = cell_slice
			df_left_colno = df_left_colno.append({'divno': df_left.iloc[l]['divno'], 'colno': cell_number}, ignore_index=True)
		else:
			if element_left > prev_distance:
				#print(df_left.iloc[l])
				cell = math.modf((element_left - prev_distance)/80)
				cell_number = int(cell[1])
				cell_slice = int(cell[0]*80*1000/35)
				print("Setting Column %s's width as %d" %(used_cell_number + cell_number, cell_slice))
				worksheet.col(used_cell_number + cell_number + 1).width = cell_slice
				df_left_colno = df_left_colno.append({'divno': df_left.iloc[l]['divno'], 'colno': used_cell_number + cell_number + 1}, ignore_index=True)
				used_cell_number = used_cell_number + cell_number + 1
				prev_distance =  element_left
i = 0
for h in range(len(df_top)):
	if df_top.iloc[h]['topheight'] > 0:
		i = i + 1
		element_top = df_top.iloc[h]['topheight']
		cell = math.modf(element_top/22)
		cell_number = int(cell[1])
		cell_slice = int(cell[0]*22*1000/35)
		if i == 1:
			prev_height = element_top
			used_cell_number = cell_number + 1
			#print(used_cell_number)
			print("Setting Row %s's height as %d" %(cell_number, cell_slice))
			worksheet.row(cell_number).height_mismatch = True
			worksheet.row(cell_number).height = cell_slice
			df_top_rowno = df_top_rowno.append({'divno': df_top.iloc[h]['divno'], 'rowno': cell_number}, ignore_index=True)
		else:
			if element_top > prev_height:
				#print(df_left.iloc[l])
				cell = math.modf((element_top - prev_height)/22)
				cell_number = int(cell[1])
				cell_slice = int(cell[0]*22*1000/35)
				print("Setting Row %s's height as %d" %(used_cell_number + cell_number, cell_slice))
				worksheet.row(used_cell_number + cell_number + 1).height_mismatch = True
				worksheet.row(used_cell_number + cell_number + 1).height = cell_slice
				df_top_rowno = df_top_rowno.append({'divno': df_top.iloc[h]['divno'], 'rowno': used_cell_number + cell_number + 1}, ignore_index=True)
				used_cell_number = used_cell_number + cell_number + 1
				prev_height =  element_top

## merge cells
## @Todo

for i in range(div_total):
	print("divno %s's left colno are %s" %(i, df_left_colno[df_left_colno['divno']==i]))
	print("divno %s's top rowno are %s" %(i, df_top_rowno[df_top_rowno['divno']==i]))

workbook.save('D:\\0-Common\\Smartbi-addons\\html2spreadsheet\\frame_test1.xls')
