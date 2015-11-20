import os
import re

# Set as the raw version of the transcripts.
pizza_train = open("train/transcript/pizza_train")
pizza_dev = open("devtest/transcript/pizza_devtest")

# Makes the temp directories if they don't exist.
if not os.path.exists("data/train/pizza_tmp"):
    os.mkdir("data/train/pizza_tmp")
if not os.path.exists("data/devtest/pizza_tmp"):
    os.mkdir("data/devtest/pizza_tmp")
    
# Creates the 'reco2file_and_channel' file
text = open("data/train/pizza_tmp/reco2file_and_channel", "w")
lines = []

# Because the recording ID is the same as the wav file name, and
# since there is only a single channel, the file is written in the
# following format:
#       wav_name wav_name A
for line in pizza_train.readlines():
    match = re.match("(.*?) \((.*?)\)", line)
    rec_id = match.group(2)
    lines.append(" ".join([rec_id, rec_id, "A\n"]))
text.writelines(lines)

text = open("data/devtest/pizza_tmp/reco2file_and_channel", "w")
lines = []

for line in pizza_train.readlines():
    match = re.match("(.*?) \((.*?)\)", line)
    rec_id = match.group(2)
    lines.append(" ".join([rec_id, rec_id, "A\n"]))
text.writelines(lines)
