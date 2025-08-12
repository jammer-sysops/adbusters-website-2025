#!/usr/bin/env python3
"""
Extract all image URLs from markdown files for reference
"""

import os
import re
import glob
import json

def extract_images(content_dir):
    """Extract all image URLs from markdown files"""
    
    images = {}
    md_files = glob.glob(os.path.join(content_dir, '*.md'))
    
    for md_file in md_files:
        filename = os.path.basename(md_file)
        
        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Find featuredImage in frontmatter
        match = re.search(r'^featuredImage:\s*"([^"]+)"', content, re.MULTILINE)
        
        if match:
            featured_image = match.group(1)
            
            # Also find all inline images
            inline_images = re.findall(r'!\[[^\]]*\]\(([^)]+)\)', content)
            
            images[filename] = {
                'featuredImage': featured_image,
                'inlineImages': inline_images
            }
    
    return images

if __name__ == "__main__":
    content_dir = "content/articles"
    
    images = extract_images(content_dir)
    
    # Save to JSON file
    with open('article_images.json', 'w', encoding='utf-8') as f:
        json.dump(images, f, indent=2)
    
    # Print summary
    print(f"Found {len(images)} articles with images")
    
    # Count unique URLs
    all_urls = set()
    for article in images.values():
        if article['featuredImage']:
            all_urls.add(article['featuredImage'])
        all_urls.update(article['inlineImages'])
    
    print(f"Total unique image URLs: {len(all_urls)}")
    print("\nImage data saved to article_images.json")