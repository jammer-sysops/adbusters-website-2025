import type { ImageMetadata } from 'astro';

export type DividerAsset = {
  id: string;
  src: ImageMetadata;
  alt: string;
};

const dividerModules = import.meta.glob<
  ImageMetadata | { default: ImageMetadata }
>(
  '../assets/dividers/*.{png,jpg,jpeg,webp,svg}',
  { eager: true }
);

export const dividerAssets: DividerAsset[] = Object.entries(dividerModules)
  .map(([path, mod]) => {
    const metadata = 'default' in mod ? (mod.default as ImageMetadata) : (mod as ImageMetadata);
    const id = extractIdFromPath(path);
    return {
      id,
      src: metadata,
      alt: buildAltText(id),
    } satisfies DividerAsset;
  })
  .sort((a, b) => a.id.localeCompare(b.id));

function extractIdFromPath(path: string): string {
  const fileName = path.split('/').pop();
  if (!fileName) return path;
  return fileName.replace(/\.[^.]+$/, '');
}

function buildAltText(id: string): string {
  const words = id
    .split(/[-_]+/)
    .map((part) => part.trim())
    .filter(Boolean)
    .map((part) => part.charAt(0).toUpperCase() + part.slice(1));

  if (words.length === 0) return 'Decorative divider graphic';

  return `${words.join(' ')} divider graphic`;
}
