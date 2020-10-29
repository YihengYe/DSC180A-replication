#! /usr/bin/env python

import sys
import json

from etl import donwload_data



def main(targets):
    if 'data' in targets:
        with open('config/data-params.json') as fh:
            data_cfg=json.load(fh)
        donwload_data(data_cfg['links'], data_cfg['outpath'])
    return







if __name__ == "__main__":
    targets=sys.argv[1: ]
    main(targets)