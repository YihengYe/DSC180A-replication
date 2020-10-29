# DSC180A-replication

This is the replication project for DSC180A, B03 GROUP4

Project Team Member:
- Yiheng Ye, yiy291@ucsd.edu
- Kai-Ling Peng, kap038@ucsd.edu


Requirements:
- python 3.8
- pandas 1.1.0

CSV structure:
the csvs at data/csvs contains those coloumns: article (the article where edit happend), time , revert(0 means no revert, 1 means revert), version, and user (editor). Each contains 100000 rows for the sake of memory consumption. 

Code, Purpose, and Guideline:

- run.py: getting light-dump data and transfered them into csvs that are 100000 rows each from WikiWarMonitor(http://wwm.phy.bme.hu/), 
          use "python run.py data" (line inside the quotation marks) to run it. After running it, the zip files downloaded are 
          at data/raw, the unzipped text files are at data/unzipped, and the csvs are at the data/csvs, which contains files
          that named by every ~wiki.zip downloaded with their articles data in csv form.

- elt.py: the library for the data pipeline, see the documentation for detailed functions of every function writtened. Basically
          these functions are used to fulfill the job done in run.py.

- config/data-params.json: it stores the links of the source data as well as the output path for raw data.

- code in src/data: the source code to fulfill the functions about processing data. The current usable files are download.py(
                    download lightdump data to data/raw) and light_dump_to_csv.py(unzipp data and save them into csvs), and
                    their are used in elt.py.