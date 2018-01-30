import sys, math
from math import log
test = open(sys.argv[-1],'r')
train = open(sys.argv[-2],'r')

train_lst = []
test_lst = []

if 'politicians' in sys.argv[-1]:
	attribute_dic = {'y':1, 'n':0}
	label_dic = {'democrat':'+', 'republican':'-'}
elif 'education' in sys.argv[-1]:
	attribute_dic = {'A':1, 'notA':0}
	label_dic = {'A':'+', 'notA':'-'}
elif 'example'	in sys.argv[-1]:
	attribute_dic = {'y':1, 'n':0}
	label_dic = {'democrat':'+', 'republican':'-'}
elif 'music' in sys.argv[-1]:	
	attribute_dic = {'before1950':1, 'after1950':0, 'yes':1, 'no':0, 'fast':1, 'slow':0, 'morethan3min':1, 'lessthan3min':0}
	label_dic = {'yes':'+', 'no':'-'}
elif 'cars' in sys.argv[-1]:
	attribute_dic = {'expensive':1, 'cheap':0, 'high':1, 'low':0, 'Two':1, 'MoreThanTwo':0, 'large':1, 'small':0, 'yes':1, 'no':0}
	label_dic = {'yes':'+', 'no':'-'}

master_node = []
attributes_in_order = []

j=0
for line in train:
	if j == 0:
		attr_names = line.split(',')
		attr_names = [vim.rstrip().lstrip() for vim in attr_names]
	if j!=0:
		temp = line.split(',')
		label_hold = temp[-1].rstrip()
		label_hold = [label_dic[label_hold]]
		temp = [attribute_dic[i] for i in temp[0:len(temp)-1] if i in attribute_dic]
		temp = temp+label_hold
		train_lst.append(temp)
	j=j+1
train.close()

pos_count = 0
neg_count = 0
for i in train_lst:
	if i[-1] == '+':
		pos_count = pos_count+1
	if i[-1] == '-':
		neg_count = neg_count+1

print('['+str(pos_count)+'+/'+ str(neg_count) + '-]')
stopit = 0
	
j=0
for line in test:
	if j!=0:
		temp = line.split(',')
		label_hold = temp[-1].rstrip()
		label_hold = [label_dic[label_hold]]
		temp = [attribute_dic[i] for i in temp[0:len(temp)-1] if i in attribute_dic]
		temp = temp+label_hold
		test_lst.append(temp)
	j=j+1
test.close()

def entropy_left(content):
	attr_num = len(content[0])-1
	ex_num = len(content)
	entropy_left = []
	for v in range(attr_num):
		zero_pos = 0
		zero_neg = 0
		one_pos = 0
		one_neg = 0
		for u in content:
			if u[v]==0 and u[-1]=='+':
				zero_pos = zero_pos+1
			if u[v]==1 and u[-1]=='+':
				one_pos = one_pos+1
			if u[v]==0 and u[-1]=='-':
				zero_neg = zero_neg+1
			if u[v]==1 and u[-1]=='-':
				one_neg = one_neg+1
		prob_attr_zero = (zero_neg+zero_pos)/float(ex_num)
		prob_attr_one = (one_neg+one_pos)/float(ex_num)
		a = one_neg/float(one_neg+one_pos)
		b = one_pos/float(one_neg+one_pos)
		c = zero_pos/float(zero_neg+zero_pos)
		d = zero_neg/float(zero_neg+zero_pos)
		if a==0:
			k1 = 0
		else:
			k1 = a*log(1.0/a,2)
		if b==0:
			k2 = 0
		else:
			k2 = b*log(1.0/b,2)
		if c==0:
			k3 = 0
		else:
			k3 = c*log(1.0/c,2)
		if d==0:
			k4 = 0
		else:
			k4 = d*log(1.0/d,2)
		surprise_label_zero = k3+k4
		surprise_label_one = k1+k2
		final = prob_attr_zero*surprise_label_zero + prob_attr_one*surprise_label_one
		entropy_left.append(final)
	return entropy_left
	
def actual_entropy(content):
	num_pos = 0
	num_neg = 0
	for u in content:
		if u[-1] == '+':
			num_pos = num_pos+1
		if u[-1] == '-':
			num_neg = num_neg+1
	t1 = num_pos/float(num_neg+num_pos)
	t2 = num_neg/float(num_neg+num_pos)
	if t1 == 0:
		lh = 0
	else:
		lh = t1*log(1/t1,2)
	if t2 == 0:
		rh = 0
	else:
		rh = t2*log(1/t2,2)	
	return lh+rh

def update_attr_usage_status(attr_chosen):
	attr_usage_status[attr_chosen] = 100

def update_content(content,attr_usage_status):
	for j in range(len(attr_usage_status)-1):
		if attr_usage_status[j] == 100:
			for i in content:
				del i[j]
	return content

def LH_content(content,attr_chosen):
	updated_content_for_left = []
	for u in content:
		if u[attr_chosen] == 0:
			pin = u[0:attr_chosen]+u[attr_chosen+1:]
			updated_content_for_left.append(pin)
	return updated_content_for_left

def RH_content(content,attr_chosen):
	updated_content_for_right = []
	for u in content:
		if u[attr_chosen] == 1:
			pin = u[0:attr_chosen]+u[attr_chosen+1:]
			updated_content_for_right.append(pin)
	return updated_content_for_right

def add_node_to_master(a,b,c,d,e,f,g,h,i,j,k):
	master_node.append(list([a,b,c,d,e,f,g,h,i,j,k]))
	
def pick_next_node():
	if (all_retire(master_node)):
		create_tree()
		print ('error(train): '+ str(evaluate_error(train_lst)))
		print ('error(test): '+ str(evaluate_error(test_lst)))
		sys.exit()		
		
	current_max_depth = 0
	for i in master_node:
		if i[0]>current_max_depth and i[-1] == 0:
			current_max_depth = i[0]
	
	j = -1
	for i in master_node:
		j=j+1
		if i[0] == current_max_depth and i[2] == 0 and i[3] == 0 and i[-1] == 0:
			return [i,j]
		elif i[0] == current_max_depth and i[2] != 0 and i[3] == 0 and i[-1] == 0:
			return [i,j]

depth = 0
left_status = 0
right_status = 0
retire = 0
parent = -1
lh_child = 0
rh_child = 0
attr_available = attr_names
cause_attr = 'root'
nory = 'null'
add_node_to_master(depth,train_lst,left_status,right_status,parent,lh_child,rh_child,attr_available,cause_attr,nory,retire)

itsindex = 0
times_entry = 0

def posneg(a):
	numpos = 0
	numneg = 0
	for i in a:
		if i[-1] == '+':
			numpos+=1
		if i[-1] == '-':
			numneg+=1

	return '['+str(numpos)+'+/'+str(numneg)+'-]'

def check_All():
	#retire node if depth is 2
	for i in master_node:
		if i[0] == 2:
			i[-1] = 1
	#figure what this is
	for i in master_node:
		if i[2]!=0 and i[3]!=0:
			i[-1] = 1
	#retire node if all labels are same
	for i in master_node:
		numpos = 0
		numneg = 0
		for k in i[1]:
			if k[-1] == '+':
				numpos+=1
			if k[-1] == '-':
				numneg+=1
		if numpos==0 or numneg==0:
			i[-1] = 1
		if i[0] == 2:
			i[-1] = 1
	#retire parent if children retired
	for i in master_node:
		child1_status = master_node[i[5]][-1]
		child2_status = master_node[i[6]][-1]
		if child1_status == 1 and child2_status == 1:
			i[-1] = 1
			
	for i in master_node:
		child1_status = master_node[i[5]][-1]
		child2_status = master_node[i[6]][-1]
		if child1_status == 1 and child2_status == 1:
			i[-1] = 1
	
	for i in master_node:
		child1_status = master_node[i[5]][-1]
		child2_status = master_node[i[6]][-1]
		if child1_status == 1 and child2_status == 1:
			i[-1] = 1

def create_tree():
	parent1 = []
	children1 = []
	for k in master_node:
		if k[0] == 0:
			parent1.append(k)
	for t in parent1:
		children1.append(master_node[t[5]])
		children1.append(master_node[t[6]])

	str1 = children1[0][8].lstrip().rstrip() + ' = n: ' + posneg(children1[0][1])
	str4 = children1[1][8].lstrip().rstrip() + ' = y: ' + posneg(children1[1][1])
	
	children2 = []
	for t in children1:
		children2.append(master_node[t[5]])
		children2.append(master_node[t[6]])
	
	str2 = '| ' + children2[0][8].lstrip().rstrip() + ' = n: ' + posneg(children2[0][1])
	str3 = '| ' + children2[1][8].lstrip().rstrip() + ' = y: ' + posneg(children2[1][1])
	str5 = '| ' + children2[2][8].lstrip().rstrip() + ' = n: ' + posneg(children2[2][1])
	str6 = '| ' + children2[3][8].lstrip().rstrip() + ' = y: ' + posneg(children2[3][1])
	
	print str1
	if children2[0][8] != 'root':
		print str2
	if children2[1][8] != 'root':
		print str3
	print str4
	if children2[2][8] != 'root':
		print str5
	if children2[3][8] != 'root':
		print str6
	
def all_retire(node_collection):
	x = True
	for i in node_collection:
		if i[-1] == 0:
			x = False
	return x

def make_decision(node):
	content = node[1]
	numpos = 0
	numneg = 0
	for i in content:
		if i[-1] == '+':
			numpos += 1
		if i[-1] == '-':
			numneg += 1
	if numpos>=numneg:
		return '+'
	else:
		return '-'

def evaluate_error(lst):
	data = []
	label = []
	prediction = []
	#separate out data and labels
	for i in lst:
		temp = i[0:len(i)-1]
		data.append(temp)
		label.append(i[-1])
	
	for i in data:
		first_decision_attr_name = master_node[1][8]
		first_decision_attr_index = attr_names.index(first_decision_attr_name)
		data_value1 = i[first_decision_attr_index]
		if data_value1 == 1:
			deciding_node1 = master_node[2]
		if data_value1 == 0:
			deciding_node1 = master_node[1]
		if deciding_node1[5] == 0:
			#change needed here also??
			prediction.append(make_decision(deciding_node1))
			#print (prediction)
		else:
			deciding_node2_l = master_node[deciding_node1[5]]
			deciding_node2_r = master_node[deciding_node1[6]]
			second_decision_attr_name = deciding_node2_l[8]
			second_decision_attr_index = attr_names.index(second_decision_attr_name)
			if i[second_decision_attr_index] == 0:
				deciding_node2 = deciding_node2_l
			if i[second_decision_attr_index] == 1:
				deciding_node2 = deciding_node2_r
			prediction.append(make_decision(deciding_node2))
	
	counter = -1
	error_number = 0
	for i in label:
		counter+=1
		if i != prediction[counter]:
			error_number+=1
	return float(error_number)/len(label)

def process_node(node_id,itsindex,times_entry):
	if node_id[2] == 0:
		SH = entropy_left(node_id[1])
		SE = actual_entropy(node_id[1])
		if SE-min(SH) >= 0.1:
			attr_chosen = SH.index(min(SH))
			hold_cause = node_id[7][attr_chosen]
			hold_available = [i for i in node_id[7] if i!=hold_cause]
			temp1 = LH_content(node_id[1],attr_chosen)
			temp2 = RH_content(node_id[1],attr_chosen)
			next_child_index = len(master_node)
			if len(temp1[0]) == 1:
				add_node_to_master(node_id[0]+1,temp1,0,0,itsindex,0,0,hold_available,hold_cause,'n',1)
				add_node_to_master(node_id[0]+1,temp2,0,0,itsindex,0,0,hold_available,hold_cause,'y',1)
				node_id[-1] = 1
			else:
				add_node_to_master(node_id[0]+1,temp1,0,0,itsindex,0,0,hold_available,hold_cause,'n',0)
				add_node_to_master(node_id[0]+1,temp2,0,0,itsindex,0,0,hold_available,hold_cause,'y',0)

			node_id[2] = 1
			node_id[5] = next_child_index
			node_id[6] = next_child_index+1
		else:
			node_id[-1] = 1
		
	elif node_id[3] == 0:
		SH = entropy_left(node_id[1])
		SE = actual_entropy(node_id[1])
		if SE-min(SH) >= 0.1:
			attr_chosen = SH.index(min(SH))
			hold_cause = node_id[7][attr_chosen]
			hold_available = [i for i in node_id[7] if i!=hold_cause]
			temp1 = LH_content(node_id[1],attr_chosen)
			temp2 = RH_content(node_id[1],attr_chosen)
			next_child_index = len(master_node)
			if len(temp1[0]) == 1:
				add_node_to_master(node_id[0]+1,temp1,0,0,itsindex,0,0,hold_available,hold_cause,'n',1)
				add_node_to_master(node_id[0]+1,temp2,0,0,itsindex,0,0,hold_available,hold_cause,'y',1)
				node_id[-1] = 1
			else:
				add_node_to_master(node_id[0]+1,temp1,0,0,itsindex,0,0,hold_available,hold_cause,'n',0)
				add_node_to_master(node_id[0]+1,temp2,0,0,itsindex,0,0,hold_available,hold_cause,'y',0)

			node_id[3] = 1
			node_id[5] = next_child_index
			node_id[6] = next_child_index+1
		else: 
			node_id[-1] = 1
	check_All()
	[next_node,itsindex] = pick_next_node()
	if (next_node == master_node[0] and times_entry>0):
		create_tree()
		print ('error(train): '+ str(evaluate_error(train_lst)))
		print ('error(test): '+ str(evaluate_error(test_lst)))
		sys.exit()
	times_entry = times_entry + 1
	process_node(next_node,itsindex,times_entry)

process_node(master_node[0],0,times_entry)