import os, re, sys, wave

# dataset should be 'train' or 'devtest'.
dataset = sys.argv[1]

# Set as the cleaned version of the transcript.
transcript_clean = open("".join(["pizza_", dataset, "_clean"]))

# The raw transcriptions are needed for the exact wav file names
transcript_raw = open("".join([dataset, "/transcript/pizza_", dataset]))

# Makes the temp directories if they don't exist.
data_path = "".join(["data/", dataset, "/pizza_tmp"])
if not os.path.exists(data_path):
    os.mkdir(data_path)

# Creates the 'segments' file
segments = open(data_path + "/segments", "w")
lines = []

# Writes the file in the following format:
#
# utt_id rec_id start_time end_time
#
# where rec_id is the name of the wav file (minus ".wav")
for line_raw in transcript_raw.readlines():
    match_utt = re.match("(.*?) \((.*?)\)", transcript_clean.readline())
    match_rec = re.match("(.*?) \((.*?)\)", line_raw)
    utt_id = match_utt.group(2)
    rec_id = match_rec.group(2)
    wav = wave.open("".join([dataset, "/pizza/", rec_id, ".wav"]))
    length = str(round(((1.0 * wav.getnframes ()) / wav.getframerate ()) - 0.01, 2))
    speaker_match = re.match("[a-zA-Z]+", utt_id)
    if speaker_match:
        utt_id = "".join([speaker_match.group(0), "-", utt_id])
    else:
        utt_id = "".join(["unk-", rec_id])
    lines.append(" ".join([utt_id, rec_id, "0.00", length + "\n"]))
    wav.close()
    
segments.writelines(lines)