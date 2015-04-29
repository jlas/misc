import csv
import time
import requests

user_uuid = "2iq73-ImkEuF8UrY-Ih3iqxPI_hGYKPGBG0BwG0MVu0WkTULDF4wsF5N-2AvPYgi"
feed_type = "city"
baseurl = 'https://membersapi.wework.com/api/v5/home?encrypted_user_uuid={user_uuid}&feed_type={feed_type}&page={page}&web_feed=true'

page = 0
posts = []

post_fields = ['raw_content', 'created_at', 'liked_by_count', 'comments_count', 'uuid']
member_fields = ['company_name', 'location_name', 'name', 'title', 'uuid']

def encode(v):
    try:
        return v.encode('utf-8')
    except:
        return v

def post_filter(post):
    d = dict([(k, encode(post[k])) for k in post_fields])
    d.update(dict([(k, encode(post['member'][k])) for k in member_fields]))
    return d

def save_posts():
    with open('posts.csv', 'w') as f:
        writer = csv.DictWriter(f, fieldnames=(post_fields + member_fields))
        writer.writeheader()
        writer.writerows(posts)

def save_page():
    with open('page', 'w') as f:
        f.write(str(page))

while True:
    page += 1
    url = baseurl.format(page=page, user_uuid=user_uuid, feed_type=feed_type)
    r = requests.get(url)
    posts.extend(map(post_filter, r.json()['feed']['posts']))
    save_posts()
    save_page()
    time.sleep(2)
    
