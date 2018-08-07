import tweepy
import random
import time
# import datetime
from private import *


auth = tweepy.OAuthHandler(C_KEY, C_SECRET)
auth.set_access_token(A_TOKEN, A_TOKEN_SECRET)
api = tweepy.API(auth)

user = api.get_user('marissasbot')
greetings = ["Hey", "Hello", "Hi"]
follower_list = []


# sleeps for 1 minute if RateLimitError is raised
def limit_handled(cursor):
    while True:
        try:
            yield cursor.next()
        except tweepy.RateLimitError:
            print("sleeping...")
            time.sleep(60)


# adds all current followers to a list
def list_followers():
    for follower in limit_handled(tweepy.Cursor(api.followers).items()):
            follower_list.append(follower.screen_name)
            print("added to list")


# favorites/likes all tweets that the bot was mentioned (tagged) in
def fave_mentions():
    for mentions in tweepy.Cursor(api.mentions_timeline).items():
        try:
            api.create_favorite(mentions.id)
        except:
            pass


'''
# clears the text file containing names of followers who already received messages when a new day starts
def clear_received_file():
    if datetime.datetime.now().hour == 0:
        open('followers_who_received_messages.txt', 'w').close()
'''


# clears followers log
def clear_received_file():
    open('followers_who_received_messages.txt', 'w').close()


# chooses a positive message that isn't in the log, clears log if every line has been chosen
def positive_choice():
    positive_log = []
    with open("positive_log.txt", "r", encoding="utf-8-sig") as p_log:
        for p in p_log.readlines():
            positive_log.append(p)
    if len(positive_log) == 116:
        open('positive_log.txt', 'w').close()
    with open("positive.txt", "r", encoding="utf-8-sig") as positive:
        message = random.choice(positive.readlines())
        if len(positive_log) != 0:
            while message in positive_log:
                message = random.choice(positive.readlines())
    with open("positive_log.txt", "w", encoding="utf-8") as p_log:
        p_log.write(message + "\n")
    return message


# chooses an encouragement that isn't in the log, clears log if every line has been chosen
def encouragements_choice():
    encouragements_log = []
    with open("encouragements_log.txt", "r", encoding="utf-8-sig") as e_log:
        for e in e_log.readlines():
            encouragements_log.append(e)
    if len(encouragements_log) == 77:
        open('encouragements_log.txt', 'w').close()
    with open("encouragements.txt", "r", encoding="utf-8-sig") as encouragements:
        line = random.choice(encouragements.readlines())
        if len(encouragements_log) != 0:
            while line in encouragements_log:
                line = random.choice(encouragements.readlines())
    with open("encouragements_log.txt", "w", encoding="utf-8") as e_log:
        e_log.write(line + "\n")
    return line


# chooses a compliment that isn't in the log, clears log if every line has been chosen
def compliments_choice():
    compliments_log = []
    with open("compliments_log.txt", "r", encoding="utf-8-sig") as c_log:
        for c in c_log.readlines():
            compliments_log.append(c)
    if len(compliments_log) == 99:
        open('compliments_log.txt', 'w').close()
    with open("compliments.txt", "r", encoding="utf-8-sig") as compliments:
        line = random.choice(compliments.readlines())
        if len(compliments_log) != 0:
            while line in compliments_log:
                line = random.choice(compliments.readlines())
    with open("compliments_log.txt", "w", encoding="utf-8") as c_log:
        c_log.write(line + "\n")
    return line


# chooses a follower
def follower_choice():
    chosen_follower = random.choice(follower_list)
    with open("followers_who_received_messages.txt", "r+", encoding="utf-8") as f_log:
        follower_log = []
        for name in f_log.readlines():
            follower_log.append(name[:-1])
        if len(follower_log) == user.followers_count:
            clear_received_file()
        elif len(follower_log) != 0:
            while chosen_follower in follower_log:
                chosen_follower = random.choice(follower_list)
        f_log.write(chosen_follower + "\n")
    return chosen_follower


# writes the message, and directs the tweet at a random follower if the message type is an encouragement or compliment
def message_writer(choice):
    if choice == 1 or choice == 3:
        message = positive_choice()
    else:
        chosen_follower = follower_choice()
        greeting = random.choice(greetings)
        message = greeting + " @" + chosen_follower + ", "

        if choice == 2:
            line = encouragements_choice()
            if greeting == "Hey":
                message = message + line
            elif greeting == "Hello":
                message = message + "I just wanted to say that " + line
            else:
                message = message + "this is a reminder that " + line
        else:
            line = compliments_choice()
            if greeting == "Hey":
                message = message + line
            elif greeting == "Hello":
                message = message + "I want you to remember that " + line
            else:
                message = message + "I just want to let you know that " + line
    print(message)
    return message


# generates a random number to determine message type and posts the final tweet
def post_tweet():
    num = random.randint(1, 4)
    api.update_status(message_writer(num))


if __name__ == "__main__":
    list_followers()
    clear_received_file()
    post_tweet()
    fave_mentions()
