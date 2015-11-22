import os
import re
import wave

# Set as the cleaned version of the transcripts.
train_clean = open("pizza_train_clean")
dev_clean = open("pizza_devtest_clean")

# The raw transcriptions are needed for the exact wav file names
train_raw = open("train/transcript/pizza_train")
dev_raw = open("devtest/transcript/pizza_devtest")

# Makes the temp directories if they don't exist.
if not os.path.exists("data/train/pizza_tmp"):
    os.mkdir("data/train/pizza_tmp")
if not os.path.exists("data/devtest/pizza_tmp"):
    os.mkdir("data/devtest/pizza_tmp")

# Creates the 'segments' file
segments = open("data/train/pizza_tmp/segments", "w")
lines = []

# Writes the file in the following format:
#
# utt_id rec_id length
#
# where rec_id is the name of the wav file (minus ".wav")
for line_raw in train_raw.readlines():
    match_utt = re.match("(.*?) \((.*?)\)", train_clean.readline())
    match_rec = re.match("(.*?) \((.*?)\)", line_raw)
    utt_id = match_utt.group(2)
    rec_id = match_rec.group(2)
    wav = wave.open("train/pizza_8k/" + rec_id + ".wav")
    length = str(round(((1.0 * wav.getnframes ()) / wav.getframerate ()) - 0.01, 2))
    speaker_match = re.match("[a-zA-Z]+", utt_id)
    if speaker_match:
        utt_id = "".join([speaker_match.group(0), "-", utt_id])
    else:
        utt_id = "unk"
    lines.append(" ".join([utt_id, rec_id, "0.00", length + "\n"]))
    wav.close()
segments.writelines(lines)

segments = open("data/devtest/pizza_tmp/segments", "w")
lines = []

for line_raw in dev_raw.readlines():
    match_utt = re.match("(.*?) \((.*?)\)", dev_clean.readline())
    match_rec = re.match("(.*?) \((.*?)\)", line_raw)
    utt_id = match_utt.group(2)
    rec_id = match_rec.group(2)
    wav = wave.open("devtest/pizza_8k/" + rec_id + ".wav")
    length = str(round(((1.0 * wav.getnframes ()) / wav.getframerate ()) - 0.01, 2))
    speaker_match = re.match("[a-zA-Z]+", utt_id)
    if speaker_match:
        utt_id = "".join([speaker_match.group(0), "-", utt_id])
    else:
        utt_id = "unk"
    lines.append(" ".join([utt_id, rec_id, "0.00", length + "\n"]))
    wav.close()
segments.writelines(lines)
