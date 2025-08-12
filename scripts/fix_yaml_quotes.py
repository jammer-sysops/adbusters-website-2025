#!/usr/bin/env python3
"""
Fix YAML quote issues in frontmatter
"""

import os
import re
import glob

def fix_yaml_quotes(content_dir):
    """Fix YAML quote issues in all markdown files"""
    
    md_files = glob.glob(os.path.join(content_dir, '*.md'))
    fixed_files = []
    
    for md_file in md_files:
        print(f"Processing: {os.path.basename(md_file)}")
        
        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Split content to get frontmatter and article content
        parts = content.split('---', 2)
        if len(parts) < 3:
            continue
            
        frontmatter = parts[1]
        article_content = parts[2]
        
        # Fix double quotes in title field
        original_frontmatter = frontmatter
        
        # Fix title: ""something"" -> title: "something"
        frontmatter = re.sub(r'^title:\s*"([^"]*)"([^"]*)"', r'title: "\1\2"', frontmatter, flags=re.MULTILINE)
        
        # Fix title: "something" text -> title: "something text"
        frontmatter = re.sub(r'^title:\s*"([^"]*)"([^"]*)', r'title: "\1\2"', frontmatter, flags=re.MULTILINE)
        
        if frontmatter != original_frontmatter:
            new_content = f"---{frontmatter}---{article_content}"
            
            with open(md_file, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            fixed_files.append(os.path.basename(md_file))
            print(f"  ✓ Fixed YAML quotes")
        else:
            print(f"  No quote issues found")
    
    print(f"\nFixed {len(fixed_files)} files:")
    for filename in fixed_files:
        print(f"  - {filename}")

if __name__ == "__main__":
    content_dir = "src/content/articles"
    
    print("Starting YAML quote fix...")
    print(f"Content directory: {content_dir}")
    
    fix_yaml_quotes(content_dir)
    print("\nYAML quote fix completed!")