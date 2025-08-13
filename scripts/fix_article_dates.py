#!/usr/bin/env python3
"""
Fix article dates using the Created On field from CSV files.
This script updates the publishedOn date in markdown frontmatter with the correct creation date.
"""

import os
import csv
import re
from datetime import datetime

def parse_csv_date(date_str):
    """Parse the date string from CSV (e.g. 'Wed Jul 22 2020 20:43:04 GMT+0000 (Coordinated Universal Time)')"""
    if not date_str:
        return None
    
    try:
        # Remove GMT and timezone info
        date_part = date_str.split(' GMT')[0]
        # Remove day of week prefix
        date_part = ' '.join(date_part.split()[1:])
        # Parse the date (format: "Jul 22 2020 20:43:04")
        dt = datetime.strptime(date_part, '%b %d %Y %H:%M:%S')
        return dt.strftime('%Y-%m-%dT%H:%M:%SZ')
    except Exception as e:
        print(f"Error parsing date '{date_str}': {e}")
        return None

def create_slug_from_title(title):
    """Create a slug from title to match markdown filenames"""
    # Convert to lowercase and replace spaces/special chars with hyphens
    slug = re.sub(r'[^\w\s-]', '', title.lower())
    slug = re.sub(r'[-\s]+', '-', slug)
    return slug.strip('-')

def load_csv_dates(csv_path):
    """Load dates from CSV file, indexed by slug"""
    dates_by_slug = {}
    
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Get slug (use provided slug or generate from title)
            slug = row.get('Slug', '').strip()
            if not slug:
                title = row.get('Name', '')
                if title:
                    slug = create_slug_from_title(title)
            
            if slug:
                # Get Created On date
                created_date = row.get('Created On', '')
                if created_date:
                    parsed_date = parse_csv_date(created_date)
                    if parsed_date:
                        dates_by_slug[slug] = parsed_date
                        # Also store with potential filename variations
                        dates_by_slug[slug[:100]] = parsed_date  # Truncated version
    
    return dates_by_slug

def update_markdown_file(filepath, new_date):
    """Update the publishedOn date in a markdown file's frontmatter"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if file has frontmatter
    if not content.startswith('---'):
        print(f"  No frontmatter found in {filepath}")
        return False
    
    # Split frontmatter and content
    parts = content.split('---', 2)
    if len(parts) < 3:
        print(f"  Invalid frontmatter structure in {filepath}")
        return False
    
    frontmatter = parts[1]
    body = parts[2]
    
    # Update or add publishedOn field
    if 'publishedOn:' in frontmatter:
        # Replace existing publishedOn
        frontmatter = re.sub(
            r'publishedOn:.*$',
            f'publishedOn: {new_date}',
            frontmatter,
            count=1,
            flags=re.MULTILINE
        )
    else:
        # Add publishedOn after title
        lines = frontmatter.split('\n')
        new_lines = []
        for line in lines:
            new_lines.append(line)
            if line.startswith('title:'):
                new_lines.append(f'publishedOn: {new_date}')
        frontmatter = '\n'.join(new_lines)
    
    # Write back to file
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write('---' + frontmatter + '---' + body)
    
    return True

def main():
    """Main function to update all article dates"""
    print("=== Fixing Article Dates from CSV ===\n")
    
    # Paths
    articles_dir = '/Users/web/adbusters-website-2025/src/content/articles'
    articles_csv = '/Users/web/adbusters-website-2025/old-content/Adbusters New Homepage - Articles.csv'
    full_articles_csv = '/Users/web/adbusters-website-2025/old-content/Adbusters New Homepage - Full Articles.csv'
    
    # Load dates from both CSV files
    print("Loading dates from CSV files...")
    dates_by_slug = {}
    
    # Load from Articles CSV
    if os.path.exists(articles_csv):
        articles_dates = load_csv_dates(articles_csv)
        dates_by_slug.update(articles_dates)
        print(f"  Loaded {len(articles_dates)} dates from Articles.csv")
    
    # Load from Full Articles CSV (these will override Articles.csv if duplicate)
    if os.path.exists(full_articles_csv):
        full_articles_dates = load_csv_dates(full_articles_csv)
        dates_by_slug.update(full_articles_dates)
        print(f"  Loaded {len(full_articles_dates)} dates from Full Articles.csv")
    
    print(f"\nTotal unique articles with dates: {len(dates_by_slug)}\n")
    
    # Process markdown files
    updated_count = 0
    skipped_count = 0
    error_count = 0
    
    for filename in os.listdir(articles_dir):
        if not filename.endswith('.md'):
            continue
        
        # Extract slug from filename
        slug = filename[:-3]  # Remove .md extension
        
        # Look for matching date
        if slug in dates_by_slug:
            filepath = os.path.join(articles_dir, filename)
            new_date = dates_by_slug[slug]
            
            print(f"Updating {filename}:")
            print(f"  New date: {new_date}")
            
            if update_markdown_file(filepath, new_date):
                updated_count += 1
                print(f"  ✓ Updated successfully")
            else:
                error_count += 1
                print(f"  ✗ Failed to update")
        else:
            skipped_count += 1
            print(f"Skipping {filename}: No matching date found in CSV")
    
    # Summary
    print("\n=== Summary ===")
    print(f"Updated: {updated_count} articles")
    print(f"Skipped: {skipped_count} articles (no date found)")
    print(f"Errors: {error_count} articles")
    
    if updated_count > 0:
        print("\n✅ Date update completed successfully!")
    else:
        print("\n⚠️  No articles were updated. Check if slugs match between CSV and markdown files.")
    
    return updated_count > 0

if __name__ == '__main__':
    success = main()
    exit(0 if success else 1)