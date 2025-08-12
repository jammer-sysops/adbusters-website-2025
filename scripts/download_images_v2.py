#!/usr/bin/env python3
"""
Improved image download script with better error handling and progress tracking.
Downloads all external images (featured and inline) and converts to local paths.
"""

import os
import re
import glob
import hashlib
from pathlib import Path
from urllib.parse import urlparse, unquote
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError
import time
import ssl

# Create SSL context that doesn't verify certificates (for some CDNs)
ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

def sanitize_filename(filename):
    """Sanitize filename to be filesystem-safe"""
    # Remove or replace invalid characters
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    
    # Limit length
    name, ext = os.path.splitext(filename)
    if len(name) > 100:
        name = name[:100]
    
    return name + ext

def get_filename_from_url(url):
    """Extract and sanitize filename from URL"""
    parsed = urlparse(url)
    
    # Try to get filename from path
    filename = os.path.basename(unquote(parsed.path))
    
    # Clean up filename - remove query parameters
    filename = filename.split('?')[0].split('#')[0]
    
    # If no filename or no extension, create one based on URL hash
    if not filename or '.' not in filename:
        # Use last part of URL path or domain
        url_hash = hashlib.md5(url.encode()).hexdigest()[:8]
        
        # Try to guess extension from URL
        if '.jpg' in url.lower() or '.jpeg' in url.lower():
            ext = '.jpg'
        elif '.png' in url.lower():
            ext = '.png'
        elif '.gif' in url.lower():
            ext = '.gif'
        elif '.webp' in url.lower():
            ext = '.webp'
        else:
            ext = '.jpg'  # Default to jpg
        
        filename = f"image_{url_hash}{ext}"
    
    return sanitize_filename(filename)

def download_image(url, output_path, max_retries=3):
    """Download image from URL with retry logic"""
    for attempt in range(max_retries):
        try:
            # Create request with headers to avoid bot detection
            req = Request(url, headers={
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.9',
                'Accept-Encoding': 'gzip, deflate, br',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1'
            })
            
            # Download with timeout
            with urlopen(req, timeout=30, context=ssl_context) as response:
                # Check if response is an image
                content_type = response.headers.get('Content-Type', '')
                if not content_type.startswith('image/'):
                    print(f"    Warning: Content-Type is {content_type}, may not be an image")
                
                # Read and save the image
                with open(output_path, 'wb') as f:
                    f.write(response.read())
                
                # Verify file was written and has content
                if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
                    return True
                else:
                    os.remove(output_path) if os.path.exists(output_path) else None
                    raise Exception("Downloaded file is empty")
                    
        except HTTPError as e:
            if e.code == 404:
                print(f"    ✗ Image not found (404): {url}")
                return False
            elif e.code == 403:
                print(f"    ✗ Access forbidden (403): {url}")
                return False
            else:
                print(f"    Attempt {attempt + 1}/{max_retries} failed: HTTP {e.code}")
        except URLError as e:
            print(f"    Attempt {attempt + 1}/{max_retries} failed: {str(e)}")
        except Exception as e:
            print(f"    Attempt {attempt + 1}/{max_retries} failed: {str(e)}")
        
        if attempt < max_retries - 1:
            time.sleep(2 ** attempt)  # Exponential backoff
    
    return False

def process_markdown_files(content_dir, images_dir):
    """Process all markdown files and download their images"""
    
    # Create images directory if it doesn't exist
    Path(images_dir).mkdir(parents=True, exist_ok=True)
    
    # Track statistics
    stats = {
        'files_processed': 0,
        'files_updated': 0,
        'images_downloaded': 0,
        'images_failed': 0,
        'images_skipped': 0
    }
    
    # Track downloaded images to avoid duplicates
    url_to_local = {}
    
    # Get all markdown files
    md_files = sorted(glob.glob(os.path.join(content_dir, '*.md')))
    total_files = len(md_files)
    
    print(f"\nFound {total_files} markdown files to process")
    print("=" * 60)
    
    for idx, md_file in enumerate(md_files, 1):
        filename = os.path.basename(md_file)
        print(f"\n[{idx}/{total_files}] Processing: {filename}")
        stats['files_processed'] += 1
        
        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Find all image URLs in the file
        image_urls = []
        
        # Pattern for featuredImage in frontmatter
        featured_pattern = r'^featuredImage:\s*"([^"]+)"'
        featured_match = re.search(featured_pattern, content, re.MULTILINE)
        if featured_match:
            url = featured_match.group(1)
            if url.startswith(('http://', 'https://')):
                image_urls.append(('featured', url, featured_match.group(0)))
        
        # Pattern for inline images
        inline_pattern = r'!\[([^\]]*)\]\((https?://[^)]+)\)'
        for match in re.finditer(inline_pattern, content):
            image_urls.append(('inline', match.group(2), match.group(0)))
        
        # Process each image URL
        file_updated = False
        for img_type, url, full_match in image_urls:
            # Skip if already processed
            if url in url_to_local:
                local_path = url_to_local[url]
                if img_type == 'featured':
                    content = content.replace(
                        f'featuredImage: "{url}"',
                        f'featuredImage: "{local_path}"'
                    )
                else:
                    content = content.replace(
                        full_match,
                        full_match.replace(url, local_path)
                    )
                print(f"  ✓ Reusing cached: {local_path}")
                file_updated = True
                stats['images_skipped'] += 1
                continue
            
            # Skip if already local
            if url.startswith('/images/'):
                print(f"  ⊙ Already local: {url}")
                stats['images_skipped'] += 1
                continue
            
            # Generate local filename
            local_filename = get_filename_from_url(url)
            
            # Check for filename conflicts
            base_name, ext = os.path.splitext(local_filename)
            counter = 1
            while os.path.exists(os.path.join(images_dir, local_filename)):
                # Check if existing file is the same (by size)
                existing_size = os.path.getsize(os.path.join(images_dir, local_filename))
                if existing_size > 0:  # File exists and has content
                    local_filename = f"{base_name}_{counter}{ext}"
                    counter += 1
                else:
                    break  # Reuse the name if file is empty
            
            # Download the image
            local_file_path = os.path.join(images_dir, local_filename)
            local_web_path = f"/images/articles/{local_filename}"
            
            print(f"  Downloading {img_type}: {url[:60]}...")
            print(f"    → {local_filename}")
            
            if download_image(url, local_file_path):
                # Update content with local path
                if img_type == 'featured':
                    content = content.replace(
                        f'featuredImage: "{url}"',
                        f'featuredImage: "{local_web_path}"'
                    )
                else:
                    content = content.replace(
                        full_match,
                        full_match.replace(url, local_web_path)
                    )
                
                url_to_local[url] = local_web_path
                stats['images_downloaded'] += 1
                file_updated = True
                print(f"    ✓ Success!")
                
                # Small delay to be polite
                time.sleep(0.3)
            else:
                stats['images_failed'] += 1
                print(f"    ✗ Failed to download")
        
        # Write updated content if changed
        if content != original_content:
            with open(md_file, 'w', encoding='utf-8') as f:
                f.write(content)
            stats['files_updated'] += 1
            print(f"  ✓ Updated markdown file")
        else:
            print(f"  ○ No changes needed")
    
    # Print summary
    print("\n" + "=" * 60)
    print("DOWNLOAD COMPLETE")
    print("=" * 60)
    print(f"Files processed:    {stats['files_processed']}")
    print(f"Files updated:      {stats['files_updated']}")
    print(f"Images downloaded:  {stats['images_downloaded']}")
    print(f"Images reused:      {stats['images_skipped']}")
    print(f"Images failed:      {stats['images_failed']}")
    print(f"\nAll images saved to: {images_dir}")
    
    return stats

def main():
    """Main entry point"""
    content_dir = "/Users/web/adbusters-website-2025/src/content/articles"
    images_dir = "/Users/web/adbusters-website-2025/public/images/articles"
    
    print("=" * 60)
    print("IMAGE DOWNLOAD SCRIPT v2")
    print("=" * 60)
    print(f"Content directory: {content_dir}")
    print(f"Images directory:  {images_dir}")
    
    # Check directories exist
    if not os.path.exists(content_dir):
        print(f"Error: Content directory not found: {content_dir}")
        return False
    
    # Run the download process
    stats = process_markdown_files(content_dir, images_dir)
    
    # Return success if no critical failures
    return stats['images_failed'] == 0 or stats['images_downloaded'] > 0

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)