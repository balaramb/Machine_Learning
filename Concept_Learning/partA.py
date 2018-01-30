import sys
test = open(sys.argv[-1],'r')
train = open("9Cat-Train.labeled",'r')
dev = open("9Cat-Dev.labeled",'r')

train_lst = []
dev_lst = []
test_lst = []

H = [None,None,None,None,None,None,None,None,None]

print 2**9
print len(str(2**(2**9)))
print (3**9)+1
print (3**10)+1
print 4*(3**8)+1

j=0
for line in train:
	train_lst.append(line.split())
	train_lst[j].remove('Gender')
	train_lst[j].remove('Age')
	train_lst[j].remove('Student?')
	train_lst[j].remove('PreviouslyDeclined?')
	train_lst[j].remove('HairLength')
	train_lst[j].remove('Employed?')
	train_lst[j].remove('TypeOfColateral')
	train_lst[j].remove('FirstLoan')
	train_lst[j].remove('LifeInsurance')
	train_lst[j].remove('Risk')
	j=j+1
train.close()

j=0
for line in dev:
	dev_lst.append(line.split())
	dev_lst[j].remove('Gender')
	dev_lst[j].remove('Age')
	dev_lst[j].remove('Student?')
	dev_lst[j].remove('PreviouslyDeclined?')
	dev_lst[j].remove('HairLength')
	dev_lst[j].remove('Employed?')
	dev_lst[j].remove('TypeOfColateral')
	dev_lst[j].remove('FirstLoan')
	dev_lst[j].remove('LifeInsurance')
	dev_lst[j].remove('Risk')
	j=j+1
dev.close()

j=0
for line in test:
	test_lst.append(line.split())
	test_lst[j].remove('Gender')
	test_lst[j].remove('Age')
	test_lst[j].remove('Student?')
	test_lst[j].remove('PreviouslyDeclined?')
	test_lst[j].remove('HairLength')
	test_lst[j].remove('Employed?')
	test_lst[j].remove('TypeOfColateral')
	test_lst[j].remove('FirstLoan')
	test_lst[j].remove('LifeInsurance')
	test_lst[j].remove('Risk')
	j=j+1
test.close()

f = open('partA6.txt','w')
count = 0
for i in train_lst:
	count = count+1
	if i[-1] == 'high':
		for j in range(9):
			if H[j] == None:
				H[j] = i[j]
			elif H[j] != i[j]:
				 H[j] = '?'
	if count%30 == 0:
		z = '\t'.join(H)+'\n'
		f.write(z)
f.close()

check = []
j=0
for i in H:
	if i != '?':
		check.append(j)
	j = j+1
length = len(check)

lamb = 0
good_predicts = 0
for i in dev_lst:
	lamb = lamb+1
	actual = i[-1]
	count=0
	for j in range(9):
		if H[j] != '?' and H[j] == i[j]:
			count = count+1
	if count == length:
		predict = 'high'
	else:
		predict = 'low'
	
	if predict == actual:
		good_predicts = good_predicts+1
print 1-(good_predicts/100.0)

lamb = 0
good_predicts = 0
for i in test_lst:
	count=0
	for j in range(9):
		if H[j] != '?' and H[j] == i[j]:
			count = count+1
	if count == length:
		print 'high'
	else:
		print 'low'