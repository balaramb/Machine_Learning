import sys
from math import log as ln
from logsum import log_sum

dev_file = open(sys.argv[-4],'r')
trans_file = open(sys.argv[-3],'r')
emit_file = open(sys.argv[-2],'r')
prior_file = open(sys.argv[-1],'r')

class ForwardAlgorithm():
	"""Forward algorithm for HMMs"""
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
		self.prior_file.close()
			
		self.a = {}
		self.states = []
		for line in self.trans_file:
			temp = line.strip().split()
			hold = temp[0]
			self.states.append(hold)
			temp_dict = {}
			for i in temp:
				if ':' in i:
					temp_lst = i.split(':')
					temp_dict[temp_lst[0]] = float(temp_lst[1])
			self.a[hold] = temp_dict
		self.trans_file.close()
		numOfStates = len(self.a[self.states[0]])

		self.b = {}
		for line in self.emit_file:
			temp = line.strip().split()
			hold = temp[0]
			temp_dict = {}
			for i in temp:
				if ':' in i:
					temp_lst = i.split(':')
					temp_dict[temp_lst[0]] = float(temp_lst[1])
			self.b[hold] = temp_dict
		self.emit_file.close()
		numOfObservables = len(self.b[self.states[0]])
	
	def forward(self):
		for line in self.dev_file:
			curr_observable_sequence = line.strip().split()
			T = len(curr_observable_sequence)
			
			alpha_log = []
			
			init_alpha_log = {}
			for i in self.states:
				init_alpha_log[i] = ln(self.pie[i]) + ln(self.b[i][curr_observable_sequence[0]])
			alpha_log.append(init_alpha_log)
			
			counter = 1
			for curr_observable in curr_observable_sequence[1:]:
				temp_alpha_log = {}
				for i in self.states:
					hold = alpha_log[counter-1][self.states[0]] + ln(self.a[self.states[0]][i])
					for j in self.states[1:]:
						hold = log_sum(hold,(alpha_log[counter-1][j] + ln(self.a[j][i])))
					temp_alpha_log[i] = ln(self.b[i][curr_observable])+hold
				alpha_log.append(temp_alpha_log)
				counter += 1
			
			hold = alpha_log[T-1][self.states[0]]
			for k in self.states[1:]:
				hold = log_sum(hold,alpha_log[T-1][k])
			print(hold)

def main():
	frwd_algo = ForwardAlgorithm(dev_file,trans_file,emit_file,prior_file)
	frwd_algo.read_data()
	frwd_algo.forward()

if __name__ == '__main__':
    main()