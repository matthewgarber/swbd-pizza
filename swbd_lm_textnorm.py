import os, sys, re

lm_inpath = sys.argv[1]
lm_outfile = sys.argv[2]

with open(lm_inpath, 'r') as orig_lm:
	tmp_lm = open('lm_tmp', 'w')
	#make lowercase
	tmp_lm.write(orig_lm.read().lower())
	tmp_lm.close()
	#TODO remove markers (which ones?)
	os.system("sed -e 's/<b_aside>//' -e 's/<e_aside>//' -e 's/\[silence\]//' -e 's/\[laughter-.*\]//' <lm_tmp >{}".format(lm_outfile))
	#note partial words left in


