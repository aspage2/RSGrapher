import random

from app.util.search import lin_nearest_neighbor

vals = sorted([random.random()*1000 for i in range(1000)])

ind = lin_nearest_neighbor(float(input("Choose: ")), vals)

print("BEST MATCH: ",ind, vals[ind])

for x in range(ind-5 if  ind-5 >= 0 else 0, ind+5 if ind+5 < len(vals) else  len(vals)-1):
    print(vals[x])