import sys
from collections import Counter
from math import log as ln

class NaiveBayesClassifier():
	"""NaiveBayesClassifier"""
	def __init__(self, nStopWords = 0, smoothing = 1, topWords = 0, topWordsLogOdds = 0):
		self.nStopWords = nStopWords
		self.smoothing = smoothing
		self.topWords = topWords
		self.topWordsLogOdds = topWordsLogOdds
	
	######################################################
	# TRAINING
	######################################################
	def train(self,train_docs):
		#initialize empty lists
		train_docs_lst = []
		train_con_docs_lst = []
		train_lib_docs_lst = []

		#read in all filenames
		for line in train_docs:
			filename = line.rstrip().lstrip()
			train_docs_lst.append(filename)
			#separate out files as liberal and conservative files
			if filename[0:3] == 'lib':
				train_lib_docs_lst.append(filename)
			if filename[0:3] == 'con':
				train_con_docs_lst.append(filename)
		train_docs.close()

		#calculate the probability of a file being liberal or conservative
		self.prob_con = float(len(train_con_docs_lst))/(len(train_lib_docs_lst) + len(train_con_docs_lst))
		self.prob_lib = float(len(train_lib_docs_lst))/(len(train_lib_docs_lst) + len(train_con_docs_lst))

		#from each conservative file, read in all the words
		self.con_word_lst = []
		for filename in train_con_docs_lst:
			curr_file = open(filename,'r')
			for word in curr_file:
				self.con_word_lst.append(word.lower().lstrip().rstrip())
			curr_file.close()

		#from each liberal file, read in all the words
		self.lib_word_lst = []
		for filename in train_lib_docs_lst:
			curr_file = open(filename,'r')
			for word in curr_file:
				self.lib_word_lst.append(word.lower().lstrip().rstrip())
			curr_file.close()

		#complete list of words from entire content
		self.word_lst = self.lib_word_lst + self.con_word_lst

		#find the vocabulary of the complete content
		Vocabulary = set(self.word_lst)

		#find the number of times each word appears in the liberal content
		self.lib_wordcount = {}
		self.lib_wordcount = dict(Counter(self.lib_word_lst))

		#find the number of times each word appears in the conservative content
		self.con_wordcount = {}
		self.con_wordcount = dict(Counter(self.con_word_lst))

		#keep a register for all words in one place
		self.Mastercount = {}
		Mastercount_combined = {}
		for i in Vocabulary:
			self.Mastercount[i] = {'con':0, 'lib':0}
			if i in self.lib_wordcount:
				self.Mastercount[i]['lib'] = self.lib_wordcount[i]
			if i in self.con_wordcount:
				self.Mastercount[i]['con'] = self.con_wordcount[i]
			Mastercount_combined[i] = self.Mastercount[i]['con'] + self.Mastercount[i]['lib']

		#implementation for nStopWords
		if self.nStopWords>0:
			temp_Master_count_combined = sorted(Mastercount_combined.items(), key=lambda x: x[1], reverse = True)
			totalTop = temp_Master_count_combined[0:self.nStopWords]

			#get rid of trivial words that occur most frequently(#nStopWords)
			for i in totalTop:
				word = i[0]
				del self.Mastercount[word]
				self.lib_word_lst = [x for x in self.lib_word_lst if x != word]
				self.con_word_lst = [x for x in self.con_word_lst if x != word]
		
		#implementation for topWords
		if self.topWords == 1:
			temp_lib = sorted(self.lib_wordcount.items(), key=lambda x: x[1], reverse = True)
			temp_con = sorted(self.con_wordcount.items(), key=lambda x: x[1], reverse = True)
			
			#find top 20 most frequently words
			lib20 = temp_lib[0:20]
			con20 = temp_con[0:20]

			#print word and word probability alongside
			lib_num = 0
			for i in lib20:
				lib_num += 1
				word = i[0]
				n_lib = self.lib_wordcount[word]
				n = len(self.lib_word_lst)
				temp = float(n_lib+1)/(n+len(self.Mastercount))
				print(word + ' ' + str(round(temp,4)))
			print('')
			con_num = 0
			for i in con20:
				con_num += 1
				word = i[0]
				n_con = self.con_wordcount[word]
				n = len(self.con_word_lst)
				temp = float(n_con+1)/(n+len(self.Mastercount))
				print(word + ' ' + str(round(temp,4)))
				
		#implementation for topWordsLogOdds
		if self.topWordsLogOdds == 1:
			con_word_log = {}
			lib_word_log = {}
			for word in self.Mastercount:
				if word in self.con_wordcount:
					n_con = self.con_wordcount[word]
				else:
					n_con = 0
				n = len(self.con_word_lst)
				con_temp = float(n_con+1)/(n+len(self.Mastercount))
				
				if word in self.lib_wordcount:
					n_lib = self.lib_wordcount[word]
				else:
					n_lib = 0
				n = len(self.lib_word_lst)
				lib_temp = float(n_lib+1)/(n+len(self.Mastercount))
				
				#compute log-odds ratio
				con_word_log[word] = ln(con_temp/lib_temp)
				lib_word_log[word] = ln(lib_temp/con_temp)
			
			temp_lib = sorted(lib_word_log.items(), key=lambda x: x[1], reverse = True)
			temp_con = sorted(con_word_log.items(), key=lambda x: x[1], reverse = True)

			#find top 20 words with highest log-odds ratio
			lib20 = temp_lib[0:20]
			con20 = temp_con[0:20]

			#print word and log-odds ratio alongside
			lib_num = 0
			for i in lib20:
				word = i[0]
				log_odd = i[1]
				print (word + ' ' + str(round(log_odd,4)))
			print ('')
			con_num = 0
			for i in con20:
				word = i[0]
				log_odd = i[1]
				print (word + ' ' + str(round(log_odd,4)))

	#Classify the test document
	def classify(self,doc):
		"""Implements Naive Bayes Algorithm"""
		curr_file = open(doc,'r')
		con_prob_predict = ln(self.prob_con)
		lib_prob_predict = ln(self.prob_lib)
		for word in curr_file:
			word = word.lower().lstrip().rstrip()
			if word in self.Mastercount:
				if word in self.con_wordcount:
					n_con = self.con_wordcount[word]
				else:
					n_con = 0
				n = len(self.con_word_lst)
				temp = float(n_con+self.smoothing)/(n+self.smoothing*len(self.Mastercount))			
				con_prob_predict += ln(temp)

			if word in self.Mastercount:
				if word in self.lib_wordcount:
					n_lib = self.lib_wordcount[word]
				else:
					n_lib = 0
				n = len(self.lib_word_lst)
				temp = float(n_lib+self.smoothing)/(n+self.smoothing*len(self.Mastercount))
				lib_prob_predict += ln(temp)
		curr_file.close()
		if con_prob_predict>=lib_prob_predict:
			return 'con'
		else:
			return 'lib'

	######################################################
	# TESTING
	######################################################
	def test(self,test_docs):
		#find number of words classified correctly
		nCorrect = 0
		nTotal = 0
		for line in test_docs:
			nTotal += 1
			filename = line.rstrip().lstrip()
			actualLabel = filename[0:3]
			prediction = self.classify(filename)
			if prediction == 'con':
				print('C')
			if prediction == 'lib':
				print('L')
			if actualLabel == prediction:
				nCorrect += 1
		test_docs.close()

		#compute accuracy
		Accuracy = float(nCorrect)/nTotal
		print ('Accuracy: '+"%.4f" %round(Accuracy,4))