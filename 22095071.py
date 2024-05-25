

# -*- coding: utf-8 -*-
"""
Created on Thu May 23 20:00:41 2024

@author: DELL
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from PIL import Image, ImageDraw, ImageFont
import glob

# Function to read a CSV file with different encodings
def read_csv_file(file_path):
    encodings = ['utf-8', 'ISO-8859-1', 'latin1', 'cp1252']
    for encoding in encodings:
        try:
            return pd.read_csv(file_path, encoding=encoding)
        except UnicodeDecodeError:
            continue
    raise ValueError(f"None of the encodings worked for {file_path}")

# List all CSV files in the working directory
file_paths = glob.glob('bfi_yearbook-*.csv')

# Read and concatenate all CSV files
data_frames = []
for file_path in file_paths:
    df = read_csv_file(file_path)
    data_frames.append(df)

# Concatenate all DataFrames
df = pd.concat(data_frames, ignore_index=True)

# Handle missing values (if necessary)
df = df.dropna()

# Extract relevant columns
df = df[['Widest point of release', 'Genre', 'Box office gross (£ million)', 'Title']]

# Total films produced per year
films_per_year = df.groupby('Widest point of release')['Title'].count().reset_index()

# Genre trends over time
genre_trends = df.groupby(['Widest point of release', 'Genre'])['Title'].count().unstack().fillna(0)

# Box office revenue trends
box_office_trends = df.groupby('Widest point of release')['Box office gross (£ million)'].sum().reset_index()

# Top grossing films
top_grossing_films = df.sort_values(by='Box office gross (£ million)', ascending=False).head(10)

# Set the style
sns.set(style='whitegrid')

# Set DPI for high resolution
dpi = 300

# Plot 1: Total films produced per year
plt.figure(figsize=(10, 6), dpi=dpi)
sns.lineplot(x='Widest point of release', y='Title', data=films_per_year, marker='o')
plt.title('Total Films Produced Per Year')
plt.xlabel('Year')
plt.ylabel('Number of Films')
plt.tight_layout()
plt.savefig('films_per_year.png', dpi=dpi)
plt.close()

# Plot 2: Genre trends over time
plt.figure(figsize=(10, 6), dpi=dpi)
genre_trends.plot(kind='area', stacked=True, colormap='tab20', figsize=(10, 6))
plt.title('Genre Trends Over Time')
plt.xlabel('Year')
plt.ylabel('Number of Films')
plt.legend(loc='upper left', bbox_to_anchor=(1, 1))
plt.tight_layout()
plt.savefig('genre_trends.png', dpi=dpi)
plt.close()

# Plot 3: Box office revenue trends
plt.figure(figsize=(10, 6), dpi=dpi)
sns.lineplot(x='Widest point of release', y='Box office gross (£ million)', data=box_office_trends, marker='o', color='green')
plt.title('Box Office Revenue Trends')
plt.xlabel('Year')
plt.ylabel('Box Office Revenue (£)')
plt.tight_layout()
plt.savefig('box_office_trends.png', dpi=dpi)
plt.close()

# Plot 4: Top grossing films
plt.figure(figsize=(10, 6), dpi=dpi)
sns.barplot(x='Box office gross (£ million)', y='Title', data=top_grossing_films, palette='viridis')
plt.title('Top 10 Grossing Films')
plt.xlabel('Box Office Revenue (£)')
plt.ylabel('Film Title')
plt.tight_layout()
plt.savefig('top_grossing_films.png', dpi=dpi)
plt.close()

# Open the images
images = [Image.open(f) for f in ['films_per_year.png', 'genre_trends.png', 'box_office_trends.png', 'top_grossing_films.png']]

# Combine images into a 2x2 grid
width, height = images[0].size
new_image = Image.new('RGB', (2 * width, 2 * height + 100), (255, 255, 255))  # Add space for title

# Paste images into the grid
new_image.paste(images[0], (0, 100))
new_image.paste(images[1], (width, 100))
new_image.paste(images[2], (0, height + 100))
new_image.paste(images[3], (width, height + 100))

# Optionally add title and descriptions
draw = ImageDraw.Draw(new_image)
# Use a larger font size for the title
title_font = ImageFont.truetype("arial.ttf", 60)
subtitle_font = ImageFont.truetype("arial.ttf", 40)

# Add a title at the top center
title_text = "British Film Institute - Cinema Trends"
title_bbox = draw.textbbox((0, 0), title_text, font=title_font)
title_width = title_bbox[2] - title_bbox[0]
title_height = title_bbox[3] - title_bbox[1]
title_x = (new_image.width - title_width) / 2
title_y = 20  # Set the Y position for the title
draw.text((title_x, title_y), title_text, fill="black", font=title_font)

# Add subtitle with student name and ID
subtitle_text = "Student Name: Abeeha Zafar, Student ID: 22095071"
subtitle_bbox = draw.textbbox((0, 0), subtitle_text, font=subtitle_font)
subtitle_width = subtitle_bbox[2] - subtitle_bbox[0]
subtitle_height = subtitle_bbox[3] - subtitle_bbox[1]
subtitle_x = (new_image.width - subtitle_width) / 2
subtitle_y = title_y + title_height + 10  # Set the Y position for the subtitle
draw.text((subtitle_x, subtitle_y), subtitle_text, fill="black", font=subtitle_font)

# Save the combined image with 300 DPI
new_image.save('22095071.png', dpi=(dpi, dpi))
new_image.show()
