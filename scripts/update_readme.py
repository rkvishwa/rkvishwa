import re
import urllib.request
import os

import ssl

def fetch_svg(url):
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, context=ctx) as response:
        return response.read().decode('utf-8')

def extract_stat(svg, pattern, group=1):
    match = re.search(pattern, svg, re.IGNORECASE | re.DOTALL)
    if match:
        return match.group(group).strip()
    return "N/A"

def main():
    username = "rkvishwa"
    
    print(f"Fetching stats for {username}...")
    
    # URLs for the stats
    streak_url = f"https://github-readme-streak-stats.herokuapp.com/?user={username}"
    stats_url = f"https://github-readme-stats.vercel.app/api?username={username}"
    
    try:
        streak_svg = fetch_svg(streak_url)
        stats_svg = fetch_svg(stats_url)
        
        # Extract Longest Streak
        # The SVG has a structure like: <!-- Longest Streak big number --> <g ...> <text ...> 124 </text>
        longest_streak = extract_stat(streak_svg, r'<!-- Longest Streak big number -->.*?<text[^>]*>\s*(\d+)\s*</text>')
        
        # Extract Current Streak
        current_streak = extract_stat(streak_svg, r'<!-- Current Streak big number -->.*?<text[^>]*>\s*(\d+)\s*</text>')
        
        # Extract Total Commits
        # <text ... data-testid="commits">3402</text>
        total_commits = extract_stat(stats_svg, r'data-testid="commits"[^>]*>\s*([0-9kK,.]+)\s*</text>')
        
        print(f"Longest Streak: {longest_streak}")
        print(f"Current Streak: {current_streak}")
        print(f"Total Commits: {total_commits}")
        
        # Read the README
        readme_path = os.path.join(os.path.dirname(__file__), '..', 'README.md')
        with open(readme_path, 'r', encoding='utf-8') as f:
            readme_content = f.read()
            
        # Update the README content
        # We need to replace the stats section.
        
        # Replace Longest streak
        readme_content = re.sub(
            r'Longest streak:.*?(\n)',
            f'Longest streak: {longest_streak} days\\1',
            readme_content
        )
        
        # Replace Current streak
        readme_content = re.sub(
            r'Current streak:.*?(\n)',
            f'Current streak: {current_streak} days\\1',
            readme_content
        )
        
        # Replace Total commits
        readme_content = re.sub(
            r'Total commits:.*?(\n)',
            f'Total commits: {total_commits}\\1',
            readme_content
        )
        
        # Write back
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(readme_content)
            
        print("README.md updated successfully!")
        
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        exit(1)

if __name__ == "__main__":
    main()
