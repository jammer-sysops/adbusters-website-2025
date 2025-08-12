#!/usr/bin/env python3
"""
Download featured images from articles and update markdown files to use local paths
"""

import os
import re
import glob
from pathlib import Path
from urllib.parse import urlparse, unquote
from urllib.request import urlopen, Request
import time

def get_filename_from_url(url):
    """Extract filename from URL"""
    parsed = urlparse(url)
    filename = os.path.basename(unquote(parsed.path))
    
    # Clean up filename - remove any query parameters or fragments
    filename = filename.split('?')[0].split('#')[0]
    
    # Ensure we have a valid filename
    if not filename or '.' not in filename:
        filename = 'image.jpg'
    
    return filename

def download_image(url, output_path):
    """Download image from URL to output path"""
    try:
        # Create request with headers
        req = Request(url, headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        })
        
        # Download the file
        with urlopen(req, timeout=30) as response:
            with open(output_path, 'wb') as f:
                f.write(response.read())
        
        return True
    except Exception as e:
        print(f"Error downloading {url}: {e}")
        return False

def process_markdown_files(content_dir, images_dir):
    """Process all markdown files and download their featured images and inline images"""
    
    # Create images directory if it doesn't exist
    Path(images_dir).mkdir(parents=True, exist_ok=True)
    
    # Track downloaded images to avoid duplicates
    downloaded = {}
    
    # Process all markdown files
    md_files = glob.glob(os.path.join(content_dir, '*.md'))
    
    for md_file in md_files:
        print(f"\nProcessing: {os.path.basename(md_file)}")
        
        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        updated_content = content
        
        # Find all external images (both featured images and inline images)
        # Pattern for featuredImage in frontmatter
        featured_image_pattern = r'^featuredImage:\s*"([^"]+)"'
        # Pattern for inline images ![](url) or ![alt](url)
        inline_image_pattern = r'!\[([^\]]*)\]\((https?://[^)]+)\)'
        
        # Process featured images
        featured_match = re.search(featured_image_pattern, content, re.MULTILINE)
        if featured_match:
            image_url = featured_match.group(1)
            if image_url.startswith(('http://', 'https://')):
                local_path = process_image_url(image_url, images_dir, downloaded)
                if local_path:
                    updated_content = updated_content.replace(
                        f'featuredImage: "{image_url}"',
                        f'featuredImage: "{local_path}"'
                    )
                    print(f"  Updated featuredImage: {image_url} -> {local_path}")
        
        # Process all inline images
        inline_matches = re.findall(inline_image_pattern, content)
        for alt_text, image_url in inline_matches:
            if image_url.startswith(('http://', 'https://')):
                local_path = process_image_url(image_url, images_dir, downloaded)
                if local_path:
                    # Replace the specific image URL in the markdown
                    old_pattern = f'![{alt_text}]({image_url})'
                    new_pattern = f'![{alt_text}]({local_path})'
                    updated_content = updated_content.replace(old_pattern, new_pattern)
                    print(f"  Updated inline image: {image_url} -> {local_path}")
        
        # Write updated content back to file if changes were made
        if updated_content != content:
            with open(md_file, 'w', encoding='utf-8') as f:
                f.write(updated_content)
            print(f"  ✓ Updated markdown file")
        else:
            print(f"  No external images found or already processed")
    
    print(f"\n\nDownloaded {len(downloaded)} unique images to {images_dir}")
    print("All external images have been converted to local paths!")

def process_image_url(image_url, images_dir, downloaded):
    """Process a single image URL - download if needed and return local path"""
    
    # Skip if already a local path
    if image_url.startswith('/images/'):
        return None
    
    # Skip if already downloaded
    if image_url in downloaded:
        return downloaded[image_url]
    
    # Generate local filename
    filename = get_filename_from_url(image_url)
    
    # Handle duplicate filenames
    base_name, ext = os.path.splitext(filename)
    counter = 1
    while os.path.exists(os.path.join(images_dir, filename)):
        filename = f"{base_name}_{counter}{ext}"
        counter += 1
    
    # Download image
    local_file_path = os.path.join(images_dir, filename)
    print(f"  Downloading: {image_url}")
    print(f"  To: {filename}")
    
    if download_image(image_url, local_file_path):
        local_web_path = f"/images/articles/{filename}"
        downloaded[image_url] = local_web_path
        print(f"  ✓ Success!")
        
        # Small delay to be polite to the server
        time.sleep(0.5)
        return local_web_path
    else:
        print(f"  ✗ Failed to download image")
        return None

if __name__ == "__main__":
    content_dir = "src/content/articles"
    images_dir = "public/images/articles"
    
    print("Starting image download process for Astro content...")
    print(f"Content directory: {content_dir}")
    print(f"Images directory: {images_dir}")
    
    process_markdown_files(content_dir, images_dir)