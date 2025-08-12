#!/usr/bin/env python3
"""
Remove duplicate inline images that match the featured image in Astro markdown files
"""

import os
import re
import glob

def remove_duplicate_images(content_dir):
    """Remove duplicate inline images that match the featured image"""
    
    md_files = glob.glob(os.path.join(content_dir, '*.md'))
    processed_files = []
    
    for md_file in md_files:
        print(f"\nProcessing: {os.path.basename(md_file)}")
        
        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Find featuredImage in frontmatter
        featured_match = re.search(r'^featuredImage:\s*"([^"]+)"', content, re.MULTILINE)
        if not featured_match:
            print(f"  No featured image found")
            continue
            
        featured_image = featured_match.group(1)
        print(f"  Featured image: {featured_image}")
        
        # Split content to get frontmatter and article content
        parts = content.split('---', 2)
        if len(parts) < 3:
            print(f"  Invalid frontmatter format")
            continue
            
        frontmatter = f"---{parts[1]}---"
        article_content = parts[2]
        
        # Find the first inline image in the article content
        first_image_pattern = r'!\[[^\]]*\]\([^)]+\)'
        first_image_match = re.search(first_image_pattern, article_content)
        
        if not first_image_match:
            print(f"  No inline images found")
            continue
            
        first_image_full = first_image_match.group(0)
        
        # Extract the URL from the first image
        url_match = re.search(r'!\[[^\]]*\]\(([^)]+)\)', first_image_full)
        if not url_match:
            print(f"  Could not extract URL from first image")
            continue
            
        first_image_url = url_match.group(1)
        
        # Check if the first inline image matches the featured image
        if featured_image == first_image_url:
            print(f"  ✓ Found duplicate: {first_image_url}")
            
            # Remove the first occurrence of this image from article content
            # Be careful to only remove the first occurrence
            new_article_content = article_content.replace(first_image_full, '', 1)
            
            # Clean up any extra whitespace/newlines left behind
            new_article_content = re.sub(r'\n\n\n+', '\n\n', new_article_content)
            new_article_content = new_article_content.lstrip('\n')
            
            # Reconstruct the file
            new_content = frontmatter + new_article_content
            
            # Write the updated content back to the file
            with open(md_file, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            processed_files.append(os.path.basename(md_file))
            print(f"  ✓ Removed duplicate image")
        else:
            print(f"  No duplicate found (first image: {first_image_url})")
    
    print(f"\n\nProcessed {len(processed_files)} files:")
    for filename in processed_files:
        print(f"  - {filename}")

if __name__ == "__main__":
    content_dir = "src/content/articles"
    
    print("Starting duplicate image removal process...")
    print(f"Content directory: {content_dir}")
    
    remove_duplicate_images(content_dir)
    print("\nDuplicate image removal completed!")