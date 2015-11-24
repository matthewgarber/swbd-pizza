#from format_lm_sri.sh

if [ $# -eq 4 ] ; then
  lang_dir=$1
  lm=$2
  lexicon=$3
  out_dir=$4
else
  lang_dir=$1
  lm=$2
  out_dir=$3
fi

mkdir -p $out_dir
cp -r $lang_dir/* $out_dir || exit 1;

###check what fname actually is in out_dir
cat $lm | utils/find_arpa_oovs.pl $out_dir/words.txt \
  > $out_dir/oovs_${lm_base}.txt || exit 1;

# Removing all "illegal" combinations of <s> and </s>, which are supposed to 
# occur only at being/end of utt.  These can cause determinization failures 
# of CLG [ends up being epsilon cycles].
cat $lm |  \
  | egrep -v '<s> <s>|</s> <s>|</s> </s>' \
  | gzip -c > $tmpdir/lm.gz || exit 1;

awk '{print $1}' $out_dir/words.txt > $tmpdir/voc || exit 1;

# Change the LM vocabulary to be the intersection of the current LM vocabulary
# and the set of words in the pronunciation lexicon. This also renormalizes the 
# LM by recomputing the backoff weights, and remove those ngrams whose 
# probabilities are lower than the backed-off estimates.
###need to set srilm_opts
###is this step actually necessary?
change-lm-vocab -vocab $tmpdir/voc -lm $tmpdir/lm.gz -write-lm $tmpdir/out_lm \
  $srilm_opts || exit 1;

arpa2fst $tmpdir/out_lm | fstprint \
  | utils/eps2disambig.pl | utils/s2eps.pl \
  | fstcompile --isymbols=$out_dir/words.txt --osymbols=$out_dir/words.txt \
    --keep_isymbols=false --keep_osymbols=false \
  | fstrmepsilon | fstarcsort --sort_type=ilabel > $out_dir/G.fst || exit 1;

fstisstochastic $out_dir/G.fst

# The output is like:
# 9.14233e-05 -0.259833
# we do expect the first of these 2 numbers to be close to zero (the second is
# nonzero because the backoff weights make the states sum to >1).

echo "Succeeded in formatting LM '$lm' -> '$out_dir/G.fst'"
