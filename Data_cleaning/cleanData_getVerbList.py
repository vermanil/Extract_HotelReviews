import nltk
import csv
import pickle
import string
import re

def remove_punctuations(text):
	# print text
	exclude = string.punctuation
	# print exclude
	text = re.sub("^\d+\s|\s\d+\s|\s\d+$", " ", text)
	finalCorpus = "".join(c for c in text if c not in exclude)
	return finalCorpus

def remove_stopWord(text):
	withStopWord = text.split() 
	# print withStopWord
	stopWord=open("stop_eng.txt", "r").read().split("\n")
	removeStopWord = list()
	for w in withStopWord:
		if w not in stopWord:
			w="".join(c for c in w if c != '.')
			if w != "":
				w = re.sub("^\d+\s|\s\d+\s|\s\d+$", " ", w)
				removeStopWord.append(w)
	return removeStopWord

if __name__ == "__main__":
	corpus = list()

	location = ['mumbai']
	for l in location:
		with open('items_' + l + '.csv', 'rb') as dataFile:
			data = csv.reader(dataFile, )
			# print data.content
			for row in data:
				corpus.append(row[0])

	NounAdj = {}
	print len(corpus)
	c = -1
	for crps in corpus:
		c = c+1
		print c
		# print crps
		# con = open('conjunctions.txt','r').read().split('\n')
		# crps = " ".join(co for co in crps.split() if co not in con)
		sent_token = nltk.sent_tokenize(crps.decode('utf-8'))
		# print sent_token
		# break
		# se = ['Room is not good', 'Room is smell']
		print len(sent_token)
		for s in sent_token:
			# print(s)	
			# print s
			cr = remove_punctuations(s)
			tokens = remove_stopWord(s.encode('utf-8'))
			tagged = nltk.pos_tag(tokens)
			# print tagged
			noun = set()
			verb = set()
			for i in tagged:
				if i[1] == 'NNP' or i[1] == 'NN':
					noun.add(i[0])
					# print noun
# i[1] == 'VB' or i[1] == 'VBD' or i[1] == 'VBG' or i[1] == 'VBN' or i[1] == 'VBP'
				if i[1] == 'JJ':
					verb.add(i[0])
					# print verb

			for i in noun:
				if i in NounAdj.keys():
					for j in verb:
						NounAdj[i].add(j)		
				else:
					NounAdj[i] = verb
	pickle.dump(NounAdj,open( "Adj.p", "wb" ))
	print NounAdj
