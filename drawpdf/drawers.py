'''
'''
from reportlab.graphics.shapes import *
from reportlab.graphics.charts.lineplots import LinePlot
from reportlab.graphics.charts.textlabels import Label
from reportlab.graphics import renderPDF

drawing = Drawing(400, 200)

data = []
with open('./data.txt', 'r') as f:
    for line in f:
        if line and line[0].isdigit():
            data.append([float(n) for n in line.split()])

pred = [row[5] for row in data]
high = [row[6] for row in data]
low = [row[7] for row in data]
times = [row[0] + row[1]/12 for row in data]

lp = LinePlot()
lp.x = 50
lp.y = 50
lp.height = 125
lp.width = 300
lp.data = [zip(times, pred), zip(times, high), zip(times, low)]
lp.lines[0].strokeColor = colors.blue
lp.lines[1].strokeColor = colors.red
lp.lines[2].strokeColor = colors.green

drawing.add(lp)
drawing.add(String(250, 150, 'Sunspots', fontsize=14, fillColor=colors.red))

renderPDF.drawToFile(drawing, './output.pdf', 'Sunspots')