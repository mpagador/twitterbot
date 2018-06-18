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
        follower.follow()
        follower_list.append(follower.screen_name)

#chooses a random line from a file using Waterman's Reservoir Algorithim (Algorithim R)
def random_line(file):
    line = next(file)
    for num, aline in enumerate(file):
        if random.randrange(num + 2): continue
        line = aline
    return line

#clears the text file containing names of followers who already received messages when a new day starts
def clear_received_file():
    if datetime.time.hour == 0:
        open('followers_who_received_messages.txt', 'w').close()


#writes the message, and directs the tweet at a random follower if the message type is an encouragement or compliment
def message_writer(choice):
    if choice == 1:
        positive = open("positive.txt", "r", encoding="utf-8-sig")
        message = random_line(positive)
        positive.close()
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
            encouragements = open("encouragements.txt", "r", encoding="utf-8-sig")
            line = random_line(encouragements)
            encouragements.close()
            if greeting == "Hey":
                message = message + line
            elif greeting == "Hello":
                message = message + "I just wanted to say that " + line
            else:
                message = message + "this is a reminder that " + line
        else:
            compliments = open("compliments.txt", "r", encoding="utf-8-sig")
            line = random_line(compliments)
            compliments.close()
            if greeting == "Hey":
                message = message + line
            elif greeting == "Hello":
                message = message + "I want you to remember that " + line
            else:
                message = message + "I just want to let you know that " + line
    return message


#generates a random number to determine message type and posts the final tweet
def post_tweet():
    num = random.randint(1, 3)
    api.update_status(message_writer(num))


if __name__ == "__main__":
    follow_back()
    clear_received_file()
    post_tweet()



