#!/usr/bin/env python3

import os
import random

def create_brush_markdown_files():
    brushes_dir = 'src/content/brushes'
    os.makedirs(brushes_dir, exist_ok=True)
    
    # Define possible categories
    categories = ['separator', 'header', 'footer', 'accent', 'transition']
    
    # Create markdown files for each brush (1-28)
    for i in range(1, 29):
        filename = f"brush-{i}.md"
        filepath = os.path.join(brushes_dir, filename)
        
        # Generate some varied but reasonable values
        width = random.choice([300, 400, 500, 600, 700, 800, 900, 1000])
        top_padding = random.choice([8, 12, 16, 20, 24, 32])
        bottom_padding = random.choice([8, 12, 16, 20, 24, 32])
        category = random.choice(categories)
        src = f"/images/brushes-separators/brush-{i}.png"
        
        content = f"""---
width: {width}
src: "{src}"
topPadding: {top_padding}
bottomPadding: {bottom_padding}
category: "{category}"
---

# Brush {i}

A handdrawn brush stroke separator for the Adbusters website.
"""
        
        with open(filepath, 'w') as f:
            f.write(content)
        
        print(f"Created {filename}")
    
    print(f"\nCreated {28} brush markdown files in {brushes_dir}")

if __name__ == "__main__":
    create_brush_markdown_files()