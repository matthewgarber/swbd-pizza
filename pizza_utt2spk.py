import os, re, sys

# dataset should be 'train' or 'devtest'.
dataset = sys.argv[1]

# Makes the temp directories if they don't exist.
data_path = "".join(["data/", dataset, "/pizza_tmp"])
if not os.path.exists(data_path):
    os.mkdir(data_path)
    
utt2spk = open(data_path + "/utt2spk", "w")
# Uses the 'text' file to create the 'utt2spk' file
text_file = open(data_path + "/text")
lines = []

# Writes the transcription files following this format:
#       utt_id speaker_id
for line in text_file.readlines():
    match = re.match("(.*?)-\w*", line)
    utt_id = match.group(0)
    speaker_id = match.group(1)
    lines.append(" ".join([utt_id, speaker_id + "\n"]))

utt2spk.writelines(sorted(lines))