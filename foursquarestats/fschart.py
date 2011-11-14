import csv
import time
from pygooglechart import StackedHorizontalBarChart, StackedVerticalBarChart, \
    GroupedHorizontalBarChart, GroupedVerticalBarChart, Axis

width, height = 250, 150

f =  csv.reader(open('out_summarized.csv', 'rb'), delimiter=';', quotechar='|', dialect='excel')

xs = []
ys = []
labels = []

i = 0

for values in f:
	xs.append(i)
	labels.append(time.strptime(str(values[0]), '%Y-%m-%d %H:%M:%S'))
	ys.append(int(values[1]))
	i += 1
	
chart = StackedVerticalBarChart(width, height, x_range=(0, len(xs)))
chart.set_axis_labels(Axis.BOTTOM, labels)
chart.auto_scale = True
chart.set_bar_width(10)
chart.set_colours(['00ff00', 'ff0000'])
chart.add_data(ys)
chart.download('bar-horizontal-stacked.png')