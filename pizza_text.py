# Generates the text file for a given pizza data set.

import os, re, sys

# dataset should be 'train' or 'devtest'.
dataset = sys.argv[1]

# Set as the cleaned version of the transcript.
transcript = open("".join(["pizza_", dataset, "_clean"]))

# Makes the temp directories if they don't exist.
data_path = "".join(["data/", dataset, "/pizza_tmp"])
if not os.path.exists(data_path):
    os.mkdir(data_path)
    
# Creates the 'text' file
text = open(data_path + "/text", "w")
lines = []

# Writes the transcription files following this format:
# If the line in the transciption is:
#       blah blah blah (name_001)
#
# The line in 'text' is:
#       name-name_001 blah blah blah
#
# So name-name_001 is the utterance ID.
for line in transcript.readlines():
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
