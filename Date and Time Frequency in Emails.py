name = input("Enter file:")
if len(name) < 1 : name = "mbox-short.txt"
handle = open(name)

di = dict()
for line in handle:
    if not line.startswith("From"):
        continue
    else:
        line = line.rstrip()
        words = line.split()
        try:
            time = words[5]
            time = time.split(":")
            hour = time[0]
            #if hour in di:
            #    di[hour] = di[hour] + 1
            #else:
            #    di[hour] = 1
            di[hour] = di.get(hour,0) + 1
        except:
            continue

tmp = sorted([(v,k) for (k,v) in di.items()])
#tmp = list()
#for k,v in di.items():
#    times = (k,v)
#    tmp.append(times)
#tmp = sorted(tmp)

for k,v in tmp:
    print(k,v)
