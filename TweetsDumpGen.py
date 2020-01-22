import csv
from datetime import datetime
import tweepy
import json

import savetoaws_kartik


def get_all_tweets(screen_name):
    with open('details.json') as f:
        data=json.load(f)
        print(type(data))
    consumer_key=data["consumer_key"]
    consumer_secret=data["consumer_secret"]
    access_key=data["access_key"]
    access_secret=data["access_secret"]

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)

    # initialize a list to hold all the tweepy Tweets
    alltweets = []

    # make initial request for most recent tweets (200 is the maximum allowed count)
    new_tweets = api.user_timeline(screen_name=screen_name, count=200)

    # save most recent tweets
    alltweets.extend(new_tweets)

    # save the id of the oldest tweet less one
    oldest = alltweets[-1].id - 1

    # keep grabbing tweets until there are no tweets left to grab
    while len(new_tweets) > 0:
        print("getting tweets before %s" % (oldest))

        # all subsiquent requests use the max_id param to prevent duplicates
        new_tweets = api.user_timeline(screen_name=screen_name, count=200, max_id=oldest)

        # save most recent tweets
        alltweets.extend(new_tweets)

        # update the id of the oldest tweet less one
        oldest = alltweets[-1].id - 1

        print("...%s tweets downloaded so far" % (len(alltweets)))


    # transform the tweepy tweets into a 2D array that will populate the csv
    outtweets = [[tweet.id_str, tweet.created_at, tweet.text.encode("utf-8")] for tweet in alltweets]
    print(outtweets)



    date=datetime.today().strftime('%Y-%m-%d')
    fname="{}tweets{}.csv".format(screen_name,date)
    with open(fname,'w') as f:
        writer = csv.writer(f)
        writer.writerow(["Id", "Time", "Tweet"])
        writer.writerows(outtweets)

    a=savetoaws.upload_file_to_s3(fname,"tweetexcel", fname)
    return a


if __name__ == '__main__':
    # pass in the username of the account you want to download
    get_all_tweets("manas_saloi")
    name=''



