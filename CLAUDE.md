# Adbusters Website 2025 - Project Documentation

## Project Overview

This is the Adbusters website for 2025, built with Astro and React for interactive components, using native content collections for simple markdown content management. The project uses Tailwind CSS v4 for styling and is configured with TypeScript support.

## Technology Stack

- **Framework**: Astro v5.10.1 with React integration
- **UI Library**: React v19.1.1
- **Content Management**: Native Astro Content Collections (Markdown)
- **Styling**: Tailwind CSS v4.1.11 (using @tailwindcss/vite)
- **Language**: TypeScript
- **Build Tool**: Vite (integrated with Astro)

## Project Structure

```
/
├── public/                # Static assets
│   ├── images/           # Article images and media
│   │   └── articles/     # Article-specific images
│   └── favicon.svg
├── scripts/               # Python utility scripts
│   ├── convert_csv_to_markdown.py    # Convert CSV data to markdown articles
│   ├── download_images.py            # Download external images to local
│   ├── extract_image_urls.py         # Extract image URLs from content
│   ├── promote_to_featured_image.py  # Promote first images to featured
│   └── remove_duplicate_images.py    # Remove duplicate featured images
├── src/
│   ├── assets/           # Image and media assets
│   ├── components/       # React components
│   │   ├── ArticleCard.tsx   # Individual article card component (with featured images)
│   │   ├── ArticleGrid.tsx   # Grid of article cards
│   │   ├── Header.tsx        # Site header component
│   │   ├── Section.tsx       # Section wrapper component
│   │   ├── Navbar.tsx        # Navigation component
│   │   └── Footer.tsx        # Footer component
│   ├── content/          # Content collections
│   │   ├── articles/     # Article markdown files
│   │   └── config.ts     # Content collection configuration (includes featuredImage)
│   ├── layouts/
│   │   └── Layout.astro  # Main layout component
│   ├── pages/
│   │   ├── articles.astro    # Articles listing page
│   │   ├── articles/
│   │   │   └── [slug].astro  # Individual article pages (with featured images)
│   │   └── index.astro       # Homepage
│   └── styles/
│       └── global.css    # Global styles (imports Tailwind + utilities)
├── astro.config.mjs      # Astro configuration
├── package.json          # Project dependencies
└── tsconfig.json         # TypeScript configuration
```

## Development Workflow

### Commands

- `npm install` - Install dependencies
- `npm run dev` - Start development server (runs on localhost:4321)
- `npm run build` - Build for production
- `npm run preview` - Preview production build

### Key Features

1. **Astro Framework**: Static site generation with component islands architecture
2. **React Integration**: Interactive components using React with Astro's island architecture
3. **Content Collections**: Native Astro content management with markdown files
4. **Tailwind CSS v4**: Modern utility-first CSS framework
5. **TypeScript Support**: Full type safety with strict configuration

## Content Management

Content is managed through Astro's native content collections system:

- **Articles**: Located in `src/content/articles/` as markdown files
- **Configuration**: Content schema defined in `src/content/config.ts`
- **Type Safety**: Automatic TypeScript types generated from content schema

## Content Structure

### Articles
Articles are markdown files in `src/content/articles/` with the following frontmatter:

```yaml
---
title: 'Article Title'
publishedOn: 2024-11-05T00:01:07Z
authorSource: "— Author Name"
---
```

Content is written in standard markdown format with support for:
- Headers, paragraphs, and text formatting
- Links and images
- Lists and blockquotes
- Code blocks

## Styling

The project uses Tailwind CSS v4 with Vite integration. Global styles are imported in `src/styles/global.css`.

## Layout Structure

The main layout (`src/layouts/Layout.astro`) provides:
- Basic HTML structure
- Meta tags for responsive design
- Page title set to "adbusters"
- Slot for page content

## Development Notes

1. Content is now managed through simple markdown files in `src/content/articles/`
2. No CMS admin interface - content is edited directly in markdown files
3. TypeScript is configured with strict mode for better type safety
4. Content collections provide automatic type generation and validation

## Adding New Articles

To add a new article:

1. Create a new `.md` file in `src/content/articles/`
2. Add frontmatter with required fields: `title`, `publishedOn` (optional), `authorSource` (optional)
3. Write content in standard markdown format
4. The article will automatically appear in the articles listing

## Next Steps for Development

1. Expand the component library in `src/components/`
2. Create additional page templates and layouts
3. Configure additional content collections if needed
4. Implement navigation and site structure
5. Add SEO optimizations and meta tags
6. Set up deployment configuration

## React Components

The project includes several reusable React components:

- **ArticleCard.tsx**: Displays individual article information with title, date, and optional excerpt
- **ArticleGrid.tsx**: Grid layout for displaying multiple articles with optional excerpts
- **Header.tsx**: Site header with title, subtitle, and optional navigation
- **Section.tsx**: Reusable section wrapper with title and optional "view all" link
- **Navbar.tsx**: Complex navigation component with punk aesthetic, mobile menu, and handdrawn border styling
- **Footer.tsx**: Clean footer component with search, links, social media icons, and textured background

Components are used in Astro pages with the `client:load` directive for hydration.

## Utility Scripts

The `scripts/` directory contains Python utilities for content management:

### Image Management Scripts
- **`download_images.py`**: Downloads external images from URLs in markdown files and converts them to local paths. Handles both featured images and inline images.
- **`remove_duplicate_images.py`**: Removes duplicate inline images that exactly match the featured image in articles.
- **`promote_to_featured_image.py`**: Promotes the first inline image to featured image when no featured image exists.

### Content Processing Scripts  
- **`convert_csv_to_markdown.py`**: Converts CSV data to markdown article files (used for initial content migration).
- **`extract_image_urls.py`**: Extracts and analyzes image URLs from content files.

### Usage Examples
```bash
# Download all external images and convert to local
python3 scripts/download_images.py

# Remove duplicate images that match featured images
python3 scripts/remove_duplicate_images.py

# Promote first images to featured images where missing
python3 scripts/promote_to_featured_image.py
```

## Important Files

- `src/content/config.ts` - Content collections configuration (includes featuredImage schema)
- `astro.config.mjs` - Astro and Vite configuration with React integration
- `src/layouts/Layout.astro` - Main layout template
- `src/pages/index.astro` - Homepage using React components
- `src/pages/articles.astro` - Articles listing page using React components
- `src/pages/articles/[slug].astro` - Individual article template with featured image support
- `src/components/` - Directory containing React components