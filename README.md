# TGM DiffSinger Tools
In this repo, you'll find assorted DiffSinger tools I've created that I don't feel like making their own repo for.

## csv2lab.py

This tool can convert DiffSinger transcriptions (CSV, new format only) into HTK labels (that can be used in wavesurfer, etc.)

Requirements:
```
click
```

How to use
```
python csv2lab.py -i {path_to_transcription.csv} -o {path_to_export}
```
By default, it will be exported to a folder called "wavs".

Click help output:
```
Usage: csv2lab.py [OPTIONS]

Options:
  -i, --csv_path TEXT  Path to DiffSinger Transcription File.  [required]
  -o, --out_path TEXT  Path to Export labels.
  --help               Show this message and exit.
```
