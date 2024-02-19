# TGM DiffSinger Tools
In this repo, you'll find assorted DiffSinger tools I've created that I don't feel like making their own repo for.

## csv2lab.py

This tool can convert DiffSinger transcriptions (CSV, new format only) into HTK labels (that can be used in wavesurfer, etc.)

Requirements:

```click```

How to use

```python csv2lab.py -i {path_to_transcription.csv} -o {path_to_export}```

By default, it will be exported to a folder called "wavs".

Click help output:
```
Usage: csv2lab.py [OPTIONS]

Options:
  -i, --csv_path TEXT  Path to DiffSinger Transcription File.  [required]
  -o, --out_path TEXT  Path to Export labels.
  --help               Show this message and exit.
```

## val_config_tool.py

This tool can automatically create the speaker part of the DiffSinger config. This requires DiffSinger format data (transcriptions.csv, wavs folder). It will automatically account for data being inside of "raw" folder, ensuring the name of the speaker is proper according to the folder.

Requirements:

```click```

How to use:

```python val_config_tool.py -i {path_to_raw_data}```

Click help output:
```
Usage: val_config_tool.py [OPTIONS]

  Creates validation file list for DiffSinger config.

Options:
  -i, --in_path TEXT     Path of raw DS Voice Data.  [required]
  -v, --val_num INTEGER  Amount of Validation files to choose per speaker.
                         Default: 5
  -o, --out_path TEXT    Path to export to. Default: 'diffsinger_config.yaml'
  --help                 Show this message and exit.
```

Output:
```
num_spk: 2
raw_data_dir:
- data\canary_arc\raw
- data\canary_spark
speakers:
- canary_arc
- canary_spark
test_prefixes:
- 0:intergalactia_seg012
- 0:cny_arc_t206_04_seg001
- 0:cny_arc_t2_10_seg001
- 0:cny_arc_t2_11_seg002
- 0:what_you_need_2_seg001
- 1:cny_spark_11_seg000
- 1:cny_spark_25_seg000
- 1:cny_spark_07_seg003
- 1:cny_spark_man_01_seg000
- 1:cny_spark_14_seg002
```
