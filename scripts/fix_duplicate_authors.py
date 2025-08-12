#!/usr/bin/env python3
"""
Fix duplicate author fields in frontmatter
"""

import os
import re

def fix_duplicate_authors(file_path):
    """Fix duplicate author fields in a markdown file"""
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Look for frontmatter with duplicate author fields
    frontmatter_pattern = r'^---\n(.*?)\n---\n(.*)$'
    match = re.match(frontmatter_pattern, content, re.DOTALL)
    
    if not match:
        return False
    
    frontmatter = match.group(1)
    body = match.group(2)
    
    # Find all author lines
    author_lines = re.findall(r'^author: (.*)$', frontmatter, re.MULTILINE)
    
    if len(author_lines) <= 1:
        return False  # No duplicates
    
    # Keep the most complete author line (usually the one with issue number)
    best_author = ""
    for author in author_lines:
        if "Adbusters" in author or "-" in author:
            best_author = author
            break
    
    if not best_author:
        best_author = author_lines[-1]  # Use the last one
    
    # Remove all author lines and add the best one
    new_frontmatter = re.sub(r'^author: .*$', '', frontmatter, flags=re.MULTILINE)
    # Remove empty lines
    new_frontmatter = re.sub(r'\n\n+', '\n', new_frontmatter)
    # Add the best author line after title and publishedOn
    lines = new_frontmatter.split('\n')
    new_lines = []
    author_added = False
    
    for line in lines:
        new_lines.append(line)
        if line.startswith('publishedOn:') and not author_added:
            new_lines.append('author: ' + best_author)
            author_added = True
    
    if not author_added:
        new_lines.append('author: ' + best_author)
    
    new_frontmatter = '\n'.join(new_lines)
    
    # Reconstruct the file
    new_content = '---\n' + new_frontmatter + '\n---\n' + body
    
    with open(file_path, 'w') as f:
        f.write(new_content)
    
    return True

def main():
    articles_dir = "src/content/articles"
    fixed_count = 0
    
    for filename in os.listdir(articles_dir):
        if filename.endswith('.md'):
            file_path = os.path.join(articles_dir, filename)
            if fix_duplicate_authors(file_path):
                print("Fixed: %s" % filename)
                fixed_count += 1
    
    print("\nFixed %d files with duplicate author fields" % fixed_count)

if __name__ == "__main__":
    main()