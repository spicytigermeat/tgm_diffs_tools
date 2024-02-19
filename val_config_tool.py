import click
import glob
import csv
import random
import os
from pathlib import Path
import yaml

@click.command()
@click.option(
	'--in_path',
	'-i',
	type=str,
	required=True,
	help='Path of raw DS Voice Data.'
)
@click.option(
	'--val_num',
	'-v',
	type=int,
	default=5,
	required=False,
	help='Amount of Validation files to choose per speaker. Default: 5'
)
@click.option(
	'--out_path',
	'-o',
	type=str,
	required=False,
	default='diffsinger_config.yaml',
	help='Path to export to. Default: \'diffsinger_config.yaml\''
)

def main(val_num: int, in_path: str, out_path: str):
	'''
	Creates validation file list for DiffSinger config.
	'''

	# initialize variables
	ds_config = {
		'num_spk':0,
		'speakers':[],
		'raw_data_dir':[],
		'test_prefixes':[]
	}
	curr_speaker_index = 0

	# create a list of filenames from the transcriptions.csv file
	for tr in glob.glob(f"{in_path}/**/transcriptions.csv", recursive=True):

		name_list = []

		# add 1 to the count of speakers
		ds_config['num_spk'] = ds_config['num_spk'] + 1

		# add speaker to this iteration, accounting for if the "raw" folder is used or not
		if Path(tr).parents[0].stem == 'raw':
			ds_config['speakers'].append(str(Path(tr).parents[1].stem))
		else:
			ds_config['speakers'].append(str(Path(tr).parents[0].stem))

		# add the raw data dir
		ds_config['raw_data_dir'].append(str(Path(tr).parents[0]))

		# actually read the transcript
		with open(tr, 'r', encoding='utf-8') as csv_file:
			transcript = csv.DictReader(csv_file)

			for row in transcript:
				trn = [row for row in transcript]

		# create a list of the names
		for i in range(len(trn)):
			name_list.append(trn[i]['name'])

		# pick n number of files at random, ensuring there will be no doubles
		for i in range(val_num):
			random_prefix = random.choice(name_list)
			ds_config['test_prefixes'].append(f"{str(curr_speaker_index)}:{random_prefix}")
			name_list.remove(random_prefix)

		# add 1 to the index for the sake of "num_spk"
		curr_speaker_index += 1

	# write yaml dictionary
	with open(f"{out_path}", 'w+', encoding='utf-8') as f:
		yaml.dump(ds_config, f, default_flow_style=False)

if __name__ == '__main__':
	main()