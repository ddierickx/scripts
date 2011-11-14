from time import mktime
import datetime
import time
import csv
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import dates
import matplotlib.ticker as ticker
from matplotlib.dates import MONDAY, SATURDAY
from matplotlib.dates import MonthLocator, WeekdayLocator, DateFormatter, MinuteLocator
import pickle

def run(file_in, file_out):
    results = {}
    f =  csv.reader(open(file_in, 'rb'), delimiter=';', quotechar='|', dialect='excel')
    lineno = 0

    try:
        for values in f:
            t = time.strptime(values[0], "%Y-%m-%d %H:%M:%S")
            v = int(values[4])

            if t in results:
                results[t] = results[t] + v
            else:
                results[t] = v

            lineno += 1
    except:
        print "Error at line: " + str(lineno+1)
	
    print(len(results))
    out = csv.writer(open(file_out, 'ab+'), delimiter=';', quotechar='|', dialect='excel')
    xs = []
    ys = []

    day_x = range(0,7)
    day_y = [0]*7;

    dayhours = [24 * [0] for x in range(0, 7)]
    
    for kv in sorted(results):
        dt = datetime.datetime.fromtimestamp(mktime(kv))
        #print str(dt.weekday()) + "-" + str(dt.hour) + ":" + str(results[kv])
        dayhours[dt.weekday()][dt.hour] = dayhours[dt.weekday()][dt.hour] + results[kv]
        xs.append(mktime(kv))
        ys.append(results[kv])
        day_y[dt.weekday()] += results[kv]
	out.writerow([time.strftime("%Y-%m-%d %H:%M:%S", kv), results[kv]])

    open("dayhours.txt", "wb").write(str(dayhours))

    def format_date(x, pos):
        return datetime.datetime.fromtimestamp(x).strftime('%Y-%m-%d %H:%M:%S')

    days = ("MO", "TU", "WE", "TH", "FR", "SA", "SU")

    

    def plot_weekday(title, weekdayno):
        N = 24
        ind = np.arange(N)
        width = 0.40
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.bar(range(0, 24), dayhours[weekdayno], width, color='g')
        ax.set_xticklabels(range(0, 24))
        ax.set_xticks(ind+(width / 2))

        for label in ax.get_xticklabels():
            label.set_rotation('horizontal')

        plt.ylabel("Checkins")
        plt.xlabel("Hour")
        plt.ylim((0,500))
        
        #ax.xaxis.set_major_locator(quarters)
        #ax.xaxis.set_major_formatter(monthsFmt)
        fig.suptitle(title)
        fig.savefig(title)

    def plot_all():
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.plot(xs, ys, 'o-')
        ax.xaxis.set_major_formatter(ticker.FuncFormatter(format_date))
        #ax.xaxis.set_major_locator(quarters)
        #ax.xaxis.set_major_formatter(monthsFmt)
        ax.autoscale_view()
        fig.autofmt_xdate()
        fig.savefig("all")

    def plot_weekdays():
        N = 7
        ind = np.arange(N)
        width = 0.40
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.bar(day_x, day_y, width, color='y')
        ax.set_xticks(ind+(width / 2))
        ax.set_xticklabels(days)

        for label in ax.get_xticklabels():
            label.set_rotation('horizontal')
        
        #ax.xaxis.set_major_locator(quarters)
        #ax.xaxis.set_major_formatter(monthsFmt)
        ax.autoscale_view()
        plt.show()

    plot_weekday('Mondays', 0)
    plot_weekday('Tuesdays', 1)
    plot_weekday('Wednesdays', 2)
    plot_weekday('Thursdays', 3)
    plot_weekday('Fridays', 4)
    plot_weekday('Saturdays', 5)
    #plot_weekdays()

def autolabel(rects):
    # attach some text labels
    for rect in rects:
        height = rect.get_height()
        ax.text(rect.get_x()+rect.get_width()/2., 1.05*height, '%d'%int(height),
                ha='center', va='bottom')

def gettimestamp(dt):
    return mktime(dt)


run("out.csv", "out_summarized.csv")
