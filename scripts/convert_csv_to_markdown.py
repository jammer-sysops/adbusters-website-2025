#!/usr/bin/env python3
"""
Convert Adbusters CSV articles to TinaCMS markdown format

Note: The featuredImage field in the frontmatter will contain the original URL.
You'll need to download and upload these images through TinaCMS media manager
for proper integration.
"""

import csv
import os
import re
from datetime import datetime
try:
    from html import unescape
except ImportError:
    try:
        from HTMLParser import HTMLParser
        unescape = HTMLParser().unescape
    except ImportError:
        # Fallback for very old Python versions
        def unescape(s):
            s = s.replace("&lt;", "<")
            s = s.replace("&gt;", ">")
            s = s.replace("&amp;", "&")
            s = s.replace("&quot;", '"')
            s = s.replace("&#39;", "'")
            return s

def clean_filename(filename):
    """Create a clean filename from slug"""
    # Remove special characters and limit length
    filename = re.sub(r'[^\w\s-]', '', filename)
    filename = re.sub(r'[-\s]+', '-', filename)
    return filename[:100].strip('-')

def parse_date(date_str):
    """Parse date string to ISO format"""
    try:
        # Parse the date string (e.g., "Fri Mar 24 2023 21:58:40 GMT+0000 (Coordinated Universal Time)")
        # Extract the date part before GMT
        date_part = date_str.split(' GMT')[0]
        dt = datetime.strptime(date_part, '%a %b %d %Y %H:%M:%S')
        return dt.isoformat() + 'Z'
    except:
        # Return current date if parsing fails
        return datetime.now().isoformat() + 'Z'

def convert_html_to_markdown(html_content):
    """Convert HTML content to markdown using basic regex"""
    if not html_content:
        return ""
    
    # Unescape HTML entities first
    content = unescape(html_content)
    
    # Basic HTML to Markdown conversion
    # Convert headers
    for i in range(6, 0, -1):
        pattern = '<h%d[^>]*>(.*?)</h%d>' % (i, i)
        replacement = '#' * i + r' \1\n'
        content = re.sub(pattern, replacement, content, flags=re.IGNORECASE | re.DOTALL)
    
    # Convert paragraphs
    content = re.sub(r'<p[^>]*>(.*?)</p>', r'\1\n\n', content, flags=re.IGNORECASE | re.DOTALL)
    
    # Convert bold
    content = re.sub(r'<strong[^>]*>(.*?)</strong>', r'**\1**', content, flags=re.IGNORECASE | re.DOTALL)
    content = re.sub(r'<b[^>]*>(.*?)</b>', r'**\1**', content, flags=re.IGNORECASE | re.DOTALL)
    
    # Convert italic
    content = re.sub(r'<em[^>]*>(.*?)</em>', r'*\1*', content, flags=re.IGNORECASE | re.DOTALL)
    content = re.sub(r'<i[^>]*>(.*?)</i>', r'*\1*', content, flags=re.IGNORECASE | re.DOTALL)
    
    # Convert links
    content = re.sub(r'<a[^>]*href="([^"]*)"[^>]*>(.*?)</a>', r'[\2](\1)', content, flags=re.IGNORECASE | re.DOTALL)
    
    # Convert images
    content = re.sub(r'<img[^>]*src="([^"]*)"[^>]*alt="([^"]*)"[^>]*/?>', r'![\2](\1)', content, flags=re.IGNORECASE | re.DOTALL)
    content = re.sub(r'<img[^>]*src="([^"]*)"[^>]*/?>', r'![](\1)', content, flags=re.IGNORECASE | re.DOTALL)
    
    # Convert line breaks
    content = re.sub(r'<br\s*/?>', '\n', content, flags=re.IGNORECASE)
    
    # Convert blockquotes
    content = re.sub(r'<blockquote[^>]*>(.*?)</blockquote>', lambda m: '> ' + m.group(1).strip().replace('\n', '\n> ') + '\n', content, flags=re.IGNORECASE | re.DOTALL)
    
    # Convert lists
    content = re.sub(r'<ul[^>]*>(.*?)</ul>', lambda m: re.sub(r'<li[^>]*>(.*?)</li>', r'- \1\n', m.group(1), flags=re.IGNORECASE | re.DOTALL), content, flags=re.IGNORECASE | re.DOTALL)
    content = re.sub(r'<ol[^>]*>(.*?)</ol>', lambda m: '\n'.join(['%d. %s' % (i+1, item.strip()) for i, item in enumerate(re.findall(r'<li[^>]*>(.*?)</li>', m.group(1), flags=re.IGNORECASE | re.DOTALL))]) + '\n', content, flags=re.IGNORECASE | re.DOTALL)
    
    # Remove remaining HTML tags
    content = re.sub(r'<[^>]+>', '', content)
    
    # Clean up excessive whitespace
    content = re.sub(r'\n{3,}', '\n\n', content)
    content = re.sub(r' +', ' ', content)
    
    return content.strip()

def process_csv_to_markdown(csv_file, output_dir):
    """Process CSV file and convert to markdown files"""
    
    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    with open(csv_file, 'r') as f:
        reader = csv.DictReader(f)
        
        count = 0
        for row in reader:
            # Skip if article is archived or draft
            if row.get('Archived', '').lower() == 'true' or row.get('Draft', '').lower() == 'true':
                continue
            
            # Extract fields - updated for new CSV structure
            title = row.get('Name', 'Untitled')
            slug = row.get('Slug', clean_filename(title.lower()))
            
            # Use "Article published date" if available, otherwise "Published On"
            published_date = row.get('Article published date', '') or row.get('Published On', '')
            published_on = parse_date(published_date) if published_date else None
            
            # Build frontmatter
            frontmatter = """---
title: "%s\"""" % title
            
            if published_on:
                frontmatter += '\npublishedOn: %s' % published_on
            
            # Add author field - updated field names
            author_source = row.get('Author') or row.get('From AB issue', '')
            if author_source:
                if row.get('From AB issue'):
                    # Format as "- Author - Adbusters #Issue"
                    author_string = "- %s" % author_source
                    if row.get('From AB issue'):
                        author_string += " - Adbusters #%s" % row['From AB issue']
                    frontmatter += '\nauthor: "%s"' % author_string
                else:
                    frontmatter += '\nauthor: "%s"' % author_source
            
            # Use "Featured image" field for featuredImage
            if row.get('Featured image'):
                frontmatter += '\nfeaturedImage: "%s"' % row["Featured image"]
            
            frontmatter += "\n---\n\n"
            
            # Convert content from HTML to markdown
            # Try multiple content fields in order of preference
            content_raw = (
                row.get('Article content (Rich text)', '') or 
                row.get('Article blurb', '') or 
                row.get('Short Article Preview', '')
            )
            content = convert_html_to_markdown(content_raw)
            
            # Write to file
            filename = "%s.md" % clean_filename(slug)
            filepath = os.path.join(output_dir, filename)
            
            with open(filepath, 'w') as out_file:
                out_file.write(frontmatter + content)
            
            count += 1
            print("Created: %s" % filename)
    
    print("\nConverted %d articles to markdown files in %s" % (count, output_dir))

if __name__ == "__main__":
    csv_file = "old-content/Adbusters New Homepage - Articles.csv"
    output_dir = "src/content/articles"
    
    # Check if csv file exists
    if not os.path.exists(csv_file):
        print("Error: CSV file not found at %s" % csv_file)
        print("Available CSV files:")
        for f in os.listdir("old-content"):
            if f.endswith('.csv'):
                print("  - old-content/%s" % f)
        exit(1)
    
    print("Converting CSV: %s" % csv_file)
    print("Output directory: %s" % output_dir)
    process_csv_to_markdown(csv_file, output_dir)