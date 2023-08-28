import re
import os
from typing_extensions import Text

directory = "videos/"
file_names = os.listdir(directory)

# Filter files that are txt or mp4
file_names = [f for f in file_names if os.path.isfile(os.path.join(directory, f)) and (f.endswith('.txt') or f.endswith('.mp4'))]

# Sort the file names by modification time in descending order
file_names.sort(key=lambda x: os.path.getmtime(os.path.join(directory, x)), reverse=True)

# Get the latest txt and mp4 file names
latest_files = {}
for file in file_names:
    if file.endswith('.txt') and 'txt' not in latest_files:
        latest_files['txt'] = file
    elif file.endswith('.mp4') and 'mp4' not in latest_files:
        latest_files['mp4'] = file
    if len(latest_files) == 2:
        break

# Get the text file content and extract title and description
text_file = latest_files.get('txt')
video_file = latest_files.get('mp4')
with open(os.path.join(directory, text_file), 'r') as file:
    content = file.read()
    title_match = re.search(r'---Youtube title---\n(.*?)\n', content, flags=re.DOTALL)
    title = title_match.group(1) if title_match else None
    description_match = re.search(r'---Youtube description---\n([\s\S]*)', content)
    description = description_match.group(1) if description_match else None

# Run the upload script with the latest mp4 and txt files
if video_file and text_file:
    os.system(f'python3 upload.py --file="{directory}{video_file}" --privacyStatus="public" --title="{title}" --description="{description}"')
