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

- run.py: Turns XML data into light dump TXT files. Transfers light dump data into CSVs that are around 100,000 rows each. 
          Use "python run.py data" (line inside the quotation marks) to run it. The zipped file downloads are at data/raw, light 
          dump data will be stored in data/unzipped, and processed CSVs are at data/csvs, which contains article edit data in csv 
          form.

- elt.py: the library for the data pipeline, see the documentation for detailed functions of every function writtened. Basically
          these functions are used to fulfill the job done in run.py.

- config/data-params.json: it stores the links of the source data as well as the output path for raw data.

- code in src/data: the source code to fulfill the functions about processing data. The current usable files are
                    xml_to_light_dump.py (turns xml into light dump data), download.py(
                    download lightdump data to data/raw), and light_dump_to_csv.py(unzipp data and save them into csvs).

## Responsibilities:
- Yiheng Ye set up the structure of the project and the structure of run.py. He also wrote download.py and light_dump_to_csv.py and put then into etl.py to download light-dump data and store them into the csv format.
- Kai-Ling Peng provided reference notebooks for processing light dump data. She wrote code for turning XML data into light dump text files (xml_to_light_dump.py).