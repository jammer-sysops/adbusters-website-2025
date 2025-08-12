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

export const collections = {
  articles,
  'spoof-ads': spoofAds,
};