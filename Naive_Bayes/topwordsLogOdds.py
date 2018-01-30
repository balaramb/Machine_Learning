import Naive_Bayes as nb
import sys

def main():
	train_docs = open(sys.argv[-1],'r')

	naiveb = nb.NaiveBayesClassifier(topWordsLogOdds = 1)
	naiveb.train(train_docs)

if __name__ == '__main__':
    main()