#!/bin/bash

### Edited from the Kaldi SWBD example
### Takes either 'train' or 'devtest' as its argument.
###
### New comments are after "###".

# Switchboard-1 training data preparation customized for Edinburgh
# Author:  Arnab Ghoshal (Jan 2013)

# To be run from one tmpdirectory above this script.

## The input is some tmpdirectory containing the switchboard-1 release 2
## corpus (LDC97S62).  Note: we don't make many assumptions about how
## you unpacked this.  We are just doing a "find" command to locate
## the .sph files.

## The second input is optional, which should point to a tmpdirectory containing
## Switchboard transcriptions/documentations (specifically, the conv.tab file).
## If specified, the script will try to use the actual speaker PINs provided 
## with the corpus instead of the conversation side ID (Kaldi default). We 
## will be using "find" to locate this file so we don't make any assumptions
## on the tmpdirectory structure. (Peng Qi, Aug 2014)

## . path.sh

### Set up sorting.
export LANG=C; export LC_ALL=C

datadir=$1

tmpdir=data/$1/swbd_tmp
mkdir -p $tmpdir

### Downsample all audio for the pizza data to 8000 and reduce to a single channel.

python downsample_audio.py

sph2pipe=sph2pipe_v2.5/sph2pipe

# find sph audio files
ls $datadir/swbd | sort > $tmpdir/sph.flist

### Normalize the SWBD transcripts.
sh swbd_textnorm.sh $datadir

# (1c) Make segment files from transcript
#segments file format is: utt-id side-id start-time end-time, e.g.:
#sw02001-A_000098-001156 sw02001-A 0.98 11.56
### Maps each utterance to a specific portion of an audio file.
awk '{ 
       segment=$1;
       split(segment,S,"[_-]");
       side=S[2]; audioname=S[1]; startf=S[3]; endf=S[4];
       print segment " " audioname "-" side " " startf/100 " " endf/100
}' < $tmpdir/text > $tmpdir/segments

sed -e 's?.*/??' -e 's?.sph??' $tmpdir/sph.flist | paste - $tmpdir/sph.flist \
  > $tmpdir/sph.scp

awk -v sph2pipe=$sph2pipe -v datadir=$datadir '{
  printf("%s-A %s -f wav -p -c 1 %s |\n", $1, sph2pipe, datadir"/swbd/"$2); 
  printf("%s-B %s -f wav -p -c 2 %s |\n", $1, sph2pipe, datadir"/swbd/"$2);
}' < $tmpdir/sph.scp | sort > $tmpdir/wav.scp || exit 1;
#side A - channel 1, side B - channel 2

# this file reco2file_and_channel maps recording-id (e.g. sw02001-A)
# to the file name sw02001 and the A, e.g.
# sw02001-A  sw02001 A
# In this case it's trivial, but in other corpora the information might
# be less obvious.  Later it will be needed for ctm scoring.
awk '{print $1}' $tmpdir/wav.scp \
  | perl -ane '$_ =~ m:^(\S+)-([AB])$: || die "bad label $_"; 
               print "$1-$2 $1 $2\n"; ' \
  > $tmpdir/reco2file_and_channel || exit 1;

### Creates a file listing each utterance and its speaker and creates a file
### listing each speaker and the utterances they speak for SWBD.
awk '{spk=substr($1,1,9); print $1 " " spk}' $tmpdir/segments > $tmpdir/utt2spk \
  || exit 1;

# We assume each conversation side is a separate speaker. This is a very 
# reasonable assumption for Switchboard. The actual speaker info file is at:
# http://www.ldc.upenn.edu/Catalog/desc/addenda/swb-multi-annot.summary

### Create the text, segments, etc. files for the pizza data.
python pizza_text.py $datadir
python pizza_segments.py $datadir
python pizza_wavscp.py $datadir
python pizza_reco2file_and_channel.py $datadir
python pizza_utt2spk.py $datadir

### Combine the temporary files for the pizza and SWBD data into their final form.
pizza_tmp=data/$datadir/pizza_tmp
cat $pizza_tmp/text $tmpdir/text | sort -u > data/$datadir/text
cat $pizza_tmp/segments $tmpdir/segments | sort -u > data/$datadir/segments
cat $pizza_tmp/wav.scp $tmpdir/wav.scp | sort -u > data/$datadir/wav.scp
cat $pizza_tmp/reco2file_and_channel $tmpdir/reco2file_and_channel | sort -u > data/$datadir/reco2file_and_channel
cat $pizza_tmp/utt2spk $tmpdir/utt2spk | sort -u > data/$datadir/utt2spk

sort -k 2 data/$datadir/utt2spk | scripts/utt2spk_to_spk2utt.pl > data/$datadir/spk2utt || exit 1;

if [ $# == 2 ]; then # fix speaker IDs
  find $2 -name conv.tab > $dir/conv.tab
  local/swbd1_fix_speakerid.pl `cat $dir/conv.tab` data/train
  utils/utt2spk_to_spk2utt.pl data/train/utt2spk.new > data/train/spk2utt.new
  # patch files
  for f in spk2utt utt2spk text segments; do
    cp data/train/$f data/train/$f.old || exit 1;
    cp data/train/$f.new data/train/$f || exit 1;
  done
  rm $dir/conv.tab
fi 

### Ensures segments are present in all files.
utils/fix_data_dir.sh data/train

echo Switchboard and Pizza data preparation succeeded.

#scripts/fix_data_tmpdir.sh data/$datadir
