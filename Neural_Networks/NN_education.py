import sys, math
import numpy as np

train_attr_file = sys.argv[-3]
train_label_file = sys.argv[-2]
test_attr_file = sys.argv[-1]

class NeuralNetwork():
	"""Neural Network with one hidden layer"""
	def __init__(self,train_attr_name,train_label_name,test_attr_name,yeta = 0.005):
		self.yeta = yeta
		self.train_attr_name = train_attr_name
		self.train_label_name = train_label_name
		self.test_attr_name = test_attr_name

	def read_data(self):
		train_attr = open(self.train_attr_name,'r')
		train_label = open(self.train_label_name,'r')
		test_attr = open(self.test_attr_name,'r')
		
		#READ TRAINING DATA
		#training features
		train_attr_lst = []
		j=0
		for line in train_attr:
			if j == 0:
				self.attr_names = line.split(',')
				self.attr_names = [vim.rstrip().lstrip() for vim in self.attr_names]
			if j!=0:
				temp = line.split(',')
				temp = [mi.rstrip().lstrip() for mi in temp]
				temp = [float(ni) for ni in temp]
				train_attr_lst.append(temp)
			j=j+1
		train_attr.close()
		train_attr_matrix = np.array(train_attr_lst)
		self.train_attr_matrix_normalized = train_attr_matrix/100.0												#feature-scaling

		#training labels
		train_label_lst = []
		j=0
		for line in train_label:
			temp = line.rstrip().lstrip()
			temp = float(temp)
			temp = [temp]
			train_label_lst.append(temp)
		train_label.close()
		self.train_label_matrix = np.array(train_label_lst)
		self.train_label_matrix_normalized = self.train_label_matrix/100.0										#feature-scaling


		#READ TEST DATA
		#test features
		test_attr_lst = []
		j=0
		for line in test_attr:
			if j!=0:
				temp = line.split(',')
				temp = [mi.rstrip().lstrip() for mi in temp]
				temp = [float(ni) for ni in temp]
				test_attr_lst.append(temp)
			j=j+1
		test_attr.close()
		test_attr_matrix = np.array(test_attr_lst)
		self.test_attr_matrix_normalized = test_attr_matrix/100.0												#feature-scaling

	def initialize_wb(self):
		hidden_units_num = len(self.attr_names)-1
		#initialize weights
		self.Theta1 = (2*np.random.random([len(self.attr_names),hidden_units_num])-1).T
		self.Theta2 = (2*np.random.random([hidden_units_num,1])-1).T
		#initialize biases
		self.b1 = 0.1
		self.b2 = -0.1

	def sigmoid_func(self,number):
		return 1.0/(1.0+np.exp(-number))

	def check_on_train(self):
		a1 = self.train_attr_matrix_normalized																	#400x6
		z2 = np.dot(a1,self.Theta1.T)+self.b1																	#400x4
		a2 = self.sigmoid_func(z2)																				#400x4
		z3 = np.dot(a2,self.Theta2.T)+self.b2																	#400x1
		a3 = self.sigmoid_func(z3)																				#400x1
		prediction = a3*100.0																					#400x1
		error = abs(prediction - self.train_label_matrix)
		return np.sum(error)

	def test(self):
		error = 0
		a1 = self.test_attr_matrix_normalized																	#400x6
		z2 = np.dot(a1,self.Theta1.T)+self.b1																	#400x4
		a2 = self.sigmoid_func(z2)																				#400x4
		z3 = np.dot(a2,self.Theta2.T)+self.b2																	#400x1
		a3 = self.sigmoid_func(z3)																				#400x1
		prediction = a3*100.0																					#400x1
		for i in range(len(prediction)):
			print(str(round(prediction[i,0])))
		return 0

	def backProp(self):
		a1 = self.train_attr_matrix_normalized																	#400x6
		z2 = np.dot(a1,self.Theta1.T)+self.b1																	#400x4
		a2 = self.sigmoid_func(z2)																				#400x4
		z3 = np.dot(a2,self.Theta2.T)+self.b2																	#400x1
		a3 = self.sigmoid_func(z3)																				#400x1
		er3 = (a3-self.train_label_matrix_normalized)*(a3*(1-a3))												#400x1
		er2 = er3.dot(self.Theta2)*(a2*(1-a2))																	#400x1
		Theta2_grad = self.yeta*a2.T.dot(er3)
		Theta1_grad = self.yeta*self.train_attr_matrix_normalized.T.dot(er2)
		Theta1 = self.Theta1-Theta1_grad.T
		Theta2 = self.Theta2-Theta2_grad.T
		self.b1 = self.b1 - self.yeta*np.sum(er2, axis=0)
		self.b2 = self.b2 - self.yeta*np.sum(er3, axis=0, keepdims=True)

	def train(self):
		counter = 0
		#carrying out backprop for 5000 iterations
		for i in range(5000):
			self.backProp()
			counter += 1
			curr_train_error = self.check_on_train();
			print(curr_train_error)
		print ('TRAINING COMPLETED! NOW PREDICTING.')

def main():
	nn = NeuralNetwork(train_attr_name = train_attr_file, train_label_name = train_label_file, test_attr_name = test_attr_file)
	nn.read_data()
	nn.initialize_wb()
	nn.train()
	nn.test()

if __name__ == '__main__':
    main()