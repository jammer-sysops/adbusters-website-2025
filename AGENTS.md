# Repository Guidelines

## Project Structure & Module Organization
The Astro app lives in `src/`. `src/pages` owns route-level `.astro` entries, with `/articles` and `/spoof-ads` directories for collection-driven routes. Shared UI sits in `src/components` (React and Astro) and wrappers in `src/layouts`. Tailwind plus theme tokens live in `src/styles/global.css`; markdown content belongs in `src/content`. Static assets reside in `public/`. Build artifacts land in `dist/` and stay untracked. Legacy drafts in `old-content/` and `original-content/` are reference-only unless a ticket says otherwise.

## Build, Test, and Development Commands
Install dependencies with `npm install`. `npm run dev` launches Astro on http://localhost:4321 with hot reload. Use `npm run build` to emit the production bundle into `dist/`, and `npm run preview` to review it locally. `npm run astro check` validates frontmatter, types, and content collections; run it before commits touching data.

## Coding Style & Naming Conventions
Keep React components in `PascalCase.tsx` and Astro templates in `PascalCase.astro`. Match the surrounding indentation (tabs in `.astro`, two spaces in TypeScript, standard blocks in CSS). Favor Tailwind utility classes; extend shared styles in `src/styles/global.css` when utilities fall short. Type all props, prefer small focused components, and avoid committing generated directories already listed in `.gitignore`.

## Testing Guidelines
Automated tests are not yet wired up, so rely on build-time checks plus manual QA. Always run `npm run astro check` and `npm run build` before pushing. After layout or content updates, inspect `/`, `/articles`, and `/spoof-ads` via `npm run preview`, exercising desktop and mobile breakpoints. Note any areas left untested in the PR.

## Commit & Pull Request Guidelines
Follow the existing commit voice: concise, imperative subjects under ~70 characters (example: `tighten navbar spacing`). Group related work together and keep diffs focused. PRs must describe the change, call out impacted pages, and link to issues or relevant notes in `reports/`. Add screenshots or GIFs for visible adjustments, and list the validation commands you executed.

## Scripts & Content Automation
The `scripts/` folder houses Python utilities for content conversion and cleanup. Activate the repo `venv/` (`source venv/bin/activate`) before running them, and call with `python scripts/fix_article_dates.py`. Dry-run on staged copies in `backup_temp/` when possible, and document anomalies or follow-ups inside `reports/`.
