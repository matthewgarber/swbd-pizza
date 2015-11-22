import os
import re

# Set as the cleaned version of the transcripts.
pizza_train = open("train/transcript/pizza_train")
pizza_dev = open("devtest/transcript/pizza_devtest")

# Makes the temp directories if they don't exist.
if not os.path.exists("data/train/pizza_tmp"):
    os.mkdir("data/train/pizza_tmp")
if not os.path.exists("data/devtest/pizza_tmp"):
    os.mkdir("data/devtest/pizza_tmp")
    
# Creates the 'wav.scp' file
text = open("data/train/pizza_tmp/wav.scp", "w")
lines = []

# Writes the wav.scp files following this format:
#       utt_id wav_path
for line in pizza_train.readlines():
    match = re.match("(.*?) \((.*?)\)", line)
    utt_id = match.group(2)
    wav_path = "".join(["train/pizza_8k/", utt_id, ".wav"])
    lines.append(" ".join([utt_id, wav_path + "\n"]))
text.writelines(lines)

text = open("data/devtest/pizza_tmp/wav.scp", "w")
lines = []

for line in pizza_dev.readlines():
    match = re.match("(.*?) \((.*?)\)", line)
    utt_id = match.group(2)
    wav_path = "".join(["devtest/pizza_8k/", utt_id, ".wav"])
    lines.append(" ".join([utt_id, wav_path + "\n"]))
text.writelines(lines)
