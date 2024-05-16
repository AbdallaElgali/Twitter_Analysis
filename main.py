import json
import twapi

target_user = 'jai_a_dehadrai'
user_id = '14386440'

most_recent_tweet_post = '1790721453006127199'
conversation_id = '1790721453006127199'  # of the above post/tweet

def users_country(conv_id):
    countries = []
    authors = twapi.get_tweet_reply_authors(1719934212365857090)
    for author in authors.get('data'):
        country = author.get('country')
        if country:
            if country not in countries:
                countries.append(country)
    return countries

def conversations_country(conv_id):
    with open('retweets_03Nov_2023.json', 'r') as f:
        data = json.load(f)
        locations = []
        count = 0
        for author in data:
            if count == 10:
                break
            author_username = author.get('id')
            user = twapi.get_user_info_by_id(author_username)
            if user is None:
                print(locations)
                break
            user_data = user.get('data')
            if user_data.get('location') is not None:
                location = user_data.get('location')
                locations.append(location)
            count +=1
    print(locations)


liking_users = twapi.get_all_liking_users(1725359481222263097)
twapi.save_data('XP_006_liking_users01', liking_users)

with open('XP_006_liking_users.json', 'r') as f:
    data = json.load(f)
    print(len(data))
    for user in data:
        if user.get('location') is not None:
            print(user.get('location'))