# voxia-tests
A simple test suite for Voxia. Transcribe an audio file and write the output to
file. Optionally, if a ground-truth text is provided, it's possible to evalute
with common metrics. It is also possible to provide a local file that will be
uploaded and further processed. 

## Requirements
1. Voxia API running with IP and port specified by config.json
2. `gsutil` properly set (account must have permission to voxia bucket)

## Setup gsutil
- Follow the steps at https://cloud.google.com/storage/docs/gsutil_install?hl=pt-br#deb

## Usage
```
usage: voxia_test.py [-h] [-r] [-g <GT_FILE>] <AUDIO_FILE> <SPEAKERS_N>

positional arguments:
  <AUDIO_FILE>  filename, may be local or remote (check config.json)
  <SPEAKERS_N>  number of speakers

optional arguments:
  -h, --help    show this help message and exit
  -r, --remote  AUDIO_FILE is remote (stored at GS)
  -g <GT_FILE>  compare result with ground truth text at file GT_FILE

NOTE: when uploading, existing files with same path will be overwritten
```

## Details on Usage
1. **Local audio file**
	- File stored at local path
	- FILE_PATH: `data/policial_40s.flac`
	- NUMBER_OF_SPEAKERS: 2
```bash
./voxia_test.py data/policial_40s.flac 2
```

2. **Remote audio file**
	- File stored at bucket of google cloud storage
	- GS_PATH: `test_files/policial_40s.flac`
	- NUMBER_OF_SPEAKERS: 2
	- set option: `-r`
```bash
./voxia_test.py -r test_files/policial_40s.flac 2
```

3. **Remote/Local file + measure distance from Ground Truth**
	- Same as above for file path and number of speakers
	- set option `-g` and specify `GT_PATH`, which is a .txt file
```bash
./voxia_test.py -r test_files/policial_40s.flac 2 -g data/transc_policial_40s.txt
```

## Config File
- **OBS:** `bucket_new_dir` is the folder where uploaded files will be saved

```json
{
    "voxia_ip": "127.0.0.1",
    "voxia_port": "5000",
    "bucket_url": "gs://audiosmppe",
    "bucket_new_dir": "test_files"
}
```

## Further Notes
- When uploading, if a file with the same name is already present, it will be overwritten
