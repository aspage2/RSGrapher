import tkFileDialog
import matplotlib.pyplot as pt
import numpy as np

def get_asc_meta (fh):
	fh.seek(0)
	title = fh.readline().strip()
	if (title != "DASYLab - V 12.00.01"):
		return None
	meta = {"Worksheet name":"", "Recording date":"", "Block length":"", "Delta":"", "Number of channels":""}
	for i in range (5):
		items = map (str.strip, fh.readline().strip().split(":",1))
		if (len(items)!=2 or items[0] not in meta.keys() or meta[items[0]] != ""):
			return None
		meta[items[0]] = items[1]

	if (fh.readline().strip() != "Measurement time[s]	Disp [in]	Load [lb]"):
		return None
	
	return meta

def generate_csv (ascfile, outfilename):
	ascfile.seek(0)
	for i in range (7):
		ascfile.readline()
	outfile = open (outfilename, "w")
	line = ascfile.readline().strip()
	while (line != ""):
		outfile.writelines((line.replace("\t",",") + "\n"))
		line = ascfile.readline().strip()
	outfile.close()

def generate_graph(ascfile):
	ascfile.seek(0)
	for i in range(7):
		ascfile.readline()
	x=[]
	y=[]
	line = ascfile.readline().strip()
	count = 0
	while (line != ""):
		count += 1
		if (count % 100 == 0):
			print ("Added " + str(count) + " data points")
		t, d, l = line.split("\t")
		x.append (float(d))
		y.append (float(l))
		line = ascfile.readline().strip()
	pt.plot (x, y)
	pt.show()
"""
fh = tkFileDialog.askopenfile (title="Open ASC File")
meta = get_asc_meta (fh)
if (meta == None):
	print ("An error occured. Did you select an ASC file?")
else:
	generate_graph(fh)
"""
