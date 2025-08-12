#!/usr/bin/env python3

import os
import re
from pathlib import Path

def update_spoof_ad_image_references():
    """Update spoof-ad markdown files to use new asset paths"""
    
    spoof_ads_dir = Path("src/content/spoof-ads")
    assets_dir = Path("src/assets/spoof-ads")
    
    if not spoof_ads_dir.exists():
        print("Spoof ads directory not found")
        return
    
    if not assets_dir.exists():
        print("Assets directory not found")
        return
    
    # Get list of available images in assets
    available_images = {f.name: f for f in assets_dir.glob("*.*")}
    
    files_updated = 0
    
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
            
            # Extract current spoofImage from frontmatter
            spoof_image_match = re.search(r'spoofImage:\s*["\']?([^"\'\n]+)["\']?', frontmatter)
            if not spoof_image_match:
                continue
                
            current_path = spoof_image_match.group(1)
            
            # Extract filename from current path
            filename = os.path.basename(current_path)
            
            # Check if image exists in assets
            if filename in available_images:
                # Update frontmatter to use new path without /images/ prefix
                new_path = f"../../assets/spoof-ads/{filename}"
                new_frontmatter = frontmatter.replace(current_path, new_path)
                
                # Write back the file
                new_content = f"---{new_frontmatter}---{markdown_content}"
                
                with open(md_file, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                
                files_updated += 1
                print(f"Updated: {md_file.name} -> {new_path}")
            else:
                print(f"Warning: Image not found for {md_file.name}: {filename}")
            
        except Exception as e:
            print(f"Error processing {md_file}: {e}")
    
    print(f"\nUpdated {files_updated} files")

if __name__ == "__main__":
    update_spoof_ad_image_references()