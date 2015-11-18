import os
import re
import wave

pizza_train = open("train/transcript/pizza_train")
pizza_dev = open("devtest/transcript/pizza_devtest")
if not os.path.exists("train"):
    os.mkdir("train")

if not os.path.exists("devtest"):
    os.mkdir("devtest")
    
text = open("train/segments", "w")
lines = []

for line in pizza_train.readlines():
    match = re.match("(.*?) \((.*?)\)", line)
    utt_id = match.group(2)
    wav = wave.open("train/pizza/" + utt_id + ".wav")
    length = str(round(((1.0 * wav.getnframes ()) / wav.getframerate ()) - 0.01, 2))
    lines.append(" ".join([utt_id, utt_id, "0.00", length, "\n"]))
    wav.close()
text.writelines(lines)

text = open("devtest/segments", "w")
lines = []

for line in pizza_dev.readlines():
    match = re.match("(.*?) \((.*?)\)", line)
    utt_id = match.group(2)
    wav = wave.open("devtest/pizza/" + utt_id + ".wav")
    length = str(round(((1.0 * wav.getnframes ()) / wav.getframerate ()) - 0.01, 2))
    lines.append(" ".join([utt_id, utt_id, "0.00", length, "\n"]))
    wav.close()
text.writelines(lines)
