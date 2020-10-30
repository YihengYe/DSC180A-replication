#! /usr/bin/env python

import sys
import json

from etl import *


def main(targets):
    if 'data' in targets:
        
        with open('config/data-params.json') as fh:
            data_cfg=json.load(fh)
        
        #xml to light dump
        pages = soupify_xml(data_cfg['xml_path'])
        dframes = xml_to_df(pages)
        xml_to_light_dump(dframes, 'data/unzipped')
        
        #process light dump
        donwload_data(data_cfg['links'], data_cfg['outpath'])
        extracter(data_cfg['outpath'])
        ld_to_csv('data/unzipped')
    return







if __name__ == "__main__":
    targets=sys.argv[1: ]
    main(targets)