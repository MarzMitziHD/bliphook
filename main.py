import requests
import feedparser
import re
import json
import time
import argparse
previouser_entry = None
prev_entry = None
prev_postfeed = None
i = 0
delay = 60*2

parser = argparse.ArgumentParser()
parser.add_argument("-u", "--username", help="Blips username to listen to. Must be string."#, required=True
)
parser.add_argument("-w", "--webhook_url", help="Webhook URL to post the recent bleep to. Supports only Discord, must be string."#, required=True
)
parser.add_argument("-c", "--cooldown", help="Seconds to cool down after it has checked for new posts. Must be integer."#, required=True
)
args = parser.parse_args()
args_dict = vars(args)
usr = args_dict['username']
hook_url = args_dict['webhook_url']
delay = args_dict['cooldown']

while True:
    print(f'Getting {usr}\'s RSS feed...')
    posts_feed = feedparser.parse(f'https://blips.club/{usr}/feed.rss')
    entry = posts_feed.entries[0]
    # 'content': f'**New blip from {usr}!**\n"{entry.description}"\nPublish date: {entry.published}\n{entry.link}'
    print('Check if the variable prev_postfeed and posts_feed are not the same...')
    if prev_postfeed != posts_feed:
        print('Check passed.')
        previouser_entry = posts_feed.entries[i+1]
        i = 0
        # print(json.dumps(data))
        print('Check if the prev_entry variable isn\'t \'None\'')
        if prev_entry != None:
            print('Check passed.')
            print('Go into while loop. Loop breaks once the current post at the variable \'i\' is not the previous '
                  'post.')
            while posts_feed.entries[i] != prev_entry:
                entry = posts_feed.entries[i]
                thumbnail = {'url': f'https://blips.club/profiles/{usr}.png'}
                embed = [{
                    'title': f'Blip from {usr}',
                    # 'title': 'test',
                    'color': 4716015,
                    'description': f'{entry.description}',
                    'url': f'{entry.link}',
                    'thumbnail': thumbnail
                }]
                data = {
                    'avatar_url': f'https://blips.club/profiles/{usr}.png',
                    "username": f'blips.club/{usr}',
                    "embeds": embed
                }
                r = requests.post(hook_url, data=json.dumps(data), headers={'Content-Type': 'application/json'})
                i += 1
                # print(r.text)
                print(f'Sent webhook, Discord returned with status code {r.status_code}')
                #if posts_feed.entries[i] == previouser_entry:
                #    break
    print(f'Sleeping for {delay} seconds.')
    prev_entry = entry
    prev_postfeed = posts_feed
    time.sleep(delay)
