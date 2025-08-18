import { defineCollection, z } from 'astro:content';

const articles = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    publishedOn: z.coerce.date().optional(),
    authorSource: z.string().optional(),
    featuredImage: z.string().optional(),
  }),
});

const spoofAds = defineCollection({
  type: 'content',
  schema: ({ image }) => z.object({
    name: z.string(),
    createdOn: z.coerce.date().optional(),
    spoofImage: image(),
    spoofCategory: z.string().optional(),
    caption: z.string().optional(),
    authorCredit: z.string().optional(),
  }),
});

const brushes = defineCollection({
  type: 'content',
  schema: z.object({
    width: z.number(),
    src: z.string(),
    topPadding: z.number(),
    bottomPadding: z.number(),
    category: z.string(),
  }),
});

export const collections = {
  articles,
  'spoof-ads': spoofAds,
  brushes,
};