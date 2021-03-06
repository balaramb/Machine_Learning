import Naive_Bayes as nb
import sys

def main():
	nStopWords_q = int(sys.argv[-1])
	test_docs = open(sys.argv[-2],'r')
	train_docs = open(sys.argv[-3],'r')

	naiveb = nb.NaiveBayesClassifier(nStopWords = nStopWords_q)
	naiveb.train(train_docs)
	naiveb.test(test_docs)

if __name__ == '__main__':
    main()