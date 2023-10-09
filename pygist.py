import os 
import argparse
import json
import requests
from datetime import datetime
from pprintpp import pprint


def get_gists(username):
    github_gists_url = 'http://api.github.com/users/' + username + '/gists'
    gists = []

    page = 1
    while True:
        params = {'page': page}
        response = requests.get(github_gists_url, params=params)
        
        if response.status_code != 200:
            if response.status_code == 404:
                print('Error: GitHub user "' + username + '" not found.')
            else:
                response.raise_for_status()
                exit(255)
        
        page_gists = response.json()
        if not page_gists:
            break  # No more gists to retrieve
        gists.extend(page_gists)
        page += 1

    return gists

def save_last_query_time(username, gists):
    config_file = './pygist.' + username
    try:
        with open(config_file, 'w') as user_file:
            user_file.write(gists[0]['created_at'])
    except Exception as e:
        raise

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("username", help="GitHub username")
    args = parser.parse_args()

    gists = get_gists(args.username)

    if not gists:
        pprint('GitHub user "' + args.username + '" has not published any gists.')
        exit(1)

    config_file = './pygist.' + args.username

    if not os.path.isfile(config_file):
        print('No previous entries for user "' + args.username + '"')
        print('Creating user file: ' + config_file)
        for item in gists:
            pprint("Created Date: " + item["created_at"] + " URL: " + item["html_url"])
        save_last_query_time(args.username, gists)
    else:
        try:
            with open(config_file, 'r') as user_file:
                last_query = user_file.read()
        except Exception as e:
            raise
        last_query_time = datetime.strptime(last_query, '%Y-%m-%dT%H:%M:%SZ')
        gist_created_date = datetime.strptime(gists[0]['created_at'], '%Y-%m-%dT%H:%M:%SZ')
        if gist_created_date > last_query_time:
            print('User "' + args.username + '" has created new gist(s) since the last query.')

            for item in gists:
                item_created_at = datetime.strptime(item["created_at"], '%Y-%m-%dT%H:%M:%SZ')
                if item_created_at > last_query_time:
                    pprint("Created Date: " + item["created_at"] + " URL: " + item["html_url"])

            save_last_query_time(args.username, gists)
        else:
            print('User "' + args.username + '" has not created any new gists since the last query.')
    exit(0)

if __name__ == "__main__":
    main()