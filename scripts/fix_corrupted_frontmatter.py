#!/usr/bin/env python3
"""
Fix corrupted frontmatter where multiple fields got merged into title
"""

import os
import re

def fix_corrupted_frontmatter(file_path):
    """Fix corrupted frontmatter in a markdown file"""
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Look for corrupted frontmatter where title contains other fields
    pattern1 = r'^---\ntitle: "([^"]*) publishedOn: ([^"]*) author: ([^"]*)"'
    pattern2 = r'^---\ntitle: "([^"]*) publishedOn: ([^"]*) authorSource: ([^"]*)"'
    
    match = re.match(pattern1, content, re.MULTILINE)
    if not match:
        match = re.match(pattern2, content, re.MULTILINE)
    
    if match:
        title = match.group(1)
        published_on = match.group(2)
        author = match.group(3)
        
        # Extract the rest of the content after the corrupted frontmatter
        rest_content = content[match.end():]
        
        # Build proper frontmatter
        new_frontmatter = f"""---
title: "{title}"
publishedOn: {published_on}
author: "{author}\""""
        
        # Look for featuredImage in the rest
        featured_match = re.search(r'\nfeaturedImage: "([^"]*)"', rest_content)
        if featured_match:
            new_frontmatter += f'\nfeaturedImage: "{featured_match.group(1)}"'
            # Remove the featuredImage from rest_content
            rest_content = rest_content.replace(featured_match.group(0), '')
        
        new_frontmatter += "\n---"
        
        # Find where the actual content starts (after the broken frontmatter)
        content_start = re.search(r'\n---\n', rest_content)
        if content_start:
            body = rest_content[content_start.end():]
        else:
            body = rest_content
        
        # Reconstruct the file
        new_content = new_frontmatter + '\n' + body
        
        with open(file_path, 'w') as f:
            f.write(new_content)
        
        return True
    
    return False

def main():
    articles_dir = "src/content/articles"
    fixed_count = 0
    
    for filename in os.listdir(articles_dir):
        if filename.endswith('.md'):
            file_path = os.path.join(articles_dir, filename)
            if fix_corrupted_frontmatter(file_path):
                print("Fixed corrupted frontmatter: %s" % filename)
                fixed_count += 1
    
    print("\nFixed corrupted frontmatter in %d files" % fixed_count)

if __name__ == "__main__":
    main()