import os, re, sys

# dataset should be 'train' or 'devtest'.
dataset = sys.argv[1]

# Set as the cleaned version of the transcript.
transcript = open("".join(["pizza_", dataset, "_clean"]))

# Makes the temp directories if they don't exist.
data_path = "".join(["data/", dataset, "/pizza_tmp"])
if not os.path.exists(data_path):
    os.mkdir(data_path)
    
# Creates the 'wav.scp' file
wavscp = open(data_path + "wav.scp", "w")
lines = []

# Writes the wav.scp files following this format:
#       utt_id wav_path
for line in transcript.readlines():
    match = re.match("(.*?) \((.*?)\)", line)
    utt_id = match.group(2)
    wav_path = "".join([dataset, "/pizza_8k/", utt_id, ".wav"])
    lines.append(" ".join([utt_id, wav_path + "\n"]))
wavscp.writelines(lines)
