import sys
from math import log as ln
from logsum import log_sum

dev_file = open(sys.argv[-4],'r')
trans_file = open(sys.argv[-3],'r')
emit_file = open(sys.argv[-2],'r')
prior_file = open(sys.argv[-1],'r')

class BackwardAlgorithm():
	"""Backward algorithm for HMMs"""
	def __init__(self,dev_file,trans_file,emit_file,prior_file):
		self.dev_file = dev_file
		self.trans_file = trans_file
		self.emit_file = emit_file
		self.prior_file = prior_file
	
	def read_data(self):
		self.pie = {}
		for line in prior_file:
			temp = line.strip().split()
			self.pie[temp[0]] = float(temp[1])
		prior_file.close()

		self.a = {}
		self.states = []
		for line in trans_file:
			temp = line.strip().split()
			hold = temp[0]
			self.states.append(hold)
			temp_dict = {}
			for i in temp:
				if ':' in i:
					temp_lst = i.split(':')
					temp_dict[temp_lst[0]] = float(temp_lst[1])
			self.a[hold] = temp_dict
		trans_file.close()
		numOfStates = len(self.a[self.states[0]])

		self.b = {}
		for line in emit_file:
			temp = line.strip().split()
			hold = temp[0]
			temp_dict = {}
			for i in temp:
				if ':' in i:
					temp_lst = i.split(':')
					temp_dict[temp_lst[0]] = float(temp_lst[1])
			self.b[hold] = temp_dict
		emit_file.close()
		numOfObservables = len(self.b[self.states[0]])

	def backward(self):
		for line in self.dev_file:
			curr_observable_sequence = line.strip().split()
			T = len(curr_observable_sequence)
			
			beta_log = [0]*T
			
			init_beta_log = {}
			for i in self.states:
				init_beta_log[i] = 0
			beta_log[T-1] = init_beta_log
			
			for t in range(T-2,-1,-1):
				temp_beta_log = {}
				for i in self.states:
					hold = beta_log[t+1][self.states[0]] + ln(self.a[i][self.states[0]]) + ln(self.b[self.states[0]][curr_observable_sequence[t+1]])
					for j in self.states[1:]:
						hold = log_sum(hold, beta_log[t+1][j] + ln(self.a[i][j]) + ln(self.b[j][curr_observable_sequence[t+1]]))
					temp_beta_log[i] = hold
				beta_log[t] = temp_beta_log

			hold = ln(self.pie[self.states[0]]) + ln(self.b[self.states[0]][curr_observable_sequence[0]]) + beta_log[0][self.states[0]]
			for i in self.states[1:]:
				hold = log_sum(hold,ln(self.pie[i]) + ln(self.b[i][curr_observable_sequence[0]]) + beta_log[0][i])
			print (hold)
			
def main():
	back_algo = BackwardAlgorithm(dev_file,trans_file,emit_file,prior_file)
	back_algo.read_data()
	back_algo.backward()

if __name__ == '__main__':
    main()