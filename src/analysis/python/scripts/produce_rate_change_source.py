import pandas as pd
import numpy as np
import datetime
def main():
    pd.options.display.max_rows=10000
    start_date = datetime.datetime(1989, 7, 1)
    end_date=datetime.datetime(2006, 2, 1)
    dates = pd.read_csv("../../../derivation/python/output/meeting_derived_file.csv")
    rates = pd.read_excel("../../../collection/python/data/FRED_DFEDTAR.xls", skiprows=10)
    rates.columns = ['date', 'dfedtar']
    rates['shift'] = rates['dfedtar'].shift(1)
    rates['date'] = pd.to_datetime(rates['date'])
    rates = rates[(start_date <= rates.date) & (rates.date < end_date)]

    rates['change'] = rates['shift'] != rates['dfedtar']
    dates = dates[['end_date', 'event_type']]
    dates['date'] = pd.to_datetime(dates['end_date'])
    merge = pd.merge(rates, dates, on="date", how="left")
    #merge['event_shift'] = merge['event_type'].shift(1)
    merge['month'] = merge.date.dt.month
    merge['year'] = merge.date.dt.year

    merge['meeting'] = (merge['event_type'] == "Meeting")
    merge['meeting_shift'] = merge['meeting'].shift(1).fillna(False)
    merge['sch_conf_call'] = (merge['event_type'] == "Conference Call")
    merge['sch_conf_call_shift'] = merge['sch_conf_call'].shift(1).fillna(False)


    merge['meeting_change'] = (merge['change']) & (merge['meeting']\
                       |merge['meeting_shift'])
    merge['conf_call_change'] = (merge['change'] & ~(merge['meeting']\
                       |merge['meeting_shift']))


    monthly_grp = merge.groupby(["month","year"])

    monthly = monthly_grp.sum()
    monthly['change_m'] = ((monthly.change>0)&
                  (monthly.meeting_change==monthly.change))
    monthly['change_cc'] = ((monthly.change>0)&
                  (monthly.meeting_change==False))
    monthly['change_m_and_cc'] = ((monthly.change>0)&
                      (monthly.meeting_change>0)&
                      (monthly.meeting_change!=monthly.change))
    #print(monthly)
    monthly['d_meeting'] = ((monthly.meeting>0)\
                         |(monthly.meeting_shift>0))
    monthly['d_sch_conf_call'] = ((monthly.sch_conf_call>0)\
                               |(monthly.sch_conf_call_shift>0))

    monthly['unchanged_m'] = ((monthly.change==0)&
                                    (monthly.d_meeting==True)&
                                    (monthly.d_sch_conf_call==False)
                                     )
    monthly['unchanged_cc'] = ((monthly.change == 0) &
                                    (monthly.d_meeting == False) &
                                    (monthly.d_sch_conf_call == True)
                                    )
    monthly['unchanged_m_and_cc'] = ((monthly.change == 0) &
                                    (monthly.d_meeting == True) &
                                    (monthly.d_sch_conf_call == True)
                                    )
    monthly['unchanged_no_m_or_cc'] = ((monthly.change == 0) &
                                    (monthly.d_meeting == False) &
                                    (monthly.d_sch_conf_call == False)
                                    )
    monthly.loc[monthly["change_m"]==True,
                "Event"] = "Meeting"
    monthly.loc[monthly["change_cc"] == True,
                "Event"] = "Non-Meeting Event"

    monthly.loc[monthly["change_m_and_cc"] == True,
                "Event"] = "Meeting and Non-Meeting Event"

    monthly.loc[monthly["unchanged_m"] == True,
                "Event"] = "Meeting"
    monthly.loc[monthly["unchanged_cc"] == True,
                "Event"] = "Conference Call"
    monthly.loc[monthly["unchanged_m_and_cc"] == True,
                "Event"] = "Meeting and Conference Call"
    monthly.loc[monthly["unchanged_no_m_or_cc"]==True,
                "Event"] = "No Meeting or Conference Call"

    monthly["Number of Months"] = 1
    monthly["Event"] = monthly['Event'].fillna("")
    #print(monthly[monthly["Event"]==""])
    monthly["Rate Change"] = monthly.apply(lambda x:"Observed" if x.change>0 else "Not Observed",axis=1)

    pivot = monthly.pivot_table(monthly,index=["Rate Change","Event"],
                              aggfunc=len,margins=True).astype(int)[["Number of Months"]]
    #print(pivot)
    #print(pivot)
    pivot_i = pivot.reset_index()
    pivot_s = pivot_i.groupby("Rate Change").sum().reset_index()
    pivot_s['Event'] = pivot_s["Rate Change"]+" Total"
    #print(pivot_i)
    #print(pivot_s)
    output = pivot_i.merge(pivot_s,how="outer")\
        .sort_values(by="Rate Change",ascending=False).reset_index(drop=True)
    new_order = [0,2,1,3,5,4,6,7,8,9]
    output = output.reindex(new_order).reset_index(drop=True)
    output.loc[output['Rate Change'].duplicated(),"Rate Change"]=""
    output = output.drop_duplicates(subset=["Number of Months"])
    
    output_text = output.to_latex(index=False)
    output_text = output_text.replace("Not Observed","\\hline Not Observed",1)\
        .replace("All","\\hline\\hline All",1)
    #print(output_text)
    with open("../output/overleaf_files/rate_change_sources.tex",'w+') as f:
        f.write(output_text)


if __name__ == "__main__":
    main()