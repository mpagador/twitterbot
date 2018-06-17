import tweepy
import random
from private import *

auth = tweepy.OAuthHandler(C_KEY, C_SECRET)
auth.set_access_token(A_TOKEN, A_TOKEN_SECRET)
api = tweepy.API(auth)

followers = tweepy.Cursor(api.followers).items()
greetings = open("greetings.txt", "r")


#follows back all current followers
def follow_back():
    for follower in tweepy.Cursor(api.followers).items():
        follower.follow()


#writes the message, and directs the tweet at a random follower if the message type is an encouragement or compliment
def message_writer(choice):
    if choice == 1:
        positive = open("positive.txt", "r")
        message = random.choice(positive.readlines())
    else:
        follower_list = list(followers)
        chosen_follower = random.choice(follower_list).screen_name
        print(chosen_follower)
        greeting = random.choice(greetings.readlines())
        print(greeting)
        message = greeting + " @" + chosen_follower + ", "
        print(message)
        if choice == 2:
            encouragements = open("encouragements.txt", "r")
            line = random.choice(encouragements.readlines())
            print(line)
            if greeting == "Hey":
                message = message + line
            elif greeting == "Hello":
                message = message + "I want you to know that " + line
            else:
                message = message + "this is a reminder that " + line
        else:
            compliments = open("compliments.txt", "r")
            line = random.choice(compliments.readlines())
            print(line)
            if greeting == "Hey":
                message = message + line
            elif greeting == "Hello":
                message = message + "I just wanted to say that " + line
            else:
                message = message + "I wanted to tell you that " + line
    print(message)
    return message


#generates a random number to determine message type and posts the final tweet
def post_tweet():
    num = random.randint(1, 3)
    api.update_status(message_writer(num))


if __name__ == "__main__":
    follow_back()
    post_tweet()



