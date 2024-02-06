import sys, os
import click
from itertools import islice

# This is a tool that converts DiffSinger "transcription.csv" back into HTK labels.

@click.command()
@click.option('--csv_path', '-i', required=True, help='Path to DiffSinger Transcription File.')
@click.option('--out_path', '-o', default='wavs', help='Path to Export labels.')

def main(csv_path, out_path):
	
	# read csv into a weird list thing idk i like these
	transcription_list = []
	with open(csv_path, 'r', encoding='utf-8') as csv:
		for line in islice(csv, 1, None):
			transcription_list.append(line.rstrip().split(','))

	# lets do this girls
	for sequence in transcription_list:
		try:
			name = sequence[0] # name of segment
			phonemes = sequence[1].split(' ') # phoneme list in the segment
			durs = sequence[2].split(' ') # durations list in the segment
			len_list = []
			offset = 0 # offset will always be 0 for transcriptions

			# assert that there's no errors in the transcription.
			assert len(phonemes) == len(durs)

			for i in range(len(durs)):
				'''
				Convert the durations of phonemes into HTK label style fields
				'''
				if i == 0:
					start = offset
				end = int(f"{float(durs[i]) * 10000000:.0f}")
				len_list.append([start, int(start+end)])
				start = start+end

			# ensure the export path exists
			if not os.path.exists(f"{out_path}"):
				os.mkdir(f"{out_path}")

			# write the label
			with open(f"{out_path}/{name}.lab", 'w+', encoding='utf-8') as lab:
				for i in range(len(phonemes)):
					lab.write(f"{len_list[i][0]} {len_list[i][1]} {str(phonemes[i])}\n")
		except:
			print(f"Error on {sequence}: Skipping")
			pass

if __name__ == "__main__":
	main()