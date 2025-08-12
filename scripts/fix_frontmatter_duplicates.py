#!/usr/bin/env python3
"""
Fix duplicate frontmatter fields in Astro markdown files
"""

import os
import re
import glob

def fix_frontmatter_duplicates(content_dir):
    """Fix duplicate frontmatter fields in all markdown files"""
    
    md_files = glob.glob(os.path.join(content_dir, '*.md'))
    fixed_files = []
    
    for md_file in md_files:
        print(f"Processing: {os.path.basename(md_file)}")
        
        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Split content to get frontmatter and article content
        parts = content.split('---', 2)
        if len(parts) < 3:
            print(f"  Invalid frontmatter format, skipping")
            continue
            
        frontmatter = parts[1]
        article_content = parts[2]
        
        # Parse frontmatter lines
        lines = frontmatter.strip().split('\n')
        cleaned_lines = []
        seen_fields = set()
        
        for line in lines:
            line = line.strip()
            if ':' in line:
                field_name = line.split(':', 1)[0].strip()
                if field_name in seen_fields:
                    print(f"  Removing duplicate field: {field_name}")
                    continue
                seen_fields.add(field_name)
            cleaned_lines.append(line)
        
        # Reconstruct frontmatter
        new_frontmatter = '\n'.join(cleaned_lines)
        
        # If we made changes, write the file back
        if len(cleaned_lines) != len(lines):
            new_content = f"---\n{new_frontmatter}\n---{article_content}"
            
            with open(md_file, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            fixed_files.append(os.path.basename(md_file))
            print(f"  ✓ Fixed frontmatter duplicates")
        else:
            print(f"  No duplicates found")
    
    print(f"\nFixed {len(fixed_files)} files:")
    for filename in fixed_files:
        print(f"  - {filename}")

if __name__ == "__main__":
    content_dir = "src/content/articles"
    
    print("Starting frontmatter duplicate fix...")
    print(f"Content directory: {content_dir}")
    
    fix_frontmatter_duplicates(content_dir)
    print("\nFrontmatter duplicate fix completed!")