import json
import twapi
import time

# tweet_ids = {tweet_reference: tweet_id}

tweet_ids = {'XP_007': 1725928367017316790, 'XP_008': 1726848980787560500, 'XP_013': 1764585933486313824,
             'XP_006': 1725359481222263097}


def get_all_retweets():
    for key, value in tweet_ids.items():
        print(f'Extracting Retweets for {key}')
        retweets = twapi.get_retweeting_users(value, None, [], 5)
        twapi.save_data(f'{key}_retweets', retweets)
        time.sleep(905)
        print('Sleeping for 15 minutes', time.time())

def get_all_liking_users():
    for key, value in tweet_ids.items():
        print(f'Extracting Retweets for {key}')
        liking_users = twapi.get_all_liking_users(value, None, [], 25)
        twapi.save_data(f'{key}_liking_users', liking_users)
        time.sleep(905)
        print('Sleeping for 15 minutes', time.time())

get_all_retweets()
get_all_liking_users()