import os
import re

pizza_train = open("pizza_train_clean")
pizza_dev = open("pizza_devtest_clean")
if not os.path.exists("train"):
    os.mkdir("train")

if not os.path.exists("devtest"):
    os.mkdir("devtest")
    
text = open("train/text", "w")
lines = []

for line in pizza_train.readlines():
    match = re.match("(.*?) \((.*?)\)", line)
    trans = match.group(1)
    utt_id = match.group(2)
    speaker_match = re.match("[a-zA-Z]+", utt_id)
    if speaker_match:
        speaker_id = speaker_match.group(0)
        lines.append("".join([speaker_id, "-", utt_id, " ", trans, "\n"]))
    else:
        lines.append("".join([utt_id, " ", trans, "\n"]))
text.writelines(lines)

text = open("devtest/text", "w")
lines = []

for line in pizza_dev.readlines():
    match = re.match("(.*?) \((.*?)\)", line)
    trans = match.group(1)
    utt_id = match.group(2)
    speaker_match = re.match("[a-zA-Z]+", utt_id)
    if speaker_match:
        speaker_id = speaker_match.group(0)
        lines.append("".join([speaker_id, "-", utt_id, " ", trans, "\n"]))
    else:
        lines.append("".join(["unk", "-", utt_id, " ", trans, "\n"]))
text.writelines(lines)
