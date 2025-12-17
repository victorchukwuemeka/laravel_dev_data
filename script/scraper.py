import requests
import pandas as pd
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

GOOD = 'LOL'
HEADERS = {
    "Authorization": f"token {GOOD}",
    "Accept": "application/vnd.github+json"
}

# Session with automatic retries
session = requests.Session()
retry = Retry(total=3, backoff_factor=1, status_forcelist=[500, 502, 503, 504])
adapter = HTTPAdapter(max_retries=retry)
session.mount('http://', adapter)
session.mount('https://', adapter)
session.headers.update(HEADERS)

users = []
seen_usernames = set()  

def get_repos(page):
    """Fetch repos for a given page"""
    url = f"https://api.github.com/search/repositories?q=topic:laravel+language:php&per_page=100&page={page}"
    try:
        r = session.get(url, timeout=10)
        r.raise_for_status()
        return r.json()["items"]
    except requests.exceptions.RequestException as e:
        print(f"❌ Error fetching repos page {page}: {e}")
        return []

def get_user(username):
    """Fetch user details"""
    if username in seen_usernames:  # Skip duplicates early
        return None
    
    url = f"https://api.github.com/users/{username}"
    try:
        r = session.get(url, timeout=10)
        r.raise_for_status()
        user = r.json()
        
        seen_usernames.add(username)
        return {
            "github_username": user["login"],
            "profile_url": user["html_url"],
            "email": user.get("email", "N/A"),
            "twitter": user.get("twitter_username", "N/A"),
            "blog": user.get("blog", "N/A"),
            "location": user.get("location", "N/A"),
            "followers": user.get("followers", 0),
            "public_repos": user.get("public_repos", 0),
        }
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            print(f"⚠️  User not found: {username}")
        else:
            print(f"❌ HTTP error for {username}: {e}")
        return None
    except requests.exceptions.RequestException as e:
        print(f"❌ Network error for {username}: {e}")
        return None
    except KeyError as e:
        print(f"❌ Missing data for {username}: {e}")
        return None

def process_repo(repo):
    """Process a single repo's owner"""
    owner = repo["owner"]["login"]
    return get_user(owner)

# Main execution
print("🚀 Starting to fetch repos...")

all_repos = []
for page in range(1, 11):
    print(f"📄 Fetching page {page}/10...")
    repos = get_repos(page)
    all_repos.extend(repos)
    time.sleep(0.5)  # Small delay between repo searches

print(f"✅ Found {len(all_repos)} repos")
print(f"👤 Fetching user details (using {min(10, len(all_repos))} threads)...")

# Parallel user fetching
with ThreadPoolExecutor(max_workers=10) as executor:
    futures = [executor.submit(process_repo, repo) for repo in all_repos]
    
    for i, future in enumerate(as_completed(futures), 1):
        user_data = future.result()
        if user_data:
            users.append(user_data)
        
        # Progress indicator
        if i % 10 == 0:
            print(f"✓ Processed {i}/{len(all_repos)} repos ({len(users)} unique users)")

print(f"\n✅ Collected {len(users)} unique users")
print("💾 Saving to CSV...")

df = pd.DataFrame(users)
df.to_csv("laravel_devs.csv", index=False)

print(f"✅ Done! Saved {len(df)} users to laravel_devs.csv")
