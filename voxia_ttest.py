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
import json
import argparse
from pathlib import Path


SCRIPT_DIR = Path(os.path.realpath(__file__)).parent
CONFIG_FILE = SCRIPT_DIR / "config.json"


def evaluate_transcription(audio_fname, transcribed_str, gt_fname):
    return 0


def request_transcription(remote_path, speakers_number, config_dict):
    # TODO check if voxia api is up and listening

    # TODO send transcribe request to voxia API
    
    # TODO handle response (extract text only)

    # TODO return response

    return 0


def process_file(audio_fname, speakers_number, config_dict, is_remote_file, gt_fname):
    remote_path = ""
    #if is_remote_file:
        # TODO assemble remote path
        # remote_path = ...

    #else: # local file
        # TODO upload file to bucket using gsutil, loading paths from config dict

        # TODO assemble remote path

    transcribed_str = request_transcription(remote_path, speakers_number, config_dict)

    out_transcribed_fname = Path(audio_fname).stem + "_transcribed.txt"
    out_trans_file = open(out_transcribed_fname, "w")
    out_trans_file.write(transcribed_str)
    out_trans_file.close()

    if(gt_fname):
        eval_result_str = evaluate_transcription(audio_fname, transcribed_str, gt_fname)
        
        print(eval_result_str)
        
        out_eval_fname = Path(audio_fname).stem + "_eval.txt"
        out_eval_file = open(out_eval_fname, "w")
        out_eval_file.write(eval_result_str)
        out_eval_file.close()


def main():
    parser = argparse.ArgumentParser(description=
    """
    Test voxia audio transcription with specified audio file. Writes the processed
    text to file and, if a ground-truth is provided, prints the metrics results.
    If audio file is remote (stored at GS bucket), check config.json file.
    """)

    # main parser arguments. The order is respected, so change accordingly.
    parser.add_argument('AUDIO_FILE', metavar='<AUDIO_FILE>', type=str, help='filename, may be local or remote (check config.json)')
    parser.add_argument('SPEAKERS_N', metavar='<SPEAKERS_N>', type=str, help='number of speakers')
    parser.add_argument('-r', '--remote', action='store_true', help='AUDIO_FILE is remote (stored at GS)')
    parser.add_argument('-g', metavar='<GT_FILE>', type=str, required=False, help='compare result with ground truth text at file GT_FILE')

    args = parser.parse_args()
    audio_fname = args.AUDIO_FILE
    speakers_number = args.SPEAKERS_N
    is_remote_file = args.remote
    gt_fname = args.g # may be null (=None)
    config_dict = json.load(open(SCRIPT_DIR / "config.json", "r"))

    process_file(audio_fname, speakers_number, config_dict, is_remote_file, gt_fname)


if __name__ == "__main__":
    main()