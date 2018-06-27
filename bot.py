import tweepy
import random
import time
import datetime
from private import *


auth = tweepy.OAuthHandler(C_KEY, C_SECRET)
auth.set_access_token(A_TOKEN, A_TOKEN_SECRET)
api = tweepy.API(auth)

greetings = ["Hey", "Hello", "Hi"]
follower_list = []


#sleeps for 1 minute if RateLimitError is raised
def limit_handled(cursor):
    while True:
        try:
            yield cursor.next()
        except tweepy.RateLimitError:
            time.sleep(60)


#follows back all current followers
def follow_back():
    for follower in limit_handled(tweepy.Cursor(api.followers).items()):
        try:
            follower.follow()
            follower_list.append(follower.screen_name)
        except tweepy.error.TweepError:
            pass


#unfollows non-followers
def unfollow():
    for f in limit_handled(tweepy.Cursor(api.friends).items()):
        if f.screen_name not in follower_list:
            api.destroy_friendship(f.screen_name)
            print("Unfollowed " + f.screen_name)


#favorites/likes all tweets that the bot was mentioned (tagged) in
def fave_mentions():
    for mentions in tweepy.Cursor(api.mentions_timeline).items():
        try:
            api.create_favorite(mentions.id)
        except:
            pass


#clears the text file containing names of followers who already received messages when a new day starts
def clear_received_file():
    if datetime.datetime.now().hour == 0:
        open('followers_who_received_messages.txt', 'w').close()


#writes the message, and directs the tweet at a random follower if the message type is an encouragement or compliment
def message_writer(choice):
    if choice == 1 or choice == 3:
        with open("positive.txt", "r", encoding="utf-8-sig") as positive:
            message = random.choice(positive.readlines())
    else:
        chosen_follower = random.choice(follower_list)
        with open("followers_who_received_messages.txt", "r+", encoding="utf-8") as file:
            already_received_list = []
            for name in file.readlines():
                already_received_list.append(name[:-1])
            while chosen_follower in already_received_list:
                chosen_follower = random.choice(follower_list)
            file.write(chosen_follower + "\n")

        greeting = random.choice(greetings)
        message = greeting + " @" + chosen_follower + ", "

        if choice == 2:
            with open("encouragements.txt", "r", encoding="utf-8-sig") as encouragements:
                line = random.choice(encouragements.readlines())
            if greeting == "Hey":
                message = message + line
            elif greeting == "Hello":
                message = message + "I just wanted to say that " + line
            else:
                message = message + "this is a reminder that " + line
        else:
            with open("compliments.txt", "r", encoding="utf-8-sig") as compliments:
                line = random.choice(compliments.readlines())
            if greeting == "Hey":
                message = message + line
            elif greeting == "Hello":
                message = message + "I want you to remember that " + line
            else:
                message = message + "I just want to let you know that " + line
    print(message)
    return message


#generates a random number to determine message type and posts the final tweet
def post_tweet():
    num = random.randint(1, 4)
    api.update_status(message_writer(num))


if __name__ == "__main__":
    follow_back()
    unfollow()
    fave_mentions()
    clear_received_file()
    post_tweet()
