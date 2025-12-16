import pandas as pd
import re

# Read the messy CSV
df = pd.read_csv("../laravel_devs.csv")

print(f"📊 Original data: {len(df)} rows")

# 1. Remove duplicates (by username and email)
df = df.drop_duplicates(subset=['github_username'], keep='first')
print(f"✓ After removing username duplicates: {len(df)} rows")

# 2. Clean and standardize data
def clean_url(url):
    """Clean and validate URLs"""
    if pd.isna(url) or url == "N/A" or url == "":
        return None
    url = str(url).strip()
    if not url.startswith('http'):
        url = 'https://' + url
    return url

def clean_location(loc):
    """Standardize location format"""
    if pd.isna(loc) or loc == "N/A" or loc == "":
        return None
    return str(loc).strip().title()

def clean_email(email):
    """Validate email format"""
    if pd.isna(email) or email == "N/A" or email == "":
        return None
    email = str(email).strip().lower()
    # Basic email validation
    if re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
        return email
    return None

def clean_twitter(twitter):
    """Clean Twitter handles"""
    if pd.isna(twitter) or twitter == "N/A" or twitter == "":
        return None
    twitter = str(twitter).strip()
    # Remove @ if present
    twitter = twitter.lstrip('@')
    return twitter if twitter else None

# Apply cleaning functions
df['email'] = df['email'].apply(clean_email)
df['twitter'] = df['twitter'].apply(clean_twitter)
df['blog'] = df['blog'].apply(clean_url)
df['location'] = df['location'].apply(clean_location)
df['profile_url'] = df['profile_url'].apply(clean_url)

# 3. Add categories based on followers
def categorize_developer(row):
    followers = row['followers']
    repos = row['public_repos']
    
    if followers > 1000:
        return "Influencer"
    elif followers > 500:
        return "Well-Known"
    elif followers > 100:
        return "Active"
    elif repos > 50:
        return "Prolific"
    else:
        return "Regular"

df['category'] = df.apply(categorize_developer, axis=1)

# 4. Add contact availability score
def contact_score(row):
    score = 0
    if pd.notna(row['email']):
        score += 3
    if pd.notna(row['twitter']):
        score += 2
    if pd.notna(row['blog']):
        score += 1
    return score

df['contact_score'] = df.apply(contact_score, axis=1)

# 5. Sort by usefulness (followers + contact info)
df = df.sort_values(
    by=['contact_score', 'followers', 'public_repos'], 
    ascending=[False, False, False]
)

# 6. Reorder columns for better readability
column_order = [
    'github_username',
    'category',
    'contact_score',
    'email',
    'twitter',
    'location',
    'followers',
    'public_repos',
    'blog',
    'profile_url'
]

df = df[column_order]

# 7. Create separate filtered versions
# Developers with contact info
contactable = df[df['contact_score'] > 0].copy()

# High-value developers (followers > 100 OR email available)
high_value = df[(df['followers'] > 100) | (df['email'].notna())].copy()

# Influencers only
influencers = df[df['category'] == 'Influencer'].copy()

# 8. Save organized files
df.to_csv("laravel_devs_organized.csv", index=False)
contactable.to_csv("laravel_devs_contactable.csv", index=False)
high_value.to_csv("laravel_devs_high_value.csv", index=False)
influencers.to_csv("laravel_devs_influencers.csv", index=False)

# 9. Generate summary report
print("\n" + "="*50)
print("📈 SUMMARY REPORT")
print("="*50)
print(f"Total unique developers: {len(df)}")
print(f"With email: {df['email'].notna().sum()}")
print(f"With Twitter: {df['twitter'].notna().sum()}")
print(f"With blog: {df['blog'].notna().sum()}")
print(f"With location: {df['location'].notna().sum()}")
print(f"\nCategories:")
print(df['category'].value_counts().to_string())
print(f"\nTop 5 locations:")
print(df['location'].value_counts().head().to_string())
print(f"\n✅ Files created:")
print("  - laravel_devs_organized.csv (all developers)")
print("  - laravel_devs_contactable.csv (with email/twitter)")
print("  - laravel_devs_high_value.csv (followers > 100 OR has email)")
print("  - laravel_devs_influencers.csv (followers > 1000)")

# 10. Show top 10 developers
print("\n" + "="*50)
print("🌟 TOP 10 DEVELOPERS")
print("="*50)
print(df[['github_username', 'category', 'followers', 'email', 'twitter']].head(10).to_string(index=False))