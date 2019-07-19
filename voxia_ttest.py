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


def process_file(audio_fname, speakers_number, is_remote_file):
    # TODO check if voxia api is up and listening
    


    #if is_remote_file:
        # TODO send request to voxia API
        
        # TODO handle response (extract text only)

        # TODO 





def main():
    parser = argparse.ArgumentParser(description=
    """
    Test voxia audio transcription with specified audio file. Writes the processed
    text to file and, if a ground-truth is provided, prints the metrics results.
    If audio file is remote (stored at GS bucket), check config.json file.
    """)

    # main parser arguments. The order is respected, so change accordingly.
    parser.add_argument('AUDIO_FILE', type=str, help='filename, may be local or remote (check config.json)')
    parser.add_argument('SPEAKERS_N', type=str, help='number of speakers')
    parser.add_argument('-r', '--remote', action='store_true', help='AUDIO_FILE is remote (stored at GS)')
    parser.add_argument('-g', 'GT', type=str, required=False, help='compare result with ground truth text at file GT')

    args = parser.parse_args()
    audio_fname = args.AUDIO_FILE
    speakers_number = args.SPEAKERS_N
    is_remote_file = args.r
    if(args.g):
        gt_file = args.g

    # TODO load config

    process_file(audio_fname, speakers_number, is_remote_file)


if __name__ == "__main__":
    main()