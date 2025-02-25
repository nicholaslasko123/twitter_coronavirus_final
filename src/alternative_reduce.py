#!/usr/bin/env python3
import argparse
import os
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# Parse command-line arguments
parser = argparse.ArgumentParser()
parser.add_argument('--hashtags', nargs='+', required=True,
                    help="List of hashtags to plot (e.g., --hashtags '#coronavirus' '#covid19')")
args = parser.parse_args()

# Dictionary to hold daily tweet counts per hashtag
hashtag_daily_counts = {}

# Process each hashtag
for hashtag in args.hashtags:
    daily_counts = {}
    # Iterate through each file in the outputs directory
    for filename in sorted(os.listdir('outputs')):
        # Only process language files (assumed to end with '.lang')
        if not filename.endswith('.lang'):
            continue
        file_path = os.path.join('outputs', filename)
        # Extract a date string from the filename (assuming date is at positions 10:18)
        date_str = filename[10:18]
        # Read the JSON data from the file
        if os.path.isfile(file_path):
            with open(file_path, 'r') as f:
                data = json.load(f)
            # Get the counts for the hashtag (default to an empty dict if missing)
            count = sum(data.get(hashtag, {}).values())
            daily_counts[date_str] = count
    hashtag_daily_counts[hashtag] = daily_counts

# Create a line plot for each hashtag
plt.figure(figsize=(16, 10))
for hashtag, counts_by_date in hashtag_daily_counts.items():
    dates = sorted(counts_by_date.keys())
    tweet_counts = [counts_by_date[date] for date in dates]
    plt.plot(dates, tweet_counts, label=hashtag, linewidth=1.7)

plt.xlabel('Date', fontsize=14)
plt.ylabel('Tweet Count', fontsize=14)
plt.title('Tweet Counts by Hashtag', fontsize=16)
plt.legend()
plt.tight_layout()
plt.savefig('hashtag_trends.png')
plt.close()

