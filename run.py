# TODO:
#   remove temp directories
#
#

import os

### Text normalization goes here.

## Data preparation.
os.system("sh swbd-pizza_data_prep.sh")

## Dictionary preparation.
os.system("sh pizza_prepare_dict.sh")

## Language preparation.
os.system('sh utils/prepare_lang.sh data/dict "<unk>" data/local/lang data/lang')
os.system("python swbd_lm_textnorm.py lm/swbd.all lm/swbd_all_clean")

## Create language model.
### Normalizing SWBD LM text goes here.
### Making SRI LMs goes here.
# Format language model.
os.system("sh utils/format_lm_sri.sh data/lang lm/combined_4gram.lm.gz data/dict/lexicon.txt data/lang_final")

# Compute MFCC features for training and devtest data.
for dataset in ["train", "devtest"]:
    os.system("".join(["sh steps/make_mfcc.sh --nj 50 data/", dataset, " exp/make_mfcc/", dataset, " mfcc"]))
    os.system("".join(["sh steps/compute_cmvn_stats.sh data/", dataset, " exp/make_mfcc/", dataset, " mfcc"]))
    os.system("".join(["sh utils/fix_data_dir.sh data/", dataset]))

# Train monophone model.
os.system("sh steps/train_mono.sh --nj 30 data/train data/lang_final exp/mono")

## Train triphone model, round 1.
os.system(align_cmd("exp/mono", "exp/mono_ali"))
os.system(train_deltas_cmd("exp/mono_ali", "exp/tri1"))

## Decoding, round 1.
os.system("sh utils/mkgraph.sh data/lang_final exp/tri1 exp/tri1/graph_tgpr")
os.system('sh steps/decode.sh --nj 30 --cmd "utils/run.pl" exp/tri1/graph_tgpr data/devtest exp/tri1/decode_devtest')

## Train triphone model, round 2.
os.system(align_cmd("exp/tri1", "exp/tri1_ali"))
os.system(train_deltas_cmd("exp/tri1_ali", "exp/tri2"))

## Decoding, round 2.
os.system("sh utils/mkgraph.sh data/lang_final exp/tri2 exp/tri2/graph_tgpr")
os.system('sh steps/decode.sh --nj 30 --cmd "utils/run.pl" exp/tri2/graph_tgpr data/devtest exp/tri2/decode_devtest')

## Get WER 
# Score the decoding results.
os.system("sh score.sh data/devtest  exp/tri1/graph_tgpr exp/tri1/decode_devtest")
os.system("sh score.sh data/devtest  exp/tri2/graph_tgpr exp/tri2/decode_devtest")
### Getting WER from file and printing it goes here.

def align_cmd(src_dir, align_dir):
    command = " ".join(["sh steps/align_si.sh --nj 30 data/train data/lang_final",
                        src_dir, align_dir])
    return command

def train_deltas_cmd(align_dir, exp_dir):
    command = " ".join(["sh steps/train_deltas.sh 3200 30000 data/train data/lang_final",
                        align_dir, exp_dir])
    return command
