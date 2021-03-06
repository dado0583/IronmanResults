from athletes.AthleteLoader import Results
from athletes.Results import Division
import pandas as pd
import numpy as np

all_results = Results()

def findAllResults():
    return all_results.get_results()

def findAthleteResults(name:str, is_regex:bool = False):
    df = all_results.get_results()
    if is_regex:
        df = df[df['name'].str.match(name)]
    else:
        df = df[df['name'].str.contains(name)]

    return df

def findFastResults():
    df = all_results.get_results()
    #We're removing athletes with slow times because we're not going to need to look at them
    #for predicting who is worth watching at an upcoming race.
    a = df.ix[((df['overallTime'] < pd.Timedelta('11:45:00')) & (df['overallTime'] > pd.Timedelta('07:20:00')) & (~df['raceName'].str.contains("70.3")))]
    b = df.ix[((df['overallTime'] < pd.Timedelta('5:45:00')) & (df['overallTime'] > pd.Timedelta('3:20:00')) & (df['raceName'].str.contains("70.3")))]
    
    return pd.concat([a,b])

def findFastestResults(breach:int = 15):
    df = all_results.get_results()
    #Finding the fastest athlete's per race. We'll need to figure out how to separate out pros and non-pros
    df = df.sort_values(by='overallTime', ascending=True).head(n=breach)

    return df

def findResultsForAG(div:Division):
    df = all_results.get_results()
    #Finding the fastest athlete's per race. We'll need to figure out how to separate out pros and non-pros
    df = df[df['currentAge'].between(div.lowAge, div.highAge)]

    return df

def cross_ref_world_champ_ties():
    df = findFastResults()

    non_worlds = df[~df['raceName'].str.contains("world")]

    non_worlds['yearOfRace'] = pd.DatetimeIndex(non_worlds['raceDate']).year
    non_worlds['yearOfRace'] = pd.DatetimeIndex(non_worlds['raceDate']).month

    print(non_worlds['yearOfRace'].head())
    


def test():
    #TODO: Move into testing suite
    print(findAthleteResults("Erika.*Sampaio", is_regex=True))
    print("***************")
    print(findResultsForAG(Division(male=True, lowAge=35, highAge=39)))
    print("***************")
    print(findFastestResults(breach=20))    

if __name__ == "__main__":
    df = pd.DataFrame.from_csv("http://localhost:8080/all")

    print(df.head())

    #cross_ref_world_champ_ties()