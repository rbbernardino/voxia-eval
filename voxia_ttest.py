#! /usr/bin/env python3
"""
Test voxia audio transcription with specified audio file. Writes the processed
text to file and, if a ground-truth is provided, prints the metrics results.
If audio file is remote (stored at GS bucket), check config.json file.
    ./voxia_ttest.py [-r][-e <GT>] <AUDIO_FILE> <SPEAKERS_N>
    INPUT:
        <AUDIO_FILE>  - filename, may be local or remote (check config.json)
        <SPEAKERS_N>  - number of speakers
    OPTIONS:
        -r, --remote    - whether the file is remote or not (default is false)
        -e <GT>         - evaluate result comparing with provided ground-truth
    OUTPUT:
        FNAME_trascribed.txt - the transcribed text
        FNAME_eval.txt       - output of the metrics comparing GT x transcribed
"""

import os
import sys
import json
import argparse
import requests
from subprocess import run
from subprocess import PIPE
from subprocess import CalledProcessError
from pathlib import Path
from trancription_metrics import CompareTexts


SCRIPT_DIR = Path(os.path.realpath(__file__)).parent
CONFIG_FILE = SCRIPT_DIR / "config.json"
API_PATH = "valid_gs"
RESULTS_PATH = Path("results")


def prepare_outdir(outdir_path: Path):
    if outdir_path.exists():
        if outdir_path.is_file():
            print('ERROR: output path is a file')
    else:
        outdir_path.mkdir(parents=True)


def str_to_file(out_path: Path, in_str):
    out_file = open(str(out_path), "w")
    out_file.write(in_str)
    out_file.close()


def upload_to_bucket(file_path: Path, remote_path: str):
    # OBS: gsutil cp will print progress to stderr by design, commands like
    # "ls" will print to stdout
    cmd = ["gsutil", "cp", str(file_path), remote_path]
    try:
        rslt = run(cmd, stderr=sys.stdout)
        rslt.check_returncode()
    except CalledProcessError as err:
        print('ERROR when uploading file to gs bucket:', rslt.stderr.decode('utf-8'))
        exit(1)


def evaluate_transcription(transcribed_str, gt_fname):
    text_comparator = CompareTexts()
    gt_str = open(gt_fname, "r").read()
    return text_comparator.compare_texts(transcribed_str, gt_str)


def request_transcription(remote_path, speakers_number, config_dict):
    voxia_ip = config_dict['voxia_ip']
    voxia_port = config_dict['voxia_port']
    voxia_url = "http://" + voxia_ip + ":" + voxia_port + "/" + API_PATH
    
    request_body = {
        "gs": remote_path,
        "transcription_id": "1234",
        "qtd_of_speakers": int(speakers_number)
    }

    try:
        request_result = requests.post(voxia_url, json=request_body)
    except requests.exceptions.ConnectionError as err:
        print("ERROR, couldn't connect to voxia, check config.json and if the server is running.")
        exit(1)

    if request_result.status_code != 200:
        print("ERROR: request returned " + str(request_result.status_code))
        print("----------------------")
        print(request_result.text)
        exit(1)

    result_json = request_result.json()
    transcribed_str = result_json['text_summarization'][0]
    return transcribed_str


def process_file(audio_fname, speakers_number, config_dict, is_remote_file, gt_fname):
    prepare_outdir(RESULTS_PATH)
    remote_path = ""
    if is_remote_file:
        print("Remote file selected")
        remote_path = config_dict['bucket_url'] + "/" + audio_fname
    else:
        # local file, upload to bucket and set "remote_path" variable
        print("Local file selected, will upload before processing...")
        print("----------------------------------------")
        file_path = Path(audio_fname)
        remote_path = config_dict['bucket_url'] + "/" + config_dict['bucket_new_dir'] + file_path.name
        upload_to_bucket(file_path, remote_path)
        print("----------------------------------------\n")

    print("Requesting transcription...")
    transcribed_str = request_transcription(remote_path, speakers_number, config_dict)

    out_transcribed_fname = Path(audio_fname).stem + "_transcribed.txt"
    str_to_file(RESULTS_PATH / out_transcribed_fname, transcribed_str)
    print("Transcription completed, saved to '{}'".format(RESULTS_PATH / out_transcribed_fname))

    if(gt_fname):
        print("\nGT file provided, will evaluate results with several metrics...")
        eval_result_str = evaluate_transcription(transcribed_str, gt_fname)
        print(eval_result_str)
        out_eval_fname = Path(audio_fname).stem + "_eval.txt"
        str_to_file(RESULTS_PATH / out_eval_fname, eval_result_str)
        print("Results saved to '{}'".format(RESULTS_PATH / out_eval_fname))


def main():
    parser = argparse.ArgumentParser(description="""
    Test voxia audio transcription with specified audio file. Writes the processed
    text to file and, if a ground-truth is provided, prints the metrics results.
    If audio file is remote (stored at GS bucket), check config.json file.
    """)

    # main parser arguments. The order is respected, so change accordingly.
    parser.add_argument('AUDIO_FILE', metavar='<AUDIO_FILE>', type=str,
                        help='filename, may be local or remote (check config.json)')
    parser.add_argument('SPEAKERS_N', metavar='<SPEAKERS_N>',
                        type=str, help='number of speakers')
    parser.add_argument('-r', '--remote', action='store_true',
                        help='AUDIO_FILE is remote (stored at GS)')
    parser.add_argument('-g', metavar='<GT_FILE>', type=str, required=False,
                        help='compare result with ground truth text at file GT_FILE')

    args = parser.parse_args()
    audio_fname = args.AUDIO_FILE
    speakers_number = args.SPEAKERS_N
    is_remote_file = args.remote
    gt_fname = args.g  # may be null (=None)
    config_dict = json.load(open(SCRIPT_DIR / "config.json", "r"))

    process_file(audio_fname, speakers_number, config_dict, is_remote_file, gt_fname)


if __name__ == "__main__":
    main()
