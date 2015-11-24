import os
import re

# Makes the temp directories if they don't exist.
if not os.path.exists("data/train/pizza_tmp"):
    os.mkdir("data/train/pizza_tmp")
if not os.path.exists("data/devtest/pizza_tmp"):
    os.mkdir("data/devtest/pizza_tmp")
    
utt2spk = open("data/train/pizza_tmp/utt2spk", "w")
# Uses the 'text' file to create the 'utt2spk' file
text_file = open("data/train/pizza_tmp/text")
lines = []

# Writes the transcription files following this format:
#       utt_id speaker_id
for line in text_file.readlines():
    match = re.match("(.*?)-\w*", line)
    utt_id = match.group(0)
    speaker_id = match.group(1)
    lines.append(" ".join([utt_id, speaker_id + "\n"]))
utt2spk.writelines(sorted(lines))

utt2spk = open("data/devtest/pizza_tmp/utt2spk", "w")
text_file = open("data/devtest/pizza_tmp/text")
lines = []

for line in text_file.readlines():
    match = re.match("(.*?)-\w*", line)
    utt_id = match.group(0)
    speaker_id = match.group(1)
    lines.append(" ".join([utt_id, speaker_id + "\n"]))
utt2spk.writelines(sorted(lines))
