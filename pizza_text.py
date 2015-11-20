import os
import re

# Set as the cleaned version of the transcripts.
pizza_train = open("pizza_train_clean")
pizza_dev = open("pizza_devtest_clean")

# Makes the temp directories if they don't exist.
if not os.path.exists("data/train/pizza_tmp"):
    os.mkdir("data/train/pizza_tmp")
if not os.path.exists("data/devtest/pizza_tmp"):
    os.mkdir("data/devtest/pizza_tmp")
    
# Creates the 'text' file
text = open("data/train/pizza_tmp/text", "w")
lines = []

# Writes the transcription files following this format:
# If the line in the transciption is:
#       blah blah blah (name_001)
#
# The line in 'text' is:
#       name-name_001 blah blah blah
#
# So name-name_001 is the utterance ID.
for line in pizza_train.readlines():
    match = re.match("(.*?) \((.*?)\)", line)
    trans = match.group(1)
    utt_id = match.group(2)
    speaker_match = re.match("[a-zA-Z]+", utt_id)
    if speaker_match:
        speaker_id = speaker_match.group(0)
    else:
	speaker_id = "unk"
    lines.append("".join([speaker_id, "-", utt_id, " ", trans, "\n"]))
        
text.writelines(lines)

text = open("data/devtest/pizza_tmp/text", "w")
lines = []

for line in pizza_dev.readlines():
    match = re.match("(.*?) \((.*?)\)", line)
    trans = match.group(1)
    utt_id = match.group(2)
    speaker_match = re.match("[a-zA-Z]+", utt_id)
    if speaker_match:
        speaker_id = speaker_match.group(0)
    else:
	speaker_id = "unk"
    lines.append("".join([speaker_id, "-", utt_id, " ", trans, "\n"]))
    
text.writelines(lines)
