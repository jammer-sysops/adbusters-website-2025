#!/usr/bin/env python3
"""
Promote first inline image to featured image when no featured image exists
"""

import os
import re
import glob

def promote_first_image_to_featured(content_dir):
    """Promote first inline image to featured image for articles without one"""
    
    md_files = glob.glob(os.path.join(content_dir, '*.md'))
    processed_files = []
    
    for md_file in md_files:
        print(f"\nProcessing: {os.path.basename(md_file)}")
        
        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if there's already a featuredImage
        featured_match = re.search(r'^featuredImage:\s*"([^"]+)"', content, re.MULTILINE)
        if featured_match:
            print(f"  Already has featured image: {featured_match.group(1)}")
            continue
            
        # Split content to get frontmatter and article content
        parts = content.split('---', 2)
        if len(parts) < 3:
            print(f"  Invalid frontmatter format")
            continue
            
        frontmatter = parts[1]
        article_content = parts[2]
        
        # Look for the first image at the very start of the article content
        article_content_stripped = article_content.strip()
        first_image_match = re.match(r'^!\[[^\]]*\]\(([^)]+)\)', article_content_stripped)
        
        if not first_image_match:
            print(f"  No first image found")
            continue
            
        first_image_url = first_image_match.group(1)
        first_image_full = first_image_match.group(0)
        
        print(f"  Found first image: {first_image_url}")
        
        # Add featuredImage to frontmatter
        new_frontmatter = frontmatter.rstrip() + f'\nfeaturedImage: "{first_image_url}"\n'
        
        # Remove the first image from article content
        # Find the exact position and remove it
        new_article_content = article_content_stripped[len(first_image_full):].lstrip()
        
        # Reconstruct the file
        new_content = f"---{new_frontmatter}---\n{new_article_content}"
        
        # Write the updated content back to the file
        with open(md_file, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        processed_files.append(os.path.basename(md_file))
        print(f"  ✓ Promoted to featured image and removed from content")
    
    print(f"\n\nProcessed {len(processed_files)} files:")
    for filename in processed_files:
        print(f"  - {filename}")

if __name__ == "__main__":
    content_dir = "src/content/articles"
    
    print("Starting first image promotion process...")
    print(f"Content directory: {content_dir}")
    
    promote_first_image_to_featured(content_dir)
    print("\nFirst image promotion completed!")