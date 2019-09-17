# FOMC Text Analysis Project
## Authors: Jose Luis Montiel Olea, Oliver Giesecke, Anand Chitale

### Purpose: This repository contains tools (Python and Matlab scripts), raw data and derived datasets that are primarily related to textual data produced in preparation of FOMC decisions.
## Organization:
The repository is organized as follows:
All relevant code and data is contained in the *src* folder

The *src* folder is broken down into three subfolders:

1. **Collection**: Contains tools for scraping, downloading, and extracting raw text from documents on the FOMC website.

2. **Derivation**: Contains tools that use the raw data and transform the data into a format that is suitable for the data analysis. 

3. **Analysis**: Contains tools that perform the data analysis, produces summary statistics and produces tables and figures for the draft.

Each of which contains the following grouped by programming language:
1. **Data**: Manually downloaded or modified files which must be read in (this is either raw data or manually produced data)
2. **Scripts**: Programs which produce some output
3. **Output**: Content generated by scripts


## Collection

This folder contains scripts used in order to read and download all documents from the FOMC website.

Key Files:
1. python/scripts/download_raw_doc_metadata.py:\
Reads through each page of the FOMC website (https://www.federalreserve.gov/monetarypolicy/fomc_historical_year.htm) and extracts meeting dates, available documents and the corresponding links by year. It produces the output file **raw_data.csv** which constitutes the *universe* of documents.

2. python/scripts/extract_derived_data.py:\
Reads in the raw_doc_metadata and produces a derived file derived_data.csv containing the following fields
['year', 'start_date', 'end_date', 'event_type','file_name', 'file_size','file_type', 'link', 'grouping','document_class']. This is a cleaned version of the previous file and adds information of the natural grouping of documents. This file can be considered as the reference file for available documents. 

3. python/scripts/perform_collection.sh:\
This is a shell scripts that executes all python scripts in the correct order. Apart from the two steps described above, it also downloads the documents from the website of the Federal Reserve Board and extracts the raw text from the .pdf, .html or other file types.

## Derivation
This folder contains scripts to extract meeting specific information. So far, it focuses on the extraction of policy alternatives from the ''Bluebook'' and the outcomes from the Statements.

Key Files:
1. src/derivation/python/scripts/obtain_bluebook_alternatives.py:\
Reads in the raw text of the bluebooks from collection/python/output/bluebook_raw_text and uses regular expressions to extract all sentence with the mentioning of a policy alternative. It exports extracted information to derivation/output/bluebook_alt_and_class_output.csv

2. src/derivation/python/scripts/produce_final_derived_file.py\
Reads in previous outbut and merges infromation with market information and meeting outcomes. This creates a final derived file, *final_derived_file.csv*, containing the following information:

start_date,end_date,event_type,statement_policy_change,statement_policy_action,d_statement,FFF_0_rate,FFF_1_rate,FFF_2_rate,FFF_3_rate,FFF_4_rate,FFF_5_rate,FFF_6_rate,wsj_article_count,nyt_article_count,ft_article_count,DFF_Before_meeting,DFEDTR_before,DFEDTR_end,bluebook_treatment_alt_a,bluebook_treatment_size_alt_a,bluebook_justify_alt_a,bluebook_treatment_alt_b,bluebook_treatment_size_alt_b,bluebook_justify_alt_b,bluebook_treatment_alt_c,bluebook_treatment_size_alt_c,bluebook_justify_alt_c,bluebook_treatment_alt_d,bluebook_treatment_size_alt_d,bluebook_justify_alt_d,bluebook_treatment_alt_e,bluebook_treatment_size_alt_e,bluebook_justify_alt_e,bluebook_comments,year

## Analysis
These scripts read in information from the derived output in order to produce figures, charts, graphs, and summary statistics.

Key Files:
1. src/analysis/python/scripts/extract_fed_targets_with_alternatives.py:\
Reads in derived alternative data from final_derived_data.csv in order to produce a time series of fed targets before and after each meeting, along with the rate change proposed by each alternative.

2. src/analysis/python/scripts/overleaf_production/produce_overleaf_files.sh:\
this shell script runs every file placed in the overleaf_production folder, exporting produced graphs, charts, and figures  overleaf_files output folder.
