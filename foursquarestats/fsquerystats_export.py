import time
import csv
	
def run(file_in, file_out):
    results = {}
    f =  csv.reader(open(file_in, 'rb'), delimiter=';', quotechar='|', dialect='excel')

    for values in f:
        t = values[0]
        v = int(values[4])

        if t in results:
            results[t] = results[t] + v
        else:
            results[t] = v

    out = csv.writer(open(file_out, 'ab+'), delimiter=';', quotechar='|', dialect='excel')

    for kv in results:
        out.writerow([kv, results[kv]])
        


run("queryresults.csv", "queryresults_summarized.csv")
