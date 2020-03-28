import pandas as pd
import os
import re
import pprint
import shutil
import regex

    # Clean all the obvious typos
corrections ={'BAUGHWJV':'BAUGHMAN',
              'BOHNE':'BOEHNE',
              'EISEMENGER':'EISENMENGER',
              'GEITHER':'GEITHNER',
              'KIMBREL':'KIMEREL',
              'MATTINGLY': 'MATTLINGLY',
              'FORESTALL':'FORRESTAL',
              'GRENSPAN':'GREENSPAN',
              'GREESPAN':'GREENSPAN',
              'GREENPSAN':'GREENSPAN',
              'GREENSPAN,':'GREENSPAN',
              'GREENPAN':'GREENSPAN',
              'McANDREWS':'MCANDREWS',
              'MCDONUGH':'MCDONOUGH',
              'MOSCOW':'MOSKOW',
              'MORRIS':'MORRRIS',
              'MONHOLLAN':'MONHOLLON',
              'MILIER':'MILLER',
              'MILER':'MILLER',
              'SCWLTZ':'SCHULTZ',
              'SCHELD':'SCHIELD',
              'WILLZAMS':'WILLIAMS',
              'WALLJCH':'WALLICH',
              'VOLCKFR':'VOLCKER',
              'VOLCRER':'VOLKER',
              'ALLISON for':'ALLISON',
              'ALTMA"':'ALTMANN',
              'B A U G W':'BAUGW',
              'BIES (as read by Ms':'BIES',
              'BLACK &':'BLACK',
              'MAYO/MR':'MAYO',
              'Greene':"GREENE",
              'CROSS,':'CROSS',
              'GREENSPAN,':'GREENSPAN',
              'HOSKINS,':'HOSKINS',
              'MACCLAURY':'MACLAURY',
              'MORRRIS':'MORRIS',
              "O'CONNELL":'O’CONNELL',
              'SOLOMON]':'SOLOMON',
              'TRUMAN-':'TRUMAN',
              'VOLCKER,':'VOLCKER',
              'VOLKER,':'VOLCKER',
              'WALLlCH':'WALLICH',
              '[BALLES]':'BALLES',
              '[GARDNER]':'GARDNER',
              '[KICHLINE]?':'KICHLINE',
              '[PARDEE]':'PARDEE',
              '[ROOS]':'ROOS',
              '[STERN':'STERN',
              '[WILLES]':'WILLES',
              'ŞAHIN':'SAHIN',
              '[STERN(?)':'STERN',
              '[STERN]':'STERN',
              'GRALEY':'GRAMLEY',
              'ALTMA”':'ALTMANN'}

              
            
                  
def name_corr(val):
    val = re.sub("[^A-Z]","",val)

    if val in corrections:
        return corrections[val]
    else:
        return val

def generate_speaker_corpus(separation_token_file):

    interjections = pd.read_excel(separation_token_file)
    meeting_df = pd.read_csv("../../../derivation/python/output/meeting_derived_file.csv")

    

    cc_df = meeting_df[meeting_df.event_type=="Meeting"]
    cc_df['end_date'] = pd.to_datetime(cc_df['end_date'])
    cc_df['Date'] = pd.to_datetime(cc_df['start_date'])
    cc_df = cc_df[['Date','end_date',"start_date"]]
    cc_df['date_ind'] = cc_df['end_date'].dt.strftime("%Y%m").astype(int)
    cc_df = cc_df[(cc_df['date_ind']>198707)&(cc_df['date_ind']<200602)]
    interjections['Speaker'] = interjections['Speaker'].apply(name_corr)
    interjections = interjections.rename(columns={"Date":"date_ind"})
    interjections.loc[interjections['Speaker']=="D","Speaker"] = "LINDSEY"
    interjections[interjections['Speaker']=="D"] = interjections[interjections['Speaker']=="D"].apply(lambda x:x.replace("lindsey ",""))

    speaker_file = pd.merge(cc_df,interjections,on="date_ind")[
        ["Date","Speaker","Section","content","start_date","end_date"]]
    speaker_file = speaker_file.fillna("")


    speaker_groups = speaker_file.groupby(["Date","Speaker","Section"])['content'].\
        apply(lambda x: "%s" % " ".join(x)).reset_index()

    #print(speaker_file)
    if not os.path.exists("../output/speaker_data"):
        os.mkdir("../output/speaker_data")
    speaker_file.to_csv("../output/speaker_data/speaker_corpus.csv",index=False)
    speaker_file.to_pickle("../output/speaker_data/speaker_corpus.pkl")
    return speaker_file

def generate_speaker_files(speaker_statements):
    speakers = [speaker for speaker in set(speaker_statements["Speaker"])]
    print("Number of speakers:{}".format(len(speakers)))
    count = 0
    for speaker in speakers:
        print("Currently working on statements for speaker {} of {}. Name:{}".format(count,len(speakers),speaker))
        speaker_df = speaker_statements[speaker_statements["Speaker"]==speaker]
        speaker_path = "{}/{}".format("../output/speaker_data",speaker)
        if not os.path.exists(speaker_path):
            os.mkdir(speaker_path)
        speaker_df[['Date','content']].to_csv("{}/{}_{}".format(speaker_path,speaker,"statements_by_meeting.csv"))
        speaker_list = list(speaker_df["content"])
        with open("{}/{}_{}".format(speaker_path,speaker,"corpus.txt"),"w+") as f:
            f.write(" ".join(speaker_list))
        count+=1

def main():
    speaker_statements = generate_speaker_corpus("../data/FOMC_token_separated_col_new.xlsx")
    generate_speaker_files(speaker_statements)


if __name__ == "__main__":
    main()
    
# =============================================================================
# ## Do some checks:  
# with open('../../output/data.json', 'r') as speakerids:
#     speakerid = json.load(speakerids)
#     
# speakerlist = [ x.lower() for x in speaker_statements["Speaker"].unique().tolist()]
# 
# for key,value in speakerid.items():
#     if key.lower() not in speakerlist:
#         print(key)
#     else:
#         print('in list')
# 
# =============================================================================

