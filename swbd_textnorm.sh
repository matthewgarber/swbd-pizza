export LANG=C; export LC_ALL=C #set up sorting

MAIN_DIR=$1
mkdir $MAIN_DIR/tmp
dir=$MAIN_DIR/tmp
SWBD_DIR=$2

for set in train devtest; do
	awk '{ 
	       name=substr($1,1,6); gsub("^sw","sw0",name); side=substr($1,7,1); 
	       stime=$2; etime=$3;
	       printf("%s-%s_%06.0f-%06.0f", 
	              name, side, int(100*stime+0.5), int(100*etime+0.5));
	       for(i=4;i<=NF;i++) printf(" %s", $i); printf "\n"
	}' $MAIN_DIR/$set/transcript/swbd_$set/*-trans.text > $dir/transcripts1_$set.txt;
	sort -c $dir/transcripts1_$set.txt || exit 1;
	cat $dir/transcripts1_$set.txt \
	  | perl -ane 's:\s\[SILENCE\](\s|$):$1:gi; 
	               s/<B_ASIDE>//gi; 
	               s/<E_ASIDE>//gi; 
	               print;' \
	  | awk '{if(NF > 1) { print; } } ' > $dir/transcripts2_$set.txt;
   $SWBD_DIR/local/swbd1_map_words.pl -f 2- $dir/transcripts2_$set.txt > $dir/$set_text
  #  python $SWBD_DIR/local/map_acronyms_transcripts.py -i $MAIN_DIR/tmp/$set_text -o $MAIN_DIR/tmp/$set_text_map \
  # -M data/local/dict_nosp/acronyms.map 
# mv $dir/text_map $dir/text
done

