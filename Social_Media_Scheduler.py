#pip install tweepy schedule
#pip install facebook-sdk instabot

import tweepy
import schedule
import time
from datetime import datetime
import facebook
from instabot import Bot

# Twitter API credentials
consumer_key = "YOUR_CONSUMER_KEY"
consumer_secret = "YOUR_CONSUMER_SECRET"
access_token = "YOUR_ACCESS_TOKEN"
access_token_secret = "YOUR_ACCESS_TOKEN_SECRET"

# Facebook API credentials
facebook_access_token = "YOUR_FACEBOOK_ACCESS_TOKEN"

# Instagram API credentials
instagram_username = "YOUR_INSTAGRAM_USERNAME"
instagram_password = "YOUR_INSTAGRAM_PASSWORD"

# Authenticate with Twitter
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
twitter_api = tweepy.API(auth)

# Authenticate with Facebook
facebook_api = facebook.GraphAPI(access_token=facebook_access_token, version="3.0")

# Authenticate with Instagram
instagram_bot = Bot()
instagram_bot.login(username=instagram_username, password=instagram_password)

# Function to send a tweet
def send_tweet(tweet_text):
    try:
        twitter_api.update_status(tweet_text)
        print(f"Tweet sent: {tweet_text}")
    except tweepy.TweepError as e:
        print(f"Error sending tweet: {e}")

# Function to post on Facebook
def post_on_facebook(post_text):
    try:
        facebook_api.put_object(parent_object='me', connection_name='feed', message=post_text)
        print(f"Facebook post created: {post_text}")
    except facebook.GraphAPIError as e:
        print(f"Error creating Facebook post: {e}")

# Function to post on Instagram
def post_on_instagram(post_text, image_path):
    try:
        instagram_bot.upload_photo(image_path, caption=post_text)
        print(f"Instagram post created: {post_text}")
    except Exception as e:
        print(f"Error creating Instagram post: {e}")

# Schedule social media function
def schedule_social_media(post_text, post_time, platforms, image_path=None):
    target_time = datetime.strptime(post_time, "%Y-%m-%d %H:%M")

    def send_scheduled_posts():
        if "twitter" in platforms:
            send_tweet(post_text)
        if "facebook" in platforms:
            post_on_facebook(post_text)
        if "instagram" in platforms and image_path:
            post_on_instagram(post_text, image_path)
        return schedule.CancelJob

    schedule.every().day.at(target_time.strftime("%H:%M")).do(send_scheduled_posts)

# Main function
def main():
    post_text = "Hello, this is a scheduled post!"
    post_time = "2023-04-07 12:00"  # Format: "YYYY-MM-DD HH:MM"
    platforms = ["twitter", "facebook", "instagram"]
    image_path = "path/to/your/image.jpg"  # Required for Instagram

    schedule_social_media(post_text, post_time, platforms, image_path)

    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == "__main__":
    main()
