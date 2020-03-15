import pandas as pd
import os
import re

def main():
    df = pd.DataFrame()
    os.chdir("../data/alternatives_corpora")
    for filename in os.listdir():
        if ".txt" not in filename:
            continue
        alternatives = {'a':[],'b':[],'c':[],'d':[]}
        with open(filename) as f:
            for line in f.readlines():
                if line.strip():
                    split = re.split("[a-z]\s[A-Z]{3,4}\s\d*",line.strip(),1)
                    if len(split)>1:
                        alt = line.strip()[0]
                        alternatives[alt].append(split[1])
        to_append = {
            "date":filename.split(".txt")[0],
        }
        for alternative in alternatives.keys():
            to_append["alt {} corpus".format(alternative)] = "\n".join(alternatives[alternative])
        df = df.append(to_append,ignore_index=True)
    alt_corpus_df = df.sort_values(by="date").reset_index(drop=True)



    label_df = pd.read_csv("../../output/fed_targets_with_alternatives.csv")

    label_df = label_df[
        [
            "date",
            "decision",
            "bluebook_treatment_size_alt_a",
    "bluebook_treatment_size_alt_b",
    "bluebook_treatment_size_alt_c",
    "bluebook_treatment_size_alt_d",
    "bluebook_treatment_size_alt_e"
        ]
    ]

    label_df['date'] = pd.to_datetime(label_df['date'])
    alt_corpus_df['date'] = pd.to_datetime(alt_corpus_df['date'])

    label_df = label_df[(label_df.date.dt.year>1987)&(label_df.date.dt.year<2009)]
    alt_corpus_df = alt_corpus_df[(alt_corpus_df.date.dt.year>1987)&(alt_corpus_df.date.dt.year<2009)]

    label_df['month'] = label_df.date.dt.month
    label_df['year'] = label_df.date.dt.year

    alt_corpus_df['month'] = alt_corpus_df.date.dt.month
    alt_corpus_df['year'] = alt_corpus_df.date.dt.year


    print(len(alt_corpus_df))
    print(len(label_df))
    #print(pd.concat([label_df[['month','year']],alt_corpus_df[['month','year']]]).drop_duplicates(keep=False))


    #REMOVE DUPLICATE DATE ON SEPTEMBER 15th 2003
    #print(len(label_df))
    repeat = label_df[label_df[['month','year']].duplicated()]
    #print(repeat)
    label_df = label_df[label_df.date!=pd.to_datetime("2003-09-15")]
    #print(label_df[(label_df.date.dt.year==2003)&(label_df.date.dt.month==9)])

    indices = (pd.concat([label_df[['month','year']],alt_corpus_df[['month','year']]]).drop_duplicates(keep=False))

    #print(indices)
    #print("="*50)
    label_indices = indices[0:len(indices)//2]
    alt_indices = indices[len(indices)//2:]
    #print(label_indices)
    #print(alt_indices)

    #FIX DATES WHICH APPEAR AT END OF MONTH
    #date_revisions = {'1992-06-30':'1992-07-01','1995-01-31':'1995-02-01','1998-06-30':'1998-07-01'}
    #print(list(date_revisions.keys())[0])
    #print(alt_corpus_df[ alt_corpus_df.date == list(date_revisions.keys())[0]])


    for label_index, alt_index in zip(label_indices.index,alt_indices.index):
        print(f'Label Index:{label_index}')
        print(f'Alt Index:{alt_index}')
        #print(alt_corpus_df.loc[alt_index,"date"])
        #print(label_df.loc[label_index,"date"])
        alt_corpus_df.loc[alt_index,"date"] = label_df.loc[label_index,"date"]

    label_df['month'] = label_df.date.dt.month
    label_df['year'] = label_df.date.dt.year

    alt_corpus_df['month'] = alt_corpus_df.date.dt.month
    alt_corpus_df['year'] = alt_corpus_df.date.dt.year
    #print(len(alt_corpus_df))
    #print(len(label_df))
    #print(pd.concat([label_df[['month','year']],alt_corpus_df[['month','year']]]).drop_duplicates(keep=False))


    alt_corpus_df = alt_corpus_df[[x for x in alt_corpus_df.columns if x!="date"]]
    merge_df = pd.merge(label_df,alt_corpus_df,on=['month','year'])

    merge_df = merge_df[['date', 'alt a corpus','bluebook_treatment_size_alt_a',
                     'alt b corpus','bluebook_treatment_size_alt_b',
                     'alt c corpus','bluebook_treatment_size_alt_c',
                     'alt d corpus','bluebook_treatment_size_alt_d',
                     'decision'
                    ]]
    #print(len(merge_df))

    merge_df.to_csv("../../output/alternative_outcomes_and_corpus.csv")
main()