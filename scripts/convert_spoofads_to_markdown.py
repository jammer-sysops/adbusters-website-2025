#!/usr/bin/env python3
"""
Convert Spoof Ads CSV to markdown files with local images.
"""

import csv
import os
import re
import hashlib
import time
import ssl
from pathlib import Path
from urllib.parse import urlparse, unquote
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError
from datetime import datetime

# Create SSL context that doesn't verify certificates
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

def create_slug(name):
    """Create a URL-safe slug from name"""
    # Remove HTML tags if any
    name = re.sub(r'<[^>]+>', '', name)
    # Convert to lowercase and replace spaces/special chars with hyphens
    slug = re.sub(r'[^\w\s-]', '', name.lower())
    slug = re.sub(r'[-\s]+', '-', slug)
    return slug.strip('-')

def get_image_filename_from_url(url):
    """Extract and clean filename from URL"""
    parsed = urlparse(url)
    filename = os.path.basename(unquote(parsed.path))
    
    # Clean up filename - remove query parameters
    filename = filename.split('?')[0].split('#')[0]
    
    # Remove hash prefix if present (like those long webflow IDs)
    if '_' in filename and len(filename.split('_')[0]) > 20:
        parts = filename.split('_', 1)
        if len(parts) > 1:
            filename = parts[1]
    
    # Ensure we have a valid filename
    if not filename or '.' not in filename:
        url_hash = hashlib.md5(url.encode()).hexdigest()[:8]
        filename = f"spoof-ad-{url_hash}.jpg"
    
    # Make it clean
    name, ext = os.path.splitext(filename)
    name = re.sub(r'[^\w\s-]', '-', name.lower())
    name = re.sub(r'[-\s]+', '-', name)
    name = name.strip('-')
    
    return sanitize_filename(name + ext.lower())

def download_image(url, output_path, max_retries=3):
    """Download image from URL with retry logic"""
    for attempt in range(max_retries):
        try:
            # Create request with headers
            req = Request(url, headers={
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
                'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8'
            })
            
            # Download with timeout
            with urlopen(req, timeout=30, context=ssl_context) as response:
                with open(output_path, 'wb') as f:
                    f.write(response.read())
                
                # Verify file was written
                if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
                    return True
                else:
                    if os.path.exists(output_path):
                        os.remove(output_path)
                    raise Exception("Downloaded file is empty")
                    
        except HTTPError as e:
            print(f"    HTTP Error {e.code}: {e.reason}")
            return False
        except URLError as e:
            print(f"    URL Error: {str(e)}")
        except Exception as e:
            print(f"    Attempt {attempt + 1}/{max_retries} failed: {str(e)}")
        
        if attempt < max_retries - 1:
            time.sleep(2 ** attempt)
    
    return False

def convert_date(date_str):
    """Convert date string to ISO format"""
    if not date_str:
        return None
    
    try:
        # Parse the date format from CSV
        if 'GMT' in date_str:
            # Format like "Fri Jul 30 2021 18:19:29 GMT+0000 (Coordinated Universal Time)"
            clean_date = re.sub(r'\s*GMT.*$', '', date_str)
            clean_date = re.sub(r'^[A-Za-z]+\s+', '', clean_date)  # Remove day of week
            dt = datetime.strptime(clean_date, '%b %d %Y %H:%M:%S')
        else:
            dt = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
        
        return dt.strftime('%Y-%m-%d')
    except (ValueError, AttributeError):
        return None

def process_spoofads_csv(csv_path, content_dir, images_dir):
    """Process the Spoof Ads CSV file"""
    print(f"Processing Spoof Ads CSV: {csv_path}")
    
    # Track statistics
    stats = {
        'processed': 0,
        'errors': 0,
        'images_downloaded': 0,
        'images_failed': 0
    }
    
    # Track downloaded images to avoid duplicates
    downloaded_images = {}
    
    with open(csv_path, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        
        for row_num, row in enumerate(reader, 2):
            try:
                # Extract fields
                name = row.get('Name', '').strip()
                if not name:
                    print(f"Row {row_num}: Skipping - no name")
                    continue
                
                slug = row.get('Slug', create_slug(name)).strip()
                created_date = convert_date(row.get('Created On', ''))
                spoof_image_url = row.get('Spoofs Images', '').strip()
                spoof_category = row.get('Spoof Category', '').strip()
                caption = row.get('Caption', '').strip()
                author_credit = row.get('Author Credit', '').strip()
                
                print(f"\n[{row_num - 1}] Processing: {name}")
                
                # Download image if URL provided
                local_image_path = ""
                if spoof_image_url and spoof_image_url.startswith('http'):
                    # Check if already downloaded
                    if spoof_image_url in downloaded_images:
                        local_image_path = downloaded_images[spoof_image_url]
                        print(f"  ✓ Reusing cached image: {local_image_path}")
                    else:
                        # Generate local filename
                        image_filename = get_image_filename_from_url(spoof_image_url)
                        
                        # Check for conflicts
                        base_name, ext = os.path.splitext(image_filename)
                        counter = 1
                        while os.path.exists(os.path.join(images_dir, image_filename)):
                            image_filename = f"{base_name}-{counter}{ext}"
                            counter += 1
                        
                        # Download image
                        local_file_path = os.path.join(images_dir, image_filename)
                        print(f"  Downloading image: {spoof_image_url[:60]}...")
                        print(f"    → {image_filename}")
                        
                        if download_image(spoof_image_url, local_file_path):
                            local_image_path = f"/images/spoof-ads/{image_filename}"
                            downloaded_images[spoof_image_url] = local_image_path
                            stats['images_downloaded'] += 1
                            print(f"    ✓ Success!")
                            time.sleep(0.3)  # Be polite
                        else:
                            stats['images_failed'] += 1
                            print(f"    ✗ Failed to download")
                            # Continue anyway, we'll note the missing image
                            local_image_path = spoof_image_url
                else:
                    local_image_path = spoof_image_url or ""
                
                # Build frontmatter
                frontmatter_lines = ['---']
                frontmatter_lines.append(f'name: "{name}"')
                
                if created_date:
                    frontmatter_lines.append(f'createdOn: {created_date}')
                
                if local_image_path:
                    frontmatter_lines.append(f'spoofImage: "{local_image_path}"')
                else:
                    frontmatter_lines.append('spoofImage: ""')
                
                if spoof_category:
                    frontmatter_lines.append(f'spoofCategory: "{spoof_category}"')
                
                if caption:
                    # Escape quotes in caption
                    caption_safe = caption.replace('"', '\\"')
                    frontmatter_lines.append(f'caption: "{caption_safe}"')
                
                if author_credit:
                    # Escape quotes in author credit
                    author_safe = author_credit.replace('"', '\\"')
                    frontmatter_lines.append(f'authorCredit: "{author_safe}"')
                
                frontmatter_lines.append('---')
                frontmatter = '\n'.join(frontmatter_lines)
                
                # Create markdown content
                content = ""
                if local_image_path:
                    alt_text = caption if caption else name
                    content = f"![{alt_text}]({local_image_path})\n"
                
                if caption and caption not in name:
                    content += f"\n{caption}\n"
                
                if author_credit:
                    content += f"\n*{author_credit}*\n"
                
                # Write markdown file
                filename = f"{slug}.md"
                filepath = os.path.join(content_dir, filename)
                
                with open(filepath, 'w', encoding='utf-8') as md_file:
                    md_file.write(frontmatter + '\n\n' + content)
                
                stats['processed'] += 1
                print(f"  ✓ Created: {filename}")
                
                if stats['processed'] % 10 == 0:
                    print(f"\nProgress: {stats['processed']} spoof ads processed...")
                    
            except Exception as e:
                print(f"Row {row_num}: Error processing - {e}")
                stats['errors'] += 1
    
    return stats

def main():
    """Main conversion function"""
    # Paths
    csv_path = '/Users/web/adbusters-website-2025/old-content/Adbusters New Homepage - Spoofs Ads.csv'
    content_dir = '/Users/web/adbusters-website-2025/src/content/spoof-ads'
    images_dir = '/Users/web/adbusters-website-2025/public/images/spoof-ads'
    
    print("=" * 60)
    print("SPOOF ADS CSV TO MARKDOWN CONVERTER")
    print("=" * 60)
    print(f"CSV file:    {csv_path}")
    print(f"Content dir: {content_dir}")
    print(f"Images dir:  {images_dir}")
    
    # Check if CSV exists
    if not os.path.exists(csv_path):
        print(f"\nError: CSV file not found: {csv_path}")
        return False
    
    # Create directories if needed
    Path(content_dir).mkdir(parents=True, exist_ok=True)
    Path(images_dir).mkdir(parents=True, exist_ok=True)
    
    # Clear existing spoof ads
    print("\nClearing existing spoof ads...")
    for file in os.listdir(content_dir):
        if file.endswith('.md'):
            os.remove(os.path.join(content_dir, file))
    
    # Process CSV
    stats = process_spoofads_csv(csv_path, content_dir, images_dir)
    
    # Print summary
    print("\n" + "=" * 60)
    print("CONVERSION COMPLETE")
    print("=" * 60)
    print(f"Spoof ads processed:  {stats['processed']}")
    print(f"Images downloaded:    {stats['images_downloaded']}")
    print(f"Images failed:        {stats['images_failed']}")
    print(f"Errors:               {stats['errors']}")
    
    if stats['errors'] > 0:
        print(f"\n⚠️  {stats['errors']} errors occurred. Check output above for details.")
        return stats['processed'] > 0
    else:
        print("\n✅ All spoof ads converted successfully!")
        return True

if __name__ == '__main__':
    success = main()
    exit(0 if success else 1)