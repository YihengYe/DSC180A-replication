#! /usr/bin/env python

import sys
import json

from etl import *
from eda import *


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

    if 'eda' in targets:
        with open('config/eda-params.json') as fh:
            eda_cfg=json.load(fh)
            routes=get_csvs_route(eda_cfg['csv_path'])
            for i in routes:
                for j in eda_cfg['content']:
                    generate_result(i,j)
    
    if 'mstats' in targets:
        #calculate m stats here
        pass

    return







if __name__ == "__main__":
    targets=sys.argv[1: ]
    main(targets)