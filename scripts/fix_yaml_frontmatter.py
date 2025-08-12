#!/usr/bin/env python3
"""
Fix YAML frontmatter issues in markdown files
"""

import os
import re

def fix_yaml_frontmatter(file_path):
    """Fix YAML frontmatter issues in a markdown file"""
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Look for frontmatter
    frontmatter_pattern = r'^---\n(.*?)\n---(.*)$'
    match = re.match(frontmatter_pattern, content, re.DOTALL)
    
    if not match:
        return False
    
    frontmatter = match.group(1)
    body = match.group(2)
    
    original_frontmatter = frontmatter
    
    # Fix multiline titles
    frontmatter = re.sub(r'^title: "([^"]*)\n([^"]*)"', r'title: "\1 \2"', frontmatter, flags=re.MULTILINE)
    
    # Fix authorSource with multilines
    frontmatter = re.sub(r'^authorSource: ([^\n]*)\n\n([^\n]*)""', r'author: "\1 \2"', frontmatter, flags=re.MULTILINE)
    
    # Fix broken quotes at end of title
    frontmatter = re.sub(r'^title: "([^"]*)\n([^"]*)', r'title: "\1 \2"', frontmatter, flags=re.MULTILINE)
    
    # Fix broken author lines with trailing quotes
    frontmatter = re.sub(r'^author: ([^"]*)"', r'author: "\1"', frontmatter, flags=re.MULTILINE)
    
    # Fix missing quotes around values that need them
    frontmatter = re.sub(r'^(title|author): ([^"][^"\n]*[^"])$', r'\1: "\2"', frontmatter, flags=re.MULTILINE)
    
    # Clean up extra quotes
    frontmatter = re.sub(r'^(title|author): ""([^"]*)"', r'\1: "\2"', frontmatter, flags=re.MULTILINE)
    
    # Remove empty lines in frontmatter
    frontmatter = re.sub(r'\n\n+', '\n', frontmatter)
    
    # Ensure body starts with newline
    if not body.startswith('\n'):
        body = '\n' + body
    
    if frontmatter != original_frontmatter:
        # Reconstruct the file
        new_content = '---\n' + frontmatter + '\n---' + body
        
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
            if fix_yaml_frontmatter(file_path):
                print("Fixed YAML: %s" % filename)
                fixed_count += 1
    
    print("\nFixed YAML frontmatter in %d files" % fixed_count)

if __name__ == "__main__":
    main()