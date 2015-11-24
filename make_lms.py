import sys, os

pizza_lm = sys.argv[1]
swbd_lm = sys.argv[2]

#make pizza lm
os.system('~/srilm-1.7.1/bin/macosx/ngram-count -text {} -unk -map-unk -order 3 -lm pizza_trigram.lm -wbdiscount'.format(pizza_lm))

#make swbd lm
os.system('~/srilm-1.7.1/bin/macosx/ngram-count -text {} -unk -map-unk -order 4 -lm swbd_4gram.lm -wbdiscount'.format(swbd_lm))

#combine lm into one text file
pizzafile = open(pizza_lm, 'r')
swbdfile = open(swbd_lm, 'r')
if 'swbd_pizza_lm' in os.listdir(os.getcwd()):
	os.remove('swbd_pizza_lm')
combined = open('swbd_pizza_lm', 'w')
combined.write(pizzafile.read()+'\n'+swbdfile.read())
pizzafile.close()
swbdfile.close()
combined.close()

#create combined lm
os.system('~/srilm-1.7.1/bin/macosx/ngram-count -unk -map-unk -order 4 -text swbd_pizza_lm -lm combined_4gram.lm -wbdiscount')
