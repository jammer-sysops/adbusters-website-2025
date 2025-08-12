#!/usr/bin/env python3

import os
import re
from pathlib import Path

def remove_duplicate_images_from_spoofads():
    """Remove duplicate images from spoof-ad markdown files that already exist in frontmatter"""
    
    spoof_ads_dir = Path("src/content/spoof-ads")
    
    if not spoof_ads_dir.exists():
        print("Spoof ads directory not found")
        return
    
    files_processed = 0
    images_removed = 0
    
    for md_file in spoof_ads_dir.glob("*.md"):
        try:
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Split into frontmatter and content
            if not content.startswith('---'):
                continue
                
            parts = content.split('---', 2)
            if len(parts) < 3:
                continue
                
            frontmatter = parts[1]
            markdown_content = parts[2]
            
            # Extract spoofImage from frontmatter
            spoof_image_match = re.search(r'spoofImage:\s*["\']?([^"\'\n]+)["\']?', frontmatter)
            if not spoof_image_match:
                continue
                
            spoof_image_path = spoof_image_match.group(1)
            
            # Remove markdown images that match the frontmatter spoofImage
            original_content = markdown_content
            
            # Remove images that exactly match the spoofImage path
            markdown_content = re.sub(
                rf'!\[[^\]]*\]\({re.escape(spoof_image_path)}\)\s*\n?',
                '',
                markdown_content
            )
            
            # Also remove any images with the same filename (in case of slight path differences)
            image_filename = os.path.basename(spoof_image_path)
            markdown_content = re.sub(
                rf'!\[[^\]]*\]\([^)]*{re.escape(image_filename)}\)\s*\n?',
                '',
                markdown_content
            )
            
            # Clean up extra newlines
            markdown_content = re.sub(r'\n{3,}', '\n\n', markdown_content)
            markdown_content = markdown_content.strip()
            
            if markdown_content != original_content:
                # Write back the file without duplicate images
                new_content = f"---{frontmatter}---\n\n{markdown_content}\n" if markdown_content else f"---{frontmatter}---\n"
                
                with open(md_file, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                
                images_removed += 1
                print(f"Removed duplicate image from: {md_file.name}")
            
            files_processed += 1
            
        except Exception as e:
            print(f"Error processing {md_file}: {e}")
    
    print(f"\nProcessed {files_processed} files")
    print(f"Removed duplicate images from {images_removed} files")

if __name__ == "__main__":
    remove_duplicate_images_from_spoofads()