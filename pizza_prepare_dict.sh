#!/bin/bash

### Edited from the original used in the Kaldi Switchboard Tutorial.
###
### New comments are after "###".

# Formatting the Mississippi State dictionary for use in Edinburgh. Differs 
# from the one in Kaldi s5 recipe in that it uses lower-case --Arnab (Jan 2013)

# To be run from one directory above this script.

#. path.sh

srcdir=lexicon
dir=data/dict
tmpdir=data/dict/tmp
mkdir -p $dir
mkdir -p $tmpdir
srcdict=$srcdir/sw-ms98-dict_patched.text

# assume swbd_p1_data_prep.sh was done already.
[ ! -f "$srcdict" ] && echo "No such file $srcdict" && exit 1;

cp $srcdict $tmpdir/lexicon0.txt || exit 1;
# patch <local/dict.patch $tmpdir/lexicon0.txt || exit 1;

#(2a) Dictionary preparation:
# Pre-processing (Upper-case, remove comments)
### Cleans up and normalizes the dictionary.
awk 'BEGIN{getline}($0 !~ /^#/) {print}' \
  $tmpdir/lexicon0.txt | sort | awk '($0 !~ /^[[:space:]]*$/) {print}' \
   > $tmpdir/lexicon1.txt || exit 1;

### Copies all the non-silent phones from lexicon1 to create a dictionary of non-silent phones.
cat $tmpdir/lexicon1.txt | awk '{ for(n=2;n<=NF;n++){ phones[$n] = 1; }} END{for (p in phones) print p;}' | \
  grep -v sil > $dir/nonsilence_phones.txt  || exit 1;

### Creates a file listing only silent phones.
( echo sil; echo spn; echo nsn; echo lau ) > $dir/silence_phones.txt

### Creates a file listing the optional silent phones.
echo sil > $dir/optional_silence.txt

# No "extra questions" in the input to this setup, as we don't
# have stress or tone.
echo -n >$tmpdir/extra_questions.txt

# Add to the lexicon the silences, noises etc.
# Add single letter lexicon
# The original swbd lexicon does not have precise single letter lexicion
# e.g. it does not have entry of W
cat $tmpdir/lexicon1.txt $srcdir/MSU_single_letter.txt  > $tmpdir/lexicon2.txt || exit 1;

# Map the words in the lexicon.  That is-- for each word in the lexicon, we map it
# to a new written form.  The transformations we do are:
# remove laughter markings, e.g.
# [LAUGHTER-STORY] -> STORY
# Remove partial-words, e.g.
# -[40]1K W AH N K EY
# becomes -1K
# and
# -[AN]Y IY
# becomes
# -Y
# -[A]B[OUT]- B
# becomes
# -B-
# Also, curly braces, which appear to be used for "nonstandard"
# words or non-words, are removed, e.g. 
# {WOLMANIZED} W OW L M AX N AY Z D
# -> WOLMANIZED
# Also, mispronounced words, e.g.
#  [YEAM/YEAH] Y AE M
# are changed to just e.g. YEAM, i.e. the orthography
# of the mispronounced version.
# Note-- this is only really to be used in training.  The main practical
# reason is to avoid having tons of disambiguation symbols, which
# we otherwise would get because there are many partial words with
# the same phone sequences (most problematic: S).
# Also, map
# THEM_1 EH M -> THEM
# so that multiple pronunciations just have alternate entries
# in the lexicon.

scripts/swbd1_map_words.pl -f 1 $tmpdir/lexicon2.txt | sort -u \
  > $tmpdir/lexicon3.txt || exit 1;

python scripts/format_acronyms_dict.py -i $tmpdir/lexicon3.txt -o $tmpdir/lexicon4.txt \
  -L $srcdir/MSU_single_letter.txt -M $tmpdir/acronyms_raw.map
cat $tmpdir/acronyms_raw.map | sort -u > $tmpdir/acronyms.map

### Add the pizza dictionary.
cat $srcdir/pizza_dict.txt $tmpdir/lexicon4.txt > $tmpdir/lexicon5.txt

( echo 'i ay' )| cat - $tmpdir/lexicon5.txt | tr '[A-Z]' '[a-z]' | sort -u > $tmpdir/lexicon_words.txt

( echo '<sil> sil'; echo '[vocalized-noise] spn'; echo '[noise] nsn'; \
  echo '[laughter] lau'; echo '<unk> spn' ) | cat - $tmpdir/lexicon_words.txt | sort -u \
  > $tmpdir/lexicon.txt

cp $tmpdir/lexicon_words.txt $dir
cp $tmpdir/lexicon.txt $dir
  
#pushd $tmpdir >&/dev/null
#popd >&/dev/null
#rm $tmpdir/lexiconp.txt
echo Prepared input dictionary and phone-sets for Pizza and Switchboard phase 1.
