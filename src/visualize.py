#!/usr/bin/env python3

# command line args
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--input_path',required=True)
parser.add_argument('--key',required=True)
parser.add_argument('--percent',action='store_true')
parser.add_argument('--output_filename', required=True, help='Filename for the output PNG file')
args = parser.parse_args()


# imports
import matplotlib
matplotlib.use('Agg')
import os
import json
from collections import Counter,defaultdict
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
import numpy as np

def create_bar_graph(data, file_name):
    # Sort data in ascending order for better visualization
    sorted_data_desc = sorted(data.items(), key=lambda item: item[1], reverse=True)[:10]
    sorted_data_asc = sorted(sorted_data_desc, key=lambda item: item[1])
    
    keys = [k for k, v in sorted_data_asc]
    values = [v for k, v in sorted_data_asc]

    # Create figure and apply styling
    plt.style.use('ggplot')
    fig, ax = plt.subplots(figsize=(10, 8))

    # Use a colormap for better visuals
    colors = plt.cm.viridis(np.linspace(0.3, 0.9, len(keys)))

    bars = ax.bar(keys, values, color=colors)

    # Labeling
    ax.set_xlabel('Keys', fontsize=14, fontweight='bold')
    ax.set_ylabel('Counts', fontsize=14, fontweight='bold')
    ax.set_title('Top 10 Hashtags Usage', fontsize=16, fontweight='bold', pad=20)
    ax.set_xticklabels(keys, rotation=45, ha="right", fontsize=12)
    ax.grid(axis='y', linestyle='--', alpha=0.7)

    # Add value labels on bars
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, height + 0.02*max(values), f'{int(height)}', 
                ha='center', fontsize=12, fontweight='bold')

    # Save figure
    plt.savefig(f'{file_name}.png', bbox_inches='tight', dpi=300)
    plt.close()

# open the input path
with open(args.input_path) as f:
    counts = json.load(f)

# normalize the counts by the total values
if args.percent:
    for k in counts[args.key]:
        counts[args.key][k] /= counts['_all'][k]

key_data = counts.get(args.key, {})
create_bar_graph(key_data, os.path.basename(args.input_path).split('.')[0])

