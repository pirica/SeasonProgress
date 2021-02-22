import requests # pip install requests
import tweepy # pip install tweepy
import time
import json
from PIL import Image, ImageDraw, ImageFont # pip install pillow
import datetime # pip install datetime
import schedule # pip install schedule

season_number = 'Season 0'
percent = '100'
days_left = '0'

# IGNORE ANYTHING ABOVE THIS POINT #






#------ SETTINGS ------#

# Game #
game = 'rocketleague' # games supported: fortnite, fallguys, rocketleague, apexlegends
# suggest more supported games in dsc.gg/thomaskeig

# Twitter Keys #
twitter_api_key = '' # Key found at https://developer.twitter.com/en/portal/dashboard
twitter_api_key_secret = '' # Key found at https://developer.twitter.com/en/portal/dashboard
twitter_access_token = '' # Key found at https://developer.twitter.com/en/portal/dashboard
twitter_access_token_secret = '' # Key found at https://developer.twitter.com/en/portal/dashboard

# General Configuration #
file_path = '' # If running on a VPS you must specifiy the file path to this file (eg: ""/root/progressbot") Remember the / at the begining AND END. This can be left empty if running from a PC.

# Tweet Time #
post_time = '00:00' # What time should the bot post? (measured on local time)
run_on_day = 'now' # How often should the bot post? [lowercase only] (daily/monday/tuesday/wednesday/thursday/friday/saturday/sunday) You can also use 'now' to test the bot and post right now

# Tweet Customization #
tweet_content = f'#{game} {season_number} is {percent}% Complete!\n\n{days_left} days left.' # Text to tweet alongside the image
# Variables to use: game, season_number, percent, days_left
bar_color = '#971eea' # HEX color value for the progress bar color.
progress_frame_file = 'progressframe_rl.png' # File name for the progress bar frame to utilise

#---------------------#






auth = tweepy.OAuthHandler(twitter_api_key, twitter_api_key_secret)
auth.set_access_token(twitter_access_token, twitter_access_token_secret)
api = tweepy.API(auth)

def progress_bar():
    try:
        print('Creating progress bar image')

        print('Grabbing data')

        try:
            response = requests.get(f'http://thomaskeig.co/api/progress/{game}.json')
            print("Found game data")
        except:
            print("Failed to grab game data. Have you inputted the game id correctly?")

        start_day = response.json()["start_day"]
        start_month = response.json()["start_month"]
        start_year = response.json()["start_year"]
        end_day = response.json()["end_day"]
        end_month = response.json()["end_month"]
        end_year = response.json()["end_year"]
        season_number = response.json()["season_number"]

        print('Creating Values')

        time_start = datetime.datetime(start_year, start_month, start_day)
        time_now = datetime.datetime.now()
        time_end = datetime.datetime(end_year, end_month, end_day)

        days_left = time_end - time_now
        days_left = days_left.days
        days_left = days_left + 1

        days_full = time_end - time_start
        days_full = days_full.days

        days_in = time_now - time_start
        days_in = days_in.days

        percent = (days_in / days_full)*100

        percent = round(percent)
        percentage = str(percent)
        percentage = percentage+'%'

        days_left = str(days_left)
        days_full = str(days_full)
        days_in = str(days_in)

        print('Starting to produce image')

        with Image.open(f'{file_path}{progress_frame_file}') as img:

            progress_bar_amount = 43 + (percent*11.11)

            img1 = ImageDraw.Draw(img)
            img1.rectangle([(progress_bar_amount, 255), (42, 109)], fill = bar_color)

            print('Added bar and created image')

            img.save(f'{file_path}progressbar.png')

        print('Attempting to tweet')

        try:
            api.update_with_media(f'{file_path}progressbar.png', tweet_content)
            print('Successfully tweeted')
        except:
            print("Failed to tweet")
    except:
        print("Failed to generate progress image")

    print(f'#{game} {season_number} is {percent}% Complete!\n\n{days_left} days left.')

if run_on_day == 'now':
    progress_bar()
elif run_on_day == 'daily':
    schedule.every().day.at(post_time).do(progress_bar)
elif run_on_day == 'monday':
    schedule.every().monday.at(post_time).do(progress_bar)
elif run_on_day == 'tuesday':
    schedule.every().tuesday.at(post_time).do(progress_bar)
elif run_on_day == 'wednesday':
    schedule.every().wednesday.at(post_time).do(progress_bar)
elif run_on_day == 'thursday':
    schedule.every().thursday.at(post_time).do(progress_bar)
elif run_on_day == 'friday':
    schedule.every().friday.at(post_time).do(progress_bar)
elif run_on_day == 'saturday':
    schedule.every().saturday.at(post_time).do(progress_bar)
elif run_on_day == 'sunday':
    schedule.every().sunday.at(post_time).do(progress_bar)
else:
    schedule.every().day.at(post_time).do(progress_bar)
    print("Incorrect value given for run_on_day, defaulting to every day.")

if run_on_day != 'now':
    print("--- Bot Starting ---")
    while 1:
        print(f"Waiting for {post_time}...")
        try:
            schedule.run_pending()
        except:
            print("Error while checking to run pending tasks")
        time.sleep(10)
