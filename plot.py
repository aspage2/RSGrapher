import sys

def getascmeta (fh)
	fh.seek(0)
	title = fh.readline().strip()
	if (title != "DASYLab - V 12.00.01")
		return None
	meta = {"Worksheet name":"", "Recording date":"", "Block length":"", "Delta":"", "Number of channels":""}
	for i in range (5):
		items = map (str.strip, fh.readline().strip().split(":",1))
		if (len(items)!=2 or items[0] not in meta.keys() or meta[items[0]] != ""):
			return None
		meta[items[0]] = items[1]
	
