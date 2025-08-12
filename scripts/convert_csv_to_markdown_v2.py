#!/usr/bin/env python3
"""
Improved CSV to Markdown converter with YAML validation and proper content handling.
Addresses the issues from the previous botched conversion attempt.
"""

import csv
import os
import re
import yaml
import unicodedata
from datetime import datetime

def yaml_safe_string(value):
    """
    Make a string safe for YAML frontmatter by escaping problematic characters.
    """
    if not value:
        return '""'
    
    # Remove control characters and normalize unicode
    value = ''.join(char for char in value if not unicodedata.category(char).startswith('C'))
    value = unicodedata.normalize('NFKC', value)
    
    # Escape quotes and problematic characters
    value = value.replace('"', '\\"')
    value = value.replace('\n', ' ')  # Convert newlines to spaces
    value = value.replace('\r', ' ')
    
    # Remove problematic markdown chars that could break YAML
    value = re.sub(r'[*`\[\]{}]', '', value)
    
    # Trim and wrap in quotes
    value = value.strip()
    return f'"{value}"' if value else '""'

def validate_frontmatter(frontmatter_text):
    """
    Validate that the frontmatter is valid YAML.
    """
    try:
        # Remove the closing --- for validation
        yaml_content = frontmatter_text.replace('---\n', '', 1)  # Remove opening
        if yaml_content.endswith('---'):
            yaml_content = yaml_content[:-3].rstrip()  # Remove closing
        
        yaml.safe_load(yaml_content)
        return True, None
    except yaml.YAMLError as e:
        return False, str(e)

def create_slug(title):
    """
    Create a URL-safe slug from title.
    """
    # Remove HTML tags if any
    title = re.sub(r'<[^>]+>', '', title)
    # Convert to lowercase and replace spaces/special chars with hyphens
    slug = re.sub(r'[^\w\s-]', '', title.lower())
    slug = re.sub(r'[-\s]+', '-', slug)
    return slug.strip('-')

def get_content_from_row(row):
    """
    Extract content from row, checking multiple possible content fields.
    """
    content_fields = [
        'Article content (Rich text)',
        'Part 1',  # For Full Articles
        'Article blurb',
        'Short Article Preview'
    ]
    
    for field in content_fields:
        content = row.get(field, '').strip()
        if content:
            return content
    
    return ''

def extract_featured_image(content):
    """
    Extract the first image URL from content to use as featured image.
    """
    # Look for img src attributes
    img_match = re.search(r'<img[^>]+src=["\']([^"\']+)["\']', content)
    if img_match:
        return img_match.group(1)
    return None

def clean_html_content(content):
    """
    Clean up HTML content for markdown, preserving images and basic formatting.
    """
    if not content:
        return ''
    
    # Convert basic HTML tags to markdown
    content = re.sub(r'<p[^>]*>', '', content)
    content = re.sub(r'</p>', '\n\n', content)
    content = re.sub(r'<br[^>]*/?>', '\n', content)
    content = re.sub(r'<h(\d)[^>]*>', r'\n## ', content)
    content = re.sub(r'</h\d>', '\n\n', content)
    content = re.sub(r'<strong[^>]*>', '**', content)
    content = re.sub(r'</strong>', '**', content)
    content = re.sub(r'<em[^>]*>', '*', content)
    content = re.sub(r'</em>', '*', content)
    
    # Handle images - convert to markdown format
    content = re.sub(r'<figure[^>]*>.*?<img[^>]+src=["\']([^"\']+)["\'][^>]*>.*?</figure>', r'![Image](\1)', content, flags=re.DOTALL)
    content = re.sub(r'<img[^>]+src=["\']([^"\']+)["\'][^>]*>', r'![Image](\1)', content)
    
    # Handle links
    content = re.sub(r'<a[^>]+href=["\']([^"\']+)["\'][^>]*>(.*?)</a>', r'[\2](\1)', content)
    
    # Remove remaining HTML tags
    content = re.sub(r'<[^>]+>', '', content)
    
    # Clean up whitespace
    content = re.sub(r'\n\s*\n\s*\n', '\n\n', content)
    content = content.strip()
    
    return content

def convert_date(date_str):
    """
    Convert date string to ISO format.
    """
    if not date_str:
        return None
    
    try:
        # Parse various date formats
        if 'GMT' in date_str:
            # Handle format like "Tue Nov 05 2024 00:01:07 GMT+0000 (Coordinated Universal Time)"
            clean_date = re.sub(r'\s*GMT.*$', '', date_str)
            clean_date = re.sub(r'^[A-Za-z]+\s+', '', clean_date)  # Remove day of week
            dt = datetime.strptime(clean_date, '%b %d %Y %H:%M:%S')
        else:
            # Try other common formats
            dt = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
        
        return dt.strftime('%Y-%m-%d')
    except (ValueError, AttributeError):
        return None

def process_articles_csv(csv_path, output_dir):
    """
    Process the Articles CSV file.
    """
    print(f"Processing Articles CSV: {csv_path}")
    
    with open(csv_path, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        
        processed_count = 0
        error_count = 0
        
        for row_num, row in enumerate(reader, 2):  # Start at 2 since header is row 1
            try:
                # Extract basic fields
                title = row.get('Name', '').strip()
                if not title:
                    print(f"Row {row_num}: Skipping - no title")
                    continue
                
                slug = row.get('Slug', create_slug(title)).strip()
                content = get_content_from_row(row)
                
                # Handle dates
                published_date = convert_date(row.get('Published On', ''))
                created_date = convert_date(row.get('Created On', ''))
                
                # Handle author - single field, no duplicates
                author = row.get('Author', '').strip()
                if not author:
                    author = row.get('From AB issue', '').strip()
                
                # Extract featured image from content or use provided one
                featured_image = row.get('Featured image', '').strip()
                if not featured_image:
                    featured_image = extract_featured_image(content)
                
                # Build frontmatter
                frontmatter_parts = [
                    '---',
                    f'title: {yaml_safe_string(title)}',
                ]
                
                if published_date:
                    frontmatter_parts.append(f'publishedOn: {published_date}')
                elif created_date:
                    frontmatter_parts.append(f'publishedOn: {created_date}')
                
                if author:
                    frontmatter_parts.append(f'author: {yaml_safe_string(author)}')
                
                if featured_image:
                    frontmatter_parts.append(f'featuredImage: {yaml_safe_string(featured_image)}')
                
                # Add category if available
                category = row.get('Catergory', '').strip()  # Note the typo in original CSV
                if category:
                    frontmatter_parts.append(f'category: {yaml_safe_string(category)}')
                
                frontmatter_parts.append('---')
                frontmatter = '\n'.join(frontmatter_parts)
                
                # Validate YAML
                is_valid, error = validate_frontmatter(frontmatter)
                if not is_valid:
                    print(f"Row {row_num}: YAML validation failed - {error}")
                    error_count += 1
                    continue
                
                # Clean content
                clean_content = clean_html_content(content)
                
                # Create markdown file
                filename = f"{slug}.md"
                filepath = os.path.join(output_dir, filename)
                
                with open(filepath, 'w', encoding='utf-8') as md_file:
                    md_file.write(frontmatter + '\n\n')
                    if clean_content:
                        md_file.write(clean_content + '\n')
                
                processed_count += 1
                if processed_count % 10 == 0:
                    print(f"Processed {processed_count} articles...")
                    
            except Exception as e:
                print(f"Row {row_num}: Error processing - {e}")
                error_count += 1
        
        print(f"Articles CSV: {processed_count} processed, {error_count} errors")
        return processed_count, error_count

def process_full_articles_csv(csv_path, output_dir):
    """
    Process the Full Articles CSV file.
    """
    print(f"Processing Full Articles CSV: {csv_path}")
    
    with open(csv_path, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        
        processed_count = 0
        error_count = 0
        
        for row_num, row in enumerate(reader, 2):
            try:
                # Extract basic fields
                title = row.get('Name', '').strip()
                if not title:
                    print(f"Row {row_num}: Skipping - no title")
                    continue
                
                slug = row.get('Slug', create_slug(title)).strip()
                content = get_content_from_row(row)
                
                # Handle dates
                published_date = convert_date(row.get('Published On', ''))
                created_date = convert_date(row.get('Created On', ''))
                
                # Handle author - check both possible fields
                author = row.get('Author', '').strip()
                if not author:
                    author = row.get('Author / Source', '').strip()
                
                # Featured image
                featured_image = row.get('Top image', '').strip()
                if not featured_image:
                    featured_image = extract_featured_image(content)
                
                # Build frontmatter
                frontmatter_parts = [
                    '---',
                    f'title: {yaml_safe_string(title)}',
                ]
                
                if published_date:
                    frontmatter_parts.append(f'publishedOn: {published_date}')
                elif created_date:
                    frontmatter_parts.append(f'publishedOn: {created_date}')
                
                if author:
                    frontmatter_parts.append(f'author: {yaml_safe_string(author)}')
                
                if featured_image:
                    frontmatter_parts.append(f'featuredImage: {yaml_safe_string(featured_image)}')
                
                frontmatter_parts.append('---')
                frontmatter = '\n'.join(frontmatter_parts)
                
                # Validate YAML
                is_valid, error = validate_frontmatter(frontmatter)
                if not is_valid:
                    print(f"Row {row_num}: YAML validation failed - {error}")
                    error_count += 1
                    continue
                
                # Clean content
                clean_content = clean_html_content(content)
                
                # Create markdown file
                filename = f"{slug}.md"
                filepath = os.path.join(output_dir, filename)
                
                # Don't overwrite if exists (Articles CSV takes precedence)
                if os.path.exists(filepath):
                    print(f"Row {row_num}: Skipping {filename} - already exists")
                    continue
                
                with open(filepath, 'w', encoding='utf-8') as md_file:
                    md_file.write(frontmatter + '\n\n')
                    if clean_content:
                        md_file.write(clean_content + '\n')
                
                processed_count += 1
                if processed_count % 10 == 0:
                    print(f"Processed {processed_count} full articles...")
                    
            except Exception as e:
                print(f"Row {row_num}: Error processing - {e}")
                error_count += 1
        
        print(f"Full Articles CSV: {processed_count} processed, {error_count} errors")
        return processed_count, error_count

def main():
    """
    Main conversion function with validation and error handling.
    """
    # Clear existing articles
    output_dir = '/Users/web/adbusters-website-2025/src/content/articles'
    
    print("=== CSV to Markdown Conversion v2 ===")
    print("Starting fresh conversion with YAML validation...")
    
    # Clear existing articles
    if os.path.exists(output_dir):
        for file in os.listdir(output_dir):
            if file.endswith('.md'):
                os.remove(os.path.join(output_dir, file))
    else:
        os.makedirs(output_dir, exist_ok=True)
    
    # Process both CSV files
    articles_csv = '/Users/web/adbusters-website-2025/old-content/Adbusters New Homepage - Articles.csv'
    full_articles_csv = '/Users/web/adbusters-website-2025/old-content/Adbusters New Homepage - Full Articles.csv'
    
    total_processed = 0
    total_errors = 0
    
    # Process Articles CSV first (main content)
    if os.path.exists(articles_csv):
        processed, errors = process_articles_csv(articles_csv, output_dir)
        total_processed += processed
        total_errors += errors
    else:
        print(f"Articles CSV not found: {articles_csv}")
    
    # Process Full Articles CSV (additional content)
    if os.path.exists(full_articles_csv):
        processed, errors = process_full_articles_csv(full_articles_csv, output_dir)
        total_processed += processed
        total_errors += errors
    else:
        print(f"Full Articles CSV not found: {full_articles_csv}")
    
    print("\n=== Conversion Complete ===")
    print(f"Total processed: {total_processed}")
    print(f"Total errors: {total_errors}")
    
    if total_errors > 0:
        print(f"\n⚠️  {total_errors} errors occurred. Check output above for details.")
        return False
    else:
        print("✅ All articles converted successfully!")
        return True

if __name__ == '__main__':
    success = main()
    exit(0 if success else 1)