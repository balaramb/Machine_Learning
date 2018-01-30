import sys
from math import log as ln

dev_file = open(sys.argv[-4],'r')
trans_file = open(sys.argv[-3],'r')
emit_file = open(sys.argv[-2],'r')
prior_file = open(sys.argv[-1],'r')

class ViterbiAlgorithm():
	"""Viterbi algorithm for HMMs"""
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
		self.trans_file.close()
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
		self.emit_file.close()
		numOfObservables = len(self.b[self.states[0]])

	def viterbi(self):
		for line in self.dev_file:
			curr_observable_sequence = line.strip().split()
			T = len(curr_observable_sequence)
			
			viterbi_log = []
			collection = []
			
			temp_best_path_indi = {}
			temp_viterbi_log = {}
			for i in self.states:
				temp_viterbi_log[i] = ln(self.pie[i]) + ln(self.b[i][curr_observable_sequence[0]])
				temp_best_path_indi[i] = [i]
			viterbi_log.append(temp_viterbi_log)
			collection.append(temp_best_path_indi)
			
			for curr_observable in curr_observable_sequence[1:]:
				temp_viterbi_log = {}
				#For each state i, find the state j that maximizes value
				best_j = {}
				temp_best_path_indi = {}
				for i in self.states:
					minimum = -1000000
					for j in self.states:
						value = viterbi_log[-1][j] + ln(self.a[j][i]) + ln(self.b[i][curr_observable])
						if value > minimum:
							minimum = value
							best_j[i] = j
					temp_viterbi_log[i] = minimum
					temp_best_path_indi[i] = collection[-1][best_j[i]]+[i]
				viterbi_log.append(temp_viterbi_log)
				collection.append(temp_best_path_indi)
			
			minimum = -1000000
			for i in self.states:
				if viterbi_log[-1][i] > minimum:
					minimum = viterbi_log[-1][i]
					curr_best = i
			result_lst = collection[-1][curr_best]
			
			to_be_printed = ''
			for t in range(T):
				to_be_printed += curr_observable_sequence[t] + '_' + result_lst[t] + ' '
			print (to_be_printed)

def main():
	vtb_algo = ViterbiAlgorithm(dev_file,trans_file,emit_file,prior_file)
	vtb_algo.read_data()
	vtb_algo.viterbi()

if __name__ == '__main__':
    main()