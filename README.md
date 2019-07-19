# voxia-tests
Voxia tests to improve transcription quality

## Requirements
1. voxia API running, listening on port 5000
2. `gsutil` properly set (account must have permission to voxia bucket)
3. voxia similarities must be properly set at `config.json`

## Setup gsutil

- **account:** cacl@cin.ufpe.br

```bash
sudo apt install gsutil
gcloud auth login
# login with cacl@cin.ufpe.br
```

## How it works
- voxia api route: `POST 127.0.0.1:5000/valid_gs`

Example Body:

```
{
	"gs": "gs://audiosmppe/bernardino/clodoaudo_bad_1min.wav",
	"transcription_id": "1234",
	"qtd_of_speakers": 3
}
```

## How to use
Provide either an audio already present in the gs bucket or a local file that
will be uploaded for further processing.

> **NOTE:** if a file with the same name is already present, it won't be
> replaced. To replace, specify "-r" option.


- **IN:** AUDIO_FILE or GS_PATH
