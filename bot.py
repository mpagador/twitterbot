import tweepy
import random
from private import *

auth = tweepy.OAuthHandler(C_KEY, C_SECRET)
auth.set_access_token(A_TOKEN, A_TOKEN_SECRET)
api = tweepy.API(auth)

#follows back all current followers
def follow_back():
    for follower in tweepy.Cursor(api.followers).items():
        follower.follow()

def message_writer():
    greetings = ["Hey ", "Hi ", "Hello "]
    encouragements = ["I hope you have a good day today!", "you can do whatever you set your mind to!",
                  "always try your best!"]
    followers = tweepy.Cursor(api.followers).items()

    tmp = list(followers)
    random.shuffle(tmp)

    message = random.choice(greetings) + "@" + random.choice(tmp).screen_name + ", " + random.choice(encouragements)

    return message



def post_tweet():
    api.update_status(message_writer())



if __name__ == "__main__":
    follow_back()
    post_tweet()



