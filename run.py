# Pipeline script for the SWBD/Pizza speech recognition model.
# Authors: Matthew Garber and Meital Singer

import os, shutil

# Aligns the model and aves the alignment data.
def align_cmd(src_dir, align_dir):
    command = " ".join(["sh steps/align_si.sh --nj 30 data/train data/lang_final",
                        src_dir, align_dir])
    return command

# Utilizes the given alignment data to generate a new model.
def train_deltas_cmd(align_dir, exp_dir):
    command = " ".join(["sh steps/train_deltas.sh 3200 30000 data/train data/lang_final",
                        align_dir, exp_dir])
    return command

## Data preparation.
# Pizza transcripts have already been partially edited due to discrepancies between the IDs at the
# end of each utterance and the filenames that required manual adjustment.
os.system("python pizza_textnorm.py train/transcript/pizza_train devtest/transcript/pizza_devtest lm/pizza_all")
for dataset in ["train", "devtest"]:
    os.system("sh swbd-pizza_data_prep.sh " + dataset)
  
# Remove temporary directories.
for dataset in ["train", "devtest"]:
    shutil.rmtree("".join(["data/", dataset, "/pizza_tmp"]))
    shutil.rmtree("".join(["data/", dataset, "/swbd_tmp"]))

## Dictionary preparation.
os.system("sh pizza_prepare_dict.sh")

## Language preparation.
os.system('bash utils/prepare_lang.sh data/dict "<unk>" data/local/lang data/lang')

## Create language model.
os.system("python swbd_lm_textnorm.py lm/swbd_all lm/swbd_all_clean")
os.system("python make_lms.py lm/pizza_all lm/swbd_all_clean")
lm_name = "combined_4gram.lm"
os.system("gzip " + lm_name)

# Format language model.
os.system("".join(["sh utils/format_lm_sri.sh data/lang lm/", lm_name, ".gz data/dict/lexicon.txt data/lang_final"]))

os.system("bash utils/fix_data_dir.sh data/devtest")

# Compute MFCC features for training and devtest data.
for dataset in ["train", "devtest"]:
    os.system("".join(["sh steps/make_mfcc.sh --nj 50 data/", dataset, " exp/make_mfcc/", dataset, " mfcc"]))
    os.system("".join(["sh steps/compute_cmvn_stats.sh data/", dataset, " exp/make_mfcc/", dataset, " mfcc"]))
    os.system("".join(["bash utils/fix_data_dir.sh data/", dataset]))

## Train monophone model.
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

# Print word error rate for scored lattices.
exp_path = "exp/tri2/decode_devtest/"
filenames = os.listdir(exp_path)
for filename in filenames:
    if filename.startswith("wer"):
	wer_file = open(exp_path + filename)
	print(wer_file.readlines()[1])
	wer_file.close()
