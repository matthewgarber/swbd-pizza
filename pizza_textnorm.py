"""
TODO:
normalize case for train, devtest, and lm
get rid of file names for lm
format file ids correctly
make audio files same format
digit -> written number

USAGE: python pizza_textnorm.py train_path devtest_path lm_path
"""

import os, sys, nltk
from nltk.corpus import cmudict
prondict = nltk.corpus.cmudict.dict()

num_dict = {'1':'one', '2':'two', '3':'three', '4':'four', '5':'five',
'6':'six', '7':'seven', '8':'eight', '9':'nine', '10':'ten', '11':'eleven', '12':'twelve',
'13':'thirteen', '14':'fourteen', '15':'fifteen', '16':'sixteen',
'17':'seventeen', '18':'eighteen', '19':'nineteen', '20':'twenty'}

oov_list = set()

def clean_transcript(oldfname, newfname, lm=False):
	"""make text lowercase, but keep file ids for transcripts

	for lm: get rid of extra """
	orig_transcript = open(oldfname, 'r')
	new_transcript = open(newfname, 'w')

	for line in orig_transcript.readlines():
		in_wordlist = line.lower().split()
		out_wordlist = []
		for w in in_wordlist:
			w = w.strip(',.?')
			if w in num_dict:
				new_w = num_dict[w]
			elif '(' in w and lm==True:
				i = w.index('(')
				new_w = w[:i]
			else:
				new_w = w
			out_wordlist.append(new_w)
			if new_w not in prondict and not new_w.startswith('('):
				oov_list.add(new_w)
		new_line = ' '.join(out_wordlist) + '\n'
		new_transcript.write(new_line)
	orig_transcript.close()

def check_audio(dirname):
	pass

def fix_audio(dirname):
	pass

def main():
	train_path = sys.argv[1]
	devtest_path = sys.argv[2]
	lm_path = sys.argv[3]

	clean_transcript(train_path, 'pizza_train_clean', lm=True)
	clean_transcript(devtest_path, 'pizza_devtest_clean', lm=True)
	clean_transcript(lm_path, 'lm_clean', lm=True)

	with open('oov_list', 'w') as oovfile:
		for w in oov_list:
			oovfile.write('{}\n'.format(w))

main()


