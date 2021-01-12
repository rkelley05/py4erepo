name = input("Enter file:")
if len(name) < 1 : name = "mbox-short.txt"
handle = open(name)

di = dict()
for line in handle:
    if not line.startswith("From:"):
        continue
    else:
        line = line.rstrip()
        #print(line)
        words = line.split()
        #print(words)
        emails = words[1]
        print(emails)
        if emails in di:
            di[emails] = di[emails] + 1
        else:
            di[emails] = 1

print(di)
largest = -1
theword = None
for k,v in di.items():
    if v > largest:
        largest = v
        theword = k

print(theword, largest)
