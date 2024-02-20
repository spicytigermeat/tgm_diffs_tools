import glob
import sys
import os
import click
from pathlib import Path as P

@click.command(help='Tool to add aliases to HTK style singing labels.')
@click.option(
	'--in_dir',
	'-i',
	type=str,
	required=True,
	help='Path to alias labels'
)
@click.option(
	'--alias',
	'-a',
	type=str,
	required=True,
	help='Alias to add to the end of labels.'
)
@click.option(
	'--out_dir',
	'-o',
	type=str,
	required=False,
	default='out',
	help='Path to export labels to.'
)
@click.option(
	'--excepts',
	'-e',
	type=str,
	required=False,
	help='Phonemes to ignore, seperated by a comma with no space.'
)

def main(in_dir: str, alias: str, out_dir: str, excepts: str):

	# ensure out directory exists
	if not os.path.exists(out_dir):
		try:
			os.mkdir('out')
		except:
			print('Unable to create out directory.')
			sys.exit()

	#initialize variables
	exceptions = [
		'AP', 'SP', 'pau', 'sil', 'br',
		'cl', 'Edge', 'GlottalStop', 'vtrash', 'ctrash',
		'trash', 'TRS', 'axh', 'exh'
	]

	# add any user defined exceptions
	if excepts != None:
		new_excepts = [ph for ph in excepts.rstrip().split(',')]

		for i, ph in enumerate(new_excepts):
			exceptions.append(ph)

	for lab in glob.glob(f"{P(in_dir)}/**/*.lab", recursive=True):

		label = []

		# load label as a list with nested lists
		with open(lab, 'r', encoding='utf-8') as l:
			for line in l:
				x1, x2, ph = line.rstrip().split(' ')
				label.append([x1, x2, ph])

		# run the aliaser, check for exceptions
		for i in range(len(label)):
			if label[i][2] in exceptions:
				pass
			else:
				label[i][2] = f"{label[i][2]}{alias}"

		# write new label
		with open(f"{P(out_dir, lab)}", 'w+', encoding='utf-8') as o:
			for i in range(len(label)):
				o.write(f"{label[i][0]} {label[i][1]} {label[i][2]}\n")

		print(f"Aliased {lab}.")


if __name__ == '__main__':
	main()