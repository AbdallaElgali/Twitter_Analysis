import json
import time
import requests
from requests_oauthlib import OAuth1
from tokens import consumer_key, consumer_secret, access_token, access_token_secret

XP_006 = 1725359481222263097

def get_retweeting_users(tweet_id, pag_token, all_retweets, limit):
    base_url = f'https://api.twitter.com/2/tweets/{tweet_id}/retweeted_by'

    auth = OAuth1(
        consumer_key,
        consumer_secret,
        access_token,
        access_token_secret
    )
    if limit > 0:
        if pag_token is not None:
            params = {
                'max_results': 100,  # Number of retweets per request
                'tweet.fields': 'id,author_id',  # Additional fields to include in the response
                'user.fields': 'id,username,location',
                'pagination_token': pag_token
            }
        else:
            params = {
                'max_results': 100,  # Number of retweets per request
                'tweet.fields': 'id,author_id',  # Additional fields to include in the response
                'user.fields': 'id,username,location'
            }
        response = requests.get(base_url, auth=auth, params=params)
        if response.status_code == 200:
            retweets = response.json().get('data', [])
            all_retweets.extend(retweets)
        else:
            print(f"Error: {response.status_code} - {response.text}")

        if 'next_token' in response.json().get('meta', {}):
            next_token = response.json().get('meta', {}).get('next_token')
            return get_retweeting_users(tweet_id, next_token, all_retweets, limit - 1)
        else:
            return all_retweets
    else:
        wait_time = 900
        print('Rate Limit Reached! Waiting for next request...')
        print(f'Waiting for {wait_time / 60} minutes')
        time.sleep(wait_time + 5)
        return get_retweeting_users(tweet_id, pag_token, all_retweets, 5)

def get_user_info_by_id(user_id):
    # Twitter API endpoint URL
    url = f'https://api.twitter.com/2/users/{user_id}'

    # Specify additional fields to include in the response
    params = {
        'user.fields': 'id,created_at,description,location',  # Add or remove fields as needed
        'expansions': 'most_recent_tweet_id',
        'tweet.fields': 'text,geo,source'
    }

    # Create OAuth1 authentication object with user context
    auth = OAuth1(
        consumer_key,
        consumer_secret,
        access_token,
        access_token_secret
    )

    try:
        # Send GET request to the Twitter API with OAuth1 authentication and additional fields
        response = requests.get(url, auth=auth, params=params)

        # Check if request was successful (status code 200)
        if response.status_code == 200:
            user_data = response.json()  # Parse JSON response
            return user_data
        else:
            print('Error:', response.status_code, response.text)
    except requests.RequestException as e:
        print('Request Error:', e)
    except Exception as e:
        print('Unexpected Error:', e)\

def get_user_info_by_username(user):
    # Twitter API endpoint URL
    url = f'https://api.twitter.com/2/users/by/username/{user}'

    # Specify additional fields to include in the response
    params = {
        'user.fields': 'id,created_at,description,location',  # Add or remove fields as needed
        'expansions': 'most_recent_tweet_id',
        'tweet.fields': 'text,geo,source'
    }

    # Create OAuth1 authentication object with user context
    auth = OAuth1(
        consumer_key,
        consumer_secret,
        access_token,
        access_token_secret
    )

    try:
        # Send GET request to the Twitter API with OAuth1 authentication and additional fields
        response = requests.get(url, auth=auth, params=params)

        # Check if request was successful (status code 200)
        if response.status_code == 200:
            user_data = response.json()  # Parse JSON response
            return user_data
        else:
            print('Error:', response.status_code, response.text)
    except requests.RequestException as e:
        print('Request Error:', e)
    except Exception as e:
        print('Unexpected Error:', e)

def get_tweet_info(tweet_id):
    url = f'https://api.twitter.com/2/tweets/{tweet_id}'

    # Specify additional fields to include in the response
    params = {
        'tweet.fields': 'in_reply_to_user_id,author_id,created_at,conversation_id,public_metrics',
        'expansions': 'entities.mentions.username,geo.place_id',
        'media.fields': 'public_metrics,non_public_metrics,organic_metrics,promoted_metrics'
    }

    # Create OAuth1 authentication object with user context
    auth = OAuth1(
        consumer_key,
        consumer_secret,
        access_token,
        access_token_secret
    )

    try:
        # Send GET request to the Twitter API with OAuth1 authentication and additional fields
        response = requests.get(url, auth=auth, params=params)

        # Check if request was successful (status code 200)
        if response.status_code == 200:
            data = response.json()  # Parse JSON response
            print(data)
            return data
        else:
            print('Error:', response.status_code, response.text)
    except requests.RequestException as e:
        print('Request Error:', e)
    except Exception as e:
        print('Unexpected Error:', e)
def get_tweet_reply_authors(tweet_id):
    url = f'https://api.twitter.com/2/tweets/{tweet_id}'

    # Specify additional fields to include in the response
    params = {
        'tweet.fields': 'in_reply_to_user_id,author_id,created_at,conversation_id,public_metrics,referenced_tweets',
        'expansions': 'entities.mentions.username,geo.place_id,referenced_tweets.id.author_id',
        'user.fields':'entities,id,username'
    }

    # Create OAuth1 authentication object with user context
    auth = OAuth1(
        consumer_key,
        consumer_secret,
        access_token,
        access_token_secret
    )

    try:
        # Send GET request to the Twitter API with OAuth1 authentication and additional fields
        response = requests.get(url, auth=auth, params=params)

        # Check if request was successful (status code 200)
        if response.status_code == 200:
            data = response.json()  # Parse JSON response
            return data
        else:
            print('Error:', response.status_code, response.text)
    except requests.RequestException as e:
        print('Request Error:', e)
    except Exception as e:
        print('Unexpected Error:', e)

def get_user_tweets(user_id, max_tweets):
    url = f'https://api.twitter.com/2/users/{user_id}/tweets'

    params = {
        'tweet.fields': 'id,text,created_at',  # Specify the fields you want to retrieve
        'max_results': f'{max_tweets}'  # Adjust the number of tweets you want to retrieve
    }

    auth = OAuth1(
        consumer_key,
        consumer_secret,
        access_token,
        access_token_secret
    )

    try:
        response = requests.get(url, auth=auth, params=params)

        if response.status_code == 200:
            data = response.json()
            return data
        else:
            print('Error:', response.status_code, response.text)
    except requests.RequestException as e:
        print('Request Error:', e)
    except Exception as e:
        print('Unexpected Error:', e)

def get_user_tweets_by_date(user_id, start_date, end_date):
    url = 'https://api.twitter.com/2/tweets/search/recent'

    params = {
        'query': f'from:{user_id} -is:retweet',  # Filter tweets by the user and exclude retweets
        'start_time': start_date,  # Format: YYYY-MM-DDTHH:MM:SSZ
        'end_time': end_date,  # Format: YYYY-MM-DDTHH:MM:SSZ
        'tweet.fields': 'id,text,created_at,conversation_id',  # Specify the fields you want to retrieve
        'max_results': 100  # Adjust the number of tweets you want to retrieve
    }

    auth = OAuth1(
        consumer_key,
        consumer_secret,
        access_token,
        access_token_secret
    )

    try:
        response = requests.get(url, auth=auth, params=params)

        if response.status_code == 200:
            data = response.json()
            return data
        else:
            print('Error:', response.status_code, response.text)
    except requests.RequestException as e:
        print('Request Error:', e)
    except Exception as e:
        print('Unexpected Error:', e)


def get_all_liking_users(tweet_id):
    base_url = f'https://api.twitter.com/2/tweets/{tweet_id}/liking_users'
    all_liking_users = []

    params = {
        'user.fields': 'id,name,username,location'
    }

    auth = OAuth1(
        consumer_key,
        consumer_secret,
        access_token,
        access_token_secret
    )

    try:
        remaining_requests = 13  # Initial number of remaining requests
        reset_time = time.time() + 900  # Set initial reset time (15 minutes)

        while remaining_requests > 0:
            # Check if rate limit will be exceeded in the next request
            if remaining_requests < 2:
                wait_time = reset_time - time.time()
                print(f"Rate limit about to be reached. Waiting for {wait_time:.0f} seconds...")
                time.sleep(wait_time)
                reset_time = time.time() + 900  # Reset the reset time
                remaining_requests = 75  # Reset the remaining requests counter

            response = requests.get(base_url, params=params, auth=auth)

            if response.status_code == 200:
                liking_users = response.json().get('data', [])
                all_liking_users.extend(liking_users)

                # Update remaining requests and reset time
                remaining_requests -= 1
            elif response.status_code == 429:
                print("Rate limit exceeded. Waiting for rate limit reset...")
                reset_time = int(response.headers['x-rate-limit-reset'])
                time.sleep(reset_time - time.time() + 5)  # Wait for reset (+5 seconds buffer)
                remaining_requests = 13  # Reset the remaining requests counter
            else:
                print(f"Error: {response.status_code} - {response.text}")
                break

            # Check if there are more liking users available
            if 'next_token' not in response.json().get('meta', {}):
                break

            next_token = response.json()['meta']['next_token']
            params['pagination_token'] = next_token

    except requests.RequestException as e:
        print('Request Error:', e)
    except Exception as e:
        print('Unexpected Error:', e)

    return all_liking_users


def save_data(file_name, data):
    with open(f'{file_name}.json', 'w+') as f:
        json.dump(data, f, indent=4)


'''
tweet_id = 1790787721973157933
conversation_id = 1790786883972165843
tweet_info = get_tweet_info(tweet_id)
reply_authors = get_tweet_reply_authors(conversation_id)

with open('author_ids.json', 'w') as json_file:
    json.dump(reply_authors, json_file, indent=4)
with open('tweet_info.json', 'w') as json_file:
    json.dump(tweet_info, json_file, indent=4)
'''
