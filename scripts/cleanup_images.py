#!/usr/bin/env python3
"""
Clean up image names by removing hash prefixes, update markdown references,
and delete unreferenced images.
"""

import os
import re
import glob
import shutil
from pathlib import Path

def clean_image_name(filename):
    """
    Clean up image filename by removing hash prefix.
    Examples:
    - 5f18a45126346c0ab4c9228c_Minutes_Midnight_2.png -> minutes-midnight.png
    - 642f4d74faceca8ca51df3ae_smash-phone-v2_2.gif -> smash-phone-v2.gif
    """
    # Remove the hash prefix (everything before the first underscore)
    if '_' in filename:
        parts = filename.split('_', 1)
        if len(parts[0]) > 20:  # Likely a hash
            clean_name = parts[1] if len(parts) > 1 else filename
        else:
            clean_name = filename
    else:
        clean_name = filename
    
    # Remove trailing numbers like _1, _2, _3 before extension
    name, ext = os.path.splitext(clean_name)
    name = re.sub(r'_\d+$', '', name)
    
    # Convert to lowercase and replace underscores with hyphens
    name = name.lower().replace('_', '-')
    
    # Remove any remaining special characters except hyphens
    name = re.sub(r'[^a-z0-9\-]', '-', name)
    
    # Remove multiple consecutive hyphens
    name = re.sub(r'-+', '-', name)
    
    # Remove leading/trailing hyphens
    name = name.strip('-')
    
    return name + ext.lower()

def get_all_image_references(content_dir):
    """
    Get all image references from markdown files.
    Returns a dict mapping old paths to list of files that reference them.
    """
    references = {}
    md_files = glob.glob(os.path.join(content_dir, '*.md'))
    
    for md_file in md_files:
        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Find all image references (both featured and inline)
        # Pattern for featuredImage
        featured_matches = re.findall(r'^featuredImage:\s*"([^"]+)"', content, re.MULTILINE)
        # Pattern for inline images
        inline_matches = re.findall(r'!\[([^\]]*)\]\(([^)]+)\)', content)
        
        # Collect all image paths
        for img_path in featured_matches:
            if img_path.startswith('/images/articles/'):
                if img_path not in references:
                    references[img_path] = []
                references[img_path].append(md_file)
        
        for alt_text, img_path in inline_matches:
            if img_path.startswith('/images/articles/'):
                if img_path not in references:
                    references[img_path] = []
                references[img_path].append(md_file)
    
    return references

def process_images_and_update_markdown(content_dir, images_dir):
    """
    Main processing function.
    """
    print("=" * 60)
    print("IMAGE CLEANUP SCRIPT")
    print("=" * 60)
    
    # Step 1: Get all current image references
    print("\n1. Analyzing current image references...")
    references = get_all_image_references(content_dir)
    print(f"   Found {len(references)} unique image references in markdown files")
    
    # Step 2: Create mapping of old names to new names
    print("\n2. Creating image rename mapping...")
    rename_map = {}
    name_conflicts = {}
    
    for old_path in references.keys():
        old_filename = os.path.basename(old_path)
        new_filename = clean_image_name(old_filename)
        
        # Handle name conflicts
        if new_filename in name_conflicts:
            # Add a counter to make it unique
            base, ext = os.path.splitext(new_filename)
            counter = name_conflicts[new_filename]
            name_conflicts[new_filename] += 1
            new_filename = f"{base}-{counter}{ext}"
        else:
            name_conflicts[new_filename] = 1
        
        new_path = f"/images/articles/{new_filename}"
        rename_map[old_path] = new_path
        
        if old_path != new_path:
            print(f"   {old_filename} -> {new_filename}")
    
    print(f"   {len([k for k, v in rename_map.items() if k != v])} images will be renamed")
    
    # Step 3: Rename actual image files
    print("\n3. Renaming image files...")
    renamed_count = 0
    for old_path, new_path in rename_map.items():
        old_file = os.path.join(images_dir, os.path.basename(old_path))
        new_file = os.path.join(images_dir, os.path.basename(new_path))
        
        if old_file != new_file and os.path.exists(old_file):
            # Check if target already exists
            if os.path.exists(new_file):
                print(f"   Warning: {os.path.basename(new_file)} already exists, skipping")
                continue
            
            shutil.move(old_file, new_file)
            renamed_count += 1
    
    print(f"   Renamed {renamed_count} image files")
    
    # Step 4: Update markdown files with new paths
    print("\n4. Updating markdown files...")
    updated_files = set()
    
    for md_file in glob.glob(os.path.join(content_dir, '*.md')):
        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Update all image references
        for old_path, new_path in rename_map.items():
            if old_path != new_path:
                # Update in featuredImage
                content = content.replace(f'featuredImage: "{old_path}"', 
                                        f'featuredImage: "{new_path}"')
                # Update in inline images
                content = content.replace(f']({old_path})', f']({new_path})')
        
        if content != original_content:
            with open(md_file, 'w', encoding='utf-8') as f:
                f.write(content)
            updated_files.add(md_file)
    
    print(f"   Updated {len(updated_files)} markdown files")
    
    # Step 5: Delete unreferenced images
    print("\n5. Cleaning up unreferenced images...")
    
    # Get all images currently in the directory
    all_images = set()
    for img_file in os.listdir(images_dir):
        if img_file.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.webp')):
            all_images.add(img_file)
    
    # Get all referenced images (after renaming)
    referenced_images = set()
    for new_path in rename_map.values():
        referenced_images.add(os.path.basename(new_path))
    
    # Find unreferenced images
    unreferenced = all_images - referenced_images
    
    # Delete unreferenced images
    deleted_count = 0
    for img_file in unreferenced:
        img_path = os.path.join(images_dir, img_file)
        os.remove(img_path)
        deleted_count += 1
        if deleted_count <= 10:  # Show first 10
            print(f"   Deleted: {img_file}")
    
    if deleted_count > 10:
        print(f"   ... and {deleted_count - 10} more")
    
    print(f"   Deleted {deleted_count} unreferenced images")
    
    # Final summary
    print("\n" + "=" * 60)
    print("CLEANUP COMPLETE")
    print("=" * 60)
    print(f"Images renamed:        {renamed_count}")
    print(f"Markdown files updated: {len(updated_files)}")
    print(f"Unreferenced deleted:  {deleted_count}")
    print(f"Final image count:     {len(referenced_images)}")
    
    return True

def main():
    """
    Main entry point.
    """
    content_dir = "/Users/web/adbusters-website-2025/src/content/articles"
    images_dir = "/Users/web/adbusters-website-2025/public/images/articles"
    
    # Check directories exist
    if not os.path.exists(content_dir):
        print(f"Error: Content directory not found: {content_dir}")
        return False
    
    if not os.path.exists(images_dir):
        print(f"Error: Images directory not found: {images_dir}")
        return False
    
    # Run the cleanup process
    return process_images_and_update_markdown(content_dir, images_dir)

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)