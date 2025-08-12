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

export const collections = {
  articles,
};