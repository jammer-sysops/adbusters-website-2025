#!/usr/bin/env python3
"""
Test conversion script - processes only 5 articles for validation.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from convert_csv_to_markdown_v2 import *

def test_conversion():
    """
    Test conversion on first 5 articles only.
    """
    output_dir = '/Users/web/adbusters-website-2025/test_articles'
    
    print("=== TEST: Converting first 5 articles ===")
    
    # Create test output directory
    os.makedirs(output_dir, exist_ok=True)
    
    # Process first 5 from Articles CSV
    articles_csv = '/Users/web/adbusters-website-2025/old-content/Adbusters New Homepage - Articles.csv'
    
    with open(articles_csv, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        
        processed_count = 0
        for row_num, row in enumerate(reader, 2):
            if processed_count >= 5:
                break
                
            try:
                # Extract fields
                title = row.get('Name', '').strip()
                if not title:
                    continue
                
                slug = row.get('Slug', create_slug(title)).strip()
                content = get_content_from_row(row)
                
                print(f"\n--- Article {processed_count + 1}: {title[:50]}...")
                print(f"  Slug: {slug}")
                print(f"  Has content: {'Yes' if content else 'No'}")
                
                # Handle dates
                published_date = convert_date(row.get('Published On', ''))
                created_date = convert_date(row.get('Created On', ''))
                
                # Handle author
                author = row.get('Author', '').strip()
                if not author:
                    author = row.get('From AB issue', '').strip()
                print(f"  Author: {author if author else 'None'}")
                
                # Featured image
                featured_image = row.get('Featured image', '').strip()
                if not featured_image:
                    featured_image = extract_featured_image(content)
                print(f"  Featured image: {'Yes' if featured_image else 'No'}")
                
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
                
                category = row.get('Catergory', '').strip()
                if category:
                    frontmatter_parts.append(f'category: {yaml_safe_string(category)}')
                
                frontmatter_parts.append('---')
                frontmatter = '\n'.join(frontmatter_parts)
                
                # Validate YAML
                is_valid, error = validate_frontmatter(frontmatter)
                print(f"  YAML valid: {is_valid}")
                if not is_valid:
                    print(f"    Error: {error}")
                    continue
                
                # Clean content
                clean_content = clean_html_content(content)
                
                # Create file
                filename = f"{slug}.md"
                filepath = os.path.join(output_dir, filename)
                
                with open(filepath, 'w', encoding='utf-8') as md_file:
                    md_file.write(frontmatter + '\n\n')
                    if clean_content:
                        md_file.write(clean_content[:500] + '...\n' if len(clean_content) > 500 else clean_content + '\n')
                
                print(f"  ✓ Written to: {filename}")
                processed_count += 1
                
            except Exception as e:
                print(f"  ✗ Error: {e}")
    
    print(f"\n=== Test complete: {processed_count} articles converted ===")
    
    # Show one sample file
    if processed_count > 0:
        sample_file = os.listdir(output_dir)[0]
        print(f"\nSample output ({sample_file}):")
        print("-" * 40)
        with open(os.path.join(output_dir, sample_file), 'r') as f:
            print(f.read()[:1000])
        print("-" * 40)

if __name__ == '__main__':
    test_conversion()