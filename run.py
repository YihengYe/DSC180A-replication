#! /usr/bin/env python

import sys
import json

from etl import donwload_data, extracter, ld_to_csv



def main(targets):
    if 'data' in targets:
        with open('config/data-params.json') as fh:
            data_cfg=json.load(fh)
        donwload_data(data_cfg['links'], data_cfg['outpath'])
        extracter(data_cfg['outpath'])
        ld_to_csv('data/unzipped')
    return







if __name__ == "__main__":
    targets=sys.argv[1: ]
    main(targets)