import os
import platform
import requests
import json
from datetime import datetime, timezone
from colorama import init, Fore, Style
import pyfiglet

init(autoreset=True)

def clear_screen():
    if platform.system() == 'Windows':
        os.system('cls')
    else:
        os.system('clear')

title = pyfiglet.figlet_format("Reddit Scraper")
clear_screen()
print(f"{Fore.MAGENTA}{title}{Style.RESET_ALL}")

BASE_URL = 'https://www.reddit.com/'
HEADERS = {'User-Agent': 'reddit-post-scraper by your_username'}  

def fetch_posts(subreddit, post_limit=10):
    url = BASE_URL + f'r/{subreddit}/hot.json?limit={post_limit}'
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        data = response.json()
        posts = data['data']['children']
        return posts
    else:
        print(f"{Fore.RED}Failed to fetch posts from r/{subreddit}. Status code: {response.status_code}{Style.RESET_ALL}")
        return None

def display_posts(posts):
    if not posts:
        return
    
    print(f"{Fore.CYAN}{'-'*50}\n{' '*20}Reddit Posts\n{'-'*50}{Style.RESET_ALL}")
    for post in posts:
        post_data = post['data']
        title = post_data['title']
        author = post_data['author']
        score = post_data['score']
        created_utc = post_data['created_utc']
        
        created_time = datetime.fromtimestamp(created_utc, tz=timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
        
        permalink = BASE_URL + post_data['permalink']
        
        print(f"{Fore.GREEN}Title: {title}")
        print(f"Author: {author}")
        print(f"Score: {score}")
        print(f"Created Time: {created_time}")
        print(f"Link: {permalink}")
        print(f"{'-'*50}{Style.RESET_ALL}")

def main():
    subreddit = input("Enter subreddit name: ").strip()
    post_limit = int(input("Enter number of posts to fetch (default is 10): ") or 10)
    
    posts = fetch_posts(subreddit, post_limit)
    if posts:
        display_posts(posts)

if __name__ == "__main__":
    main()