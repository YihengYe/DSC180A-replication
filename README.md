# DSC180A-replication

This is the replication project for DSC180A, B03 GROUP4

### Project Team Members:
- Yiheng Ye, yiy291@ucsd.edu
- Kai-Ling Peng, kap038@ucsd.edu

### Requirements:
- python 3.8
- pandas 1.1.0

### CSV Structure:
After running run.py, the CSV files at data/csvs contains the following coloumns: 

- article: the article where edit happend
- time: timestamp of edit
- revert: 0 if not a revert, 1 if edit was a revert
- version: index number of edit version, corresponds to original version if edit was a revert
- user: username of the editor, or IP address

Each csv contains around 100000 rows for the sake of memory consumption. 

### Code, Purpose, and Guideline:

- run.py: If target='data': Turns XML data into light dump TXT files. Transfers light dump data into CSVs that are around 5000,000 rows each. 
          Use "python run.py data" (line inside the quotation marks) to run it. The zipped file downloads are at data/raw, light 
          dump data will be stored in data/unzipped, and processed CSVs are at data/csvs, which contains article edit data in csv 
          form.

          If target='eda' (after use "data"): Reads csv files wiki by wiki. Outputs descriptions of edit frequency,revert frequency, and revert/edit ratio
          per specific group ('content') given (article,user, bots, day). Draws plots of edit frequency,revert frequency with "content" given.
          Draws histogram of revert/edit ration with "content" given.

          If target='mstats':Generates M-statistic calculated by data downloaded.

          If target='test': Runs test program about data, eda and mstats with the testdata provided

- elt.py: the library for the data pipeline, see the documentation for detailed functions of every function writtened. Basically
          these functions are used to fulfill the job done in run.py.

- eda.py: the library for data eda. see the documentation for detailed functions of every function writtened. Basically
          these functions are used to fulfill the job done in run.py.

- calc_M.py: the library for calculating M-statistics from light dumps. These functions are used to calculate M statistics and
             perform EDA on the calculated M results. 

- config/data-params.json: it stores the links of the source data as well as the output path for raw data.
- config/eda-params.json: it stores the links of the csv data as well as the output path for eda results.
- config/calculation-m-params.json: it stores the links of the input light dump data as well as the output path for eda results 
                                    for M calculations.

- code in src/data: the source code to fulfill the functions about processing data. The current usable files are
                    xml_to_light_dump.py (turns xml into light dump data), download_ld_zip.py(
                    download lightdump data to data/raw), light_dump_to_csv.py(unzipp data and save them into csvs),
                    eda.py(fullfil the eda function described in run.py), and calc_M.py (to calculate M statistics and perform EDA 
                    on calculated data.

## Responsibilities:
- Yiheng Ye set up the structure of the project and the structure of run.py. He also wrote download_ld_zip.py and light_dump_to_csv.py and put then into etl.py to download light-dump data and store them into the csv format. After that, he writes eda code (eda.py) to perform data eda on csv files.
- Kai-Ling Peng provided reference notebooks for processing light dump data. She wrote code for turning XML data into light dump text files (xml_to_light_dump.py). She wrote code for calculating M-stats on Wikipedia light dump data and performed EDA on calculated M-statistics.