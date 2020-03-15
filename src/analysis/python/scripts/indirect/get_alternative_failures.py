import os
import pandas as pd
def get_alternative_failures():
    files = os.listdir("../../data/alternatives_corpora")
    failures = pd.DataFrame()
    for fname in files:
        if ".txt" not in fname:
            continue
        with open("../../data/alternatives_corpora/"+fname) as f:
            text = f.read()
            if len(text.strip().replace("\n","")) == 0:
                failures = failures.append({"Date":fname.replace(".txt","")},ignore_index=True)
    failures = failures.sort_values(by="Date").reset_index(drop=True)
    print(failures)
    failures.to_csv("../../output/alternative_failures.csv")
if __name__ == "__main__":
    get_alternative_failures()