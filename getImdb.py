#creates a database of movies with the specified actor rows;

from imdbpie import Imdb
import pandas as pd
import os

import random
imdb = Imdb()
imdb = Imdb(anonymize=True)
imdb = Imdb(cache=True)

#path
#save to the R directory as this is what is needed.
outPath = "/users/sho/RProjects/imdb/data"

#set the bounds for the years
random.seed(4664)
maxYear = 2016
minYear = 2000

#how many rows..
numObs = 10000

#token;
#choose whether we want the actors/writers 'cast' 'writers'
#extend to allow both?

type = 'cast'


#helper(s)
currentRows = 0
failed = 0
importedTitle = set([])

df = pd.DataFrame(columns = ["Title","TitleID", "Year", "ActorFirstName", "ActorSurName"])

while(currentRows<numObs):

    #get a random number;
    n = random.randint(1000000,3000000)

    if (n not in importedTitle):
        titleID = "tt" + str(n)
    else:
        #already done so skip
        print("skipping loop as already imported")
        continue

    try:
        title = imdb.get_title_by_id(titleID)

    except:
        #debug
        print("no Match found:" + str(failed))
        failed = failed+1
        #break out of loop
        continue

    #title found
    #check it is within the selected year range
    if (title is not None):
        if (title.year is not None):
            if (title.year<=maxYear and title.year>=minYear):
                #continue

                for person in title.credits:
                    if person.token == type:
                        fullName = person.name.split();
                        firstName = fullName[0]
                        surName = fullName[len(fullName)-1]
                        filmName = title.title
                        year = title.year

                        df.loc[currentRows] = [filmName,titleID,  year, firstName, surName]
                        currentRows=currentRows+1
                        print("rows added: " + str(currentRows))

                #add to the set of completed titles
                importedTitle.add(n)




#now save out the data frame as csv... (easier in R...)
os.chdir(outPath)
df.to_csv("imdb.csv", sep=',')



