import Naive_Bayes as nb
import sys

def main():
	#read in contents
	test_docs = open(sys.argv[-1],'r')
	train_docs = open(sys.argv[-2],'r')

	naiveb = nb.NaiveBayesClassifier()
	naiveb.train(train_docs)
	naiveb.test(test_docs)

if __name__ == '__main__':
    main()