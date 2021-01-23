import pandas as pd
import csv



import tweepy

# Twitter API credentials
consumer_key = "lOwUxnz3vuZY0U0Yj7eBcKZH4"
consumer_secret = "MBXwg5w42v4M2imjjjXI1Ph7ixNQjP5wdZd96MihodouPMN7ju"
access_key = "1315308812405035008-0ie0n4poOGz5YvRcJkFmjReA8Wo1Ud"
access_secret = "7NbnxSSuBYVmCBcit5VxwkVOIL7I8sTQCXGwYFWJyoQvi"


def get_all_tweets(screen_name): #this function return all the tweets

    # Twitter only allows access to a users most recent 3240 tweets with this method
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)

    alltweets = [] # initialize a list to hold all the tweepy Tweets

    new_tweets = api.user_timeline(screen_name=screen_name, count=200)

    alltweets.extend(new_tweets) # save most recent tweets

    oldest = alltweets[-1].id - 1 # save the id of the oldest tweet less one

    # keep grabbing tweets until there are no tweets left to grab
    while len(new_tweets) > 0:
        print(f"getting tweets before {oldest}")

        # all subsiquent requests use the max_id param to prevent duplicates
        new_tweets = api.user_timeline(screen_name=screen_name, count=200, max_id=oldest)

        # save most recent tweets
        alltweets.extend(new_tweets)
        print(alltweets)

        # update the id of the oldest tweet less one
        oldest = alltweets[-1].id - 1

        print(f"...{len(alltweets)} tweets downloaded so far")  #monitoring while running



    # transform the tweepy tweets into a 2D array that will populate the csv
    outtweets = [[tweet.id_str, tweet.created_at, tweet.text, tweet.favorite_count, tweet.retweet_count] for tweet in alltweets]

    # write the csv
    with open(f'new_{screen_name}_tweets.csv', 'w') as f: #this make a csv file of all the tweets with column "Id", "time", "text of the tweet", "number of favourites" and "number of retweets"
        writer = csv.writer(f)
        writer.writerow(["id", "created_at", "text", "Favourites", "Retweet"])
        writer.writerows(outtweets)

    pass



if __name__ == '__main__': #collect data from the account of Netflix, Durex and Huawei
    get_all_tweets("Netflix")
    get_all_tweets("Durex Global")
    get_all_tweets("Huawei")

#read all the file
df1 = pd.read_csv('new_durex_tweets.csv', error_bad_lines=False)
df2 = pd.read_csv('new_netflix_tweets.csv', error_bad_lines=False)
df3 = pd.read_csv('new_Huawei_tweets.csv', error_bad_lines=False)

#create a dictionary
integration_dictionary = []
integration_dictionary = ["women", "#women","diversity","integration","racism","race","inclusion","homosexuals","not traditional" "family","traditional family","black people","black","transgender","inequality",
                          "Hispanic American","curvy","down syndrome","ally","neurodiversity","non binary","allyship","antiracist", "Bipoc","equity","equality", "#diversity",
                          "#integration","#racism","#race","#inclusion","#homosexuals","#not traditional" "#family","#nottraditionalfamily","#blackpeople","#blackmatter","#transgender","#inequality",
                          "#HispanicAmerican","#curvy","#down syndrome","#ally","#neurodiversity","#nonbinary","#allyship","#antiracist", "#Bipoc","#equity","#equality",]

frames = [df1, df2, df3]

result = pd.concat(frames) #concatenate files


pattern = '|'.join(integration_dictionary)

counter = (result.text.str.contains(pattern)).tolist()
print(len(counter))

diversity = []
for n in counter : #create a column with binary values with the same number of terms of the number of tweets
    if n == False:
        diversity.append(0)
    else:
        diversity.append(1)

result["diversity"] =  diversity #append column

result['diversity'].corr(result['Retweet'])



result.to_csv('result.csv')