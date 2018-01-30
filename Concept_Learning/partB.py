import sys, itertools

test = open(sys.argv[-1],'r')
train = open("4Cat-Train.labeled",'r')

gender = ['Male', 'Female']
age = ['Young', 'Old']
student = ['Yes', 'No']
prev = ['Yes', 'No']
label = ['low', 'high']

IS = []
for i in gender:
	for j in age:
		for k in student:
			for l in prev:
				IS.append([i,j,k,l])

concept_space = [list(k) for k in itertools.product([0, 1], repeat=16)]

j=0
train_lst = []
for line in train:
	train_lst.append(line.split())
	train_lst[j].remove('Gender')
	train_lst[j].remove('Age')
	train_lst[j].remove('Student?')
	train_lst[j].remove('PreviouslyDeclined?')
	train_lst[j].remove('Risk')
	j=j+1
train.close()

track = []
for i in train_lst:
	hold = -1
	for j in IS:
		hold = hold+1
		if i[:-1] == j:
			track.append([hold, i[-1]])
			
for i in track:
	if i[1] == 'high':
		i[1] = 1
	if i[1] == 'low':
		i[1] = 0
	
for i in concept_space:
	for j,k in track:
		if i[j] != k:
			i.append('drop');

Final_VS = []
for i in concept_space:
	if i[-1] != 'drop':
		Final_VS.append(i)
		
print 2**4
print 2**16
print len(Final_VS)

j=0
test_lst = []
for line in test:
	test_lst.append(line.split())
	test_lst[j].remove('Gender')
	test_lst[j].remove('Age')
	test_lst[j].remove('Student?')
	test_lst[j].remove('PreviouslyDeclined?')
	test_lst[j].remove('Risk')
	j=j+1
test.close()

track2 = []
for i in test_lst:
	hold = -1
	for j in IS:
		hold = hold+1
		if i[:-1] == j:
			track2.append(hold)

highlow = []
for i in track2:
	high = 0
	low = 0
	for j in Final_VS:
		if j[i] ==  1:
			high = high+1
		if j[i] ==  0:
			low = low+1
	print str(high)+' '+str(low)