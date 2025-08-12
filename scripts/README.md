# Content Management Scripts

This directory contains Python utilities for managing content and images in the Adbusters website.

## Prerequisites

- Python 3.6+
- All scripts should be run from the project root directory

## Scripts Overview

### Image Management

#### `download_images.py`
Downloads external images from markdown files and converts them to local paths.

**Features:**
- Downloads images from external URLs (uploads-ssl.webflow.com, cdn.prod.website-files.com, etc.)
- Converts both featured images and inline images
- Handles duplicate filenames automatically
- Updates markdown files with local image paths
- Respectful downloading with delays between requests

**Usage:**
```bash
python3 scripts/download_images.py
```

#### `remove_duplicate_images.py`
Removes duplicate inline images that exactly match the featured image.

**Features:**
- Finds articles where the first inline image matches the featured image
- Removes only the duplicate inline image, preserving the featured image
- Cleans up extra whitespace left behind

**Usage:**
```bash
python3 scripts/remove_duplicate_images.py
```

#### `promote_to_featured_image.py`
Promotes the first inline image to featured image when no featured image exists.

**Features:**
- Finds articles with no featured image but has a first inline image
- Adds the image as featuredImage in frontmatter
- Removes the duplicate inline image from content
- Only processes images at the very start of article content

**Usage:**
```bash
python3 scripts/promote_to_featured_image.py
```

### Content Processing

#### `convert_csv_to_markdown.py`
Converts CSV data to markdown article files (used for initial content migration).

**Usage:**
```bash
python3 scripts/convert_csv_to_markdown.py
```

#### `extract_image_urls.py`
Extracts and analyzes image URLs from content files.

**Usage:**
```bash
python3 scripts/extract_image_urls.py
```

## Typical Workflow

When setting up content with external images:

1. **Download external images:**
   ```bash
   python3 scripts/download_images.py
   ```

2. **Remove duplicates:**
   ```bash
   python3 scripts/remove_duplicate_images.py
   ```

3. **Promote first images to featured:**
   ```bash
   python3 scripts/promote_to_featured_image.py
   ```

This workflow ensures all images are local, properly organized, and displayed correctly in the website components.

## File Paths

All scripts are configured to work with the Astro project structure:
- **Content directory:** `src/content/articles/`
- **Images directory:** `public/images/articles/`
- **Web path:** `/images/articles/`

## Notes

- Scripts include error handling and progress reporting
- All scripts preserve existing content and only make necessary changes
- Always run scripts from the project root directory
- Scripts are safe to run multiple times (idempotent)