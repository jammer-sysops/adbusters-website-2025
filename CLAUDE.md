# Adbusters Website 2025 - Project Documentation

## Project Overview

This is the Adbusters website for 2025, built with Astro and integrated with TinaCMS for content management. The project uses Tailwind CSS v4 for styling and is configured with TypeScript support.

## Technology Stack

- **Framework**: Astro v5.10.1
- **CMS**: TinaCMS v2.7.9
- **Styling**: Tailwind CSS v4.1.11 (using @tailwindcss/vite)
- **Language**: TypeScript
- **Build Tool**: Vite (integrated with Astro)

## Project Structure

```
/
├── content/                # Content managed by TinaCMS
│   └── posts/             # Blog posts directory
│       └── hello-world.md # Sample post
├── public/                # Static assets
│   ├── admin/            # TinaCMS admin interface
│   │   └── index.html
│   └── favicon.svg
├── src/
│   ├── assets/           # Image and media assets
│   ├── components/       # Reusable Astro components
│   ├── layouts/
│   │   └── Layout.astro  # Main layout component
│   ├── pages/
│   │   └── index.astro   # Homepage
│   └── styles/
│       └── global.css    # Global styles (imports Tailwind)
├── tina/
│   ├── __generated__/    # Auto-generated TinaCMS files
│   └── config.ts         # TinaCMS configuration
├── astro.config.mjs      # Astro configuration
├── package.json          # Project dependencies
└── tsconfig.json         # TypeScript configuration
```

## Development Workflow

### Commands

- `npm install` - Install dependencies
- `npm run dev` - Start development server with TinaCMS (runs on localhost:4321)
- `npm run build` - Build for production
- `npm run preview` - Preview production build

### Key Features

1. **Astro Framework**: Static site generation with component islands architecture
2. **TinaCMS Integration**: Git-based content management system for editing content
3. **Tailwind CSS v4**: Modern utility-first CSS framework
4. **TypeScript Support**: Full type safety with strict configuration

## TinaCMS Configuration

The CMS is configured in `tina/config.ts` with:

- **Branch Management**: Automatically detects branch from environment variables
- **Authentication**: Uses `NEXT_PUBLIC_TINA_CLIENT_ID` and `TINA_TOKEN` environment variables
- **Media Storage**: Configured to use the `public` folder
- **Content Collections**:
  - Posts: Located in `content/posts/` with title and rich-text body fields

### Environment Variables Required

- `NEXT_PUBLIC_TINA_CLIENT_ID` - TinaCMS client ID
- `TINA_TOKEN` - TinaCMS authentication token

## Content Structure

### Posts
Posts are markdown files in `content/posts/` with the following frontmatter:

```yaml
---
title: 'Post Title'
---
```

Content supports rich-text formatting through TinaCMS.

## Styling

The project uses Tailwind CSS v4 with Vite integration. Global styles are imported in `src/styles/global.css`.

## Layout Structure

The main layout (`src/layouts/Layout.astro`) provides:
- Basic HTML structure
- Meta tags for responsive design
- Page title set to "adbusters"
- Slot for page content

## Development Notes

1. The project is a basic Astro setup with minimal initial content
2. TinaCMS admin interface is available at `/admin` when running the dev server
3. The development command runs TinaCMS alongside Astro for content editing
4. TypeScript is configured with strict mode for better type safety

## Next Steps for Development

1. Expand the component library in `src/components/`
2. Create additional page templates and layouts
3. Configure additional content collections in TinaCMS
4. Implement navigation and site structure
5. Add SEO optimizations and meta tags
6. Set up deployment configuration

## Important Files

- `tina/config.ts` - Main TinaCMS configuration
- `astro.config.mjs` - Astro and Vite configuration
- `src/layouts/Layout.astro` - Main layout template
- `src/pages/index.astro` - Homepage component