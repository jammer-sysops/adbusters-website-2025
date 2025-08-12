#!/usr/bin/env python3
"""
Script to clean up HTML entities in markdown files.
Replaces common HTML entities with their proper characters.
"""

import os
import re
import html
from pathlib import Path

def cleanup_html_entities(content):
    """Clean up HTML entities in markdown content."""
    # First, use Python's html.unescape for standard entities
    content = html.unescape(content)
    
    # Handle some specific cases that might not be caught
    replacements = {
        '&nbsp;': ' ',
        '&amp;': '&',
        '&lt;': '<',
        '&gt;': '>',
        '&quot;': '"',
        '&#39;': "'",
        '&#8217;': "'",  # right single quotation mark
        '&#8216;': "'",  # left single quotation mark
        '&#8220;': '"',  # left double quotation mark
        '&#8221;': '"',  # right double quotation mark
        '&#8211;': '–',  # en dash
        '&#8212;': '—',  # em dash
        '&#8230;': '…',  # horizontal ellipsis
    }
    
    for entity, replacement in replacements.items():
        content = content.replace(entity, replacement)
    
    # Clean up any remaining numeric entities
    content = re.sub(r'&#\d+;', '', content)
    
    # Clean up any remaining named entities that weren't caught
    content = re.sub(r'&[a-zA-Z][a-zA-Z0-9]*;', '', content)
    
    # Clean up extra whitespace that might result from removals
    content = re.sub(r'\n\s*\n\s*\n', '\n\n', content)  # Reduce multiple empty lines
    content = re.sub(r'[ \t]+', ' ', content)  # Normalize spaces and tabs
    
    return content

def process_markdown_file(file_path):
    """Process a single markdown file to clean up HTML entities."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            original_content = f.read()
        
        cleaned_content = cleanup_html_entities(original_content)
        
        # Only write if content actually changed
        if original_content != cleaned_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(cleaned_content)
            print(f"✓ Cleaned: {file_path}")
            return True
        else:
            print(f"- No changes: {file_path}")
            return False
    except Exception as e:
        print(f"✗ Error processing {file_path}: {e}")
        return False

def main():
    """Main function to process all markdown files."""
    articles_dir = Path("src/content/articles")
    
    if not articles_dir.exists():
        print(f"Error: Articles directory not found: {articles_dir}")
        return
    
    markdown_files = list(articles_dir.glob("*.md"))
    
    if not markdown_files:
        print("No markdown files found in the articles directory.")
        return
    
    print(f"Found {len(markdown_files)} markdown files to process...\n")
    
    files_modified = 0
    for file_path in sorted(markdown_files):
        if process_markdown_file(file_path):
            files_modified += 1
    
    print(f"\n✓ Completed! Modified {files_modified} out of {len(markdown_files)} files.")

if __name__ == "__main__":
    main()