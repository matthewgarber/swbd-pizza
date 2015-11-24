export LANG=C; export LC_ALL=C #set up sorting

# Takes either 'train' or 'devtest' as its argument.

set=$1

mkdir -p data/$set/swbd_tmp
dir=data/$set/swbd_tmp
awk '{ 
       name=substr($1,1,6); gsub("^sw","sw0",name); side=substr($1,7,1); 
       stime=$2; etime=$3;
       printf("%s-%s_%06.0f-%06.0f", 
              name, side, int(100*stime+0.5), int(100*etime+0.5));
       for(i=4;i<=NF;i++) printf(" %s", tolower($i)); printf "\n"
}' $set/transcript/swbd_train/*-trans.text > $dir/transcripts1_$set.txt;
sort -c $dir/transcripts1_$set.txt || exit 1;
cat $dir/transcripts1_$set.txt \
  | perl -ane 's:\s\[SILENCE\](\s|$):$1:gi; 
               s/<B_ASIDE>//gi; 
               s/<E_ASIDE>//gi; 
               print;' \
  | awk '{if(NF > 1) { print; } } ' > $dir/text;


