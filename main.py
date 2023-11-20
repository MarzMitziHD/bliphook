import requests
import feedparser
import re
import json
import time
prev_entry = None
prev_postfeed = None
usr = 'koy'
hook_url = 'https://discord.com/api/webhooks/1176041010518827060/-Q_RMHKbEtx4-iOzfaAC-tpPMafFKxpSpPnJ_xiQja5l0YXyY2i3nXeePipbrBEz4h2a'

while True:
    posts_feed = feedparser.parse(f'https://blips.club/{usr}/feed.rss')
    entry = posts_feed.entries[0]
    # 'content': f'**New blip from {usr}!**\n"{entry.description}"\nPublish date: {entry.published}\n{entry.link}'
    if prev_postfeed != posts_feed:
        i = 0
        # print(json.dumps(data))
        if prev_entry != None:
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
    prev_entry = entry
    prev_postfeed = posts_feed
    time.sleep(60*2)
