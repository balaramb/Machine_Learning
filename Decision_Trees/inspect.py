import sys, math
from math import log
train = open(sys.argv[-1],'r')

label_lst = []

j=0
for line in train:
	if j!=0:
		temp = line.split(',')
		label_lst.append(temp[-1].rstrip())
	j=j+1
train.close()

available_attributes = list(set(label_lst))

counter = []
for i in available_attributes:
	temp = 0
	for j in label_lst:
		if i==j:
			temp+=1
	counter.append(temp)

freq_label = available_attributes[counter.index(max(counter))]

mistakes = 0
for i in label_lst:
	if i != freq_label:
		mistakes+=1

actual_entropy = 0
for i in counter:
	temp = float(i)/len(label_lst)
	actual_entropy += temp*log(1/temp,2)

print 'entropy: '+str(actual_entropy)
print 'error: '+str(float(mistakes)/len(label_lst))