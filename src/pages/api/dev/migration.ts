import type { APIRoute } from 'astro';

export const prerender = false;
import { readFile, writeFile, access } from 'node:fs/promises';
import path from 'node:path';

const WORKSPACE_ROOT = process.cwd();
const CONTENT_ROOT = path.join(WORKSPACE_ROOT, 'src', 'content', 'migration');

const corsHeaders = {
	'Access-Control-Allow-Origin': '*',
	'Access-Control-Allow-Methods': 'POST, OPTIONS',
	'Access-Control-Allow-Headers': 'Content-Type',
};

const escapeYamlString = (value: string) => value.replace(/"/g, '\\"');

const ensureMarkdownExtension = (slug: string) => {
	if (!/^[a-z0-9/-]+$/i.test(slug)) {
		throw new Error(`Slug "${slug}" contains invalid characters.`);
	}
	return `${slug}.md`;
};

const buildFrontmatter = (data: {
	title?: string;
	image?: string;
	readMoreUrl?: string;
	order: number;
	visible: boolean;
	keepInArchive: boolean;
}) => {
	const lines: string[] = [];
	if (data.title) {
		lines.push(`title: "${escapeYamlString(data.title)}"`);
	}
	if (data.image) {
		lines.push(`image: "${escapeYamlString(data.image)}"`);
	}
	if (data.readMoreUrl) {
		lines.push(`read_more_url: "${escapeYamlString(data.readMoreUrl)}"`);
	}
	lines.push(`order: ${data.order}`);
	lines.push(`visible: ${data.visible}`);
	lines.push(`keep_in_archive: ${data.keepInArchive}`);

	return `---\n${lines.join('\n')}\n---\n`;
};

type MigrationItemInput = {
	slug?: string;
	order?: number;
	visible?: boolean;
	keepInArchive?: boolean;
	title?: string;
	image?: string;
	readMoreUrl?: string;
	body?: string;
};

type MigrationPayload = {
	items: MigrationItemInput[];
};

const isRecord = (value: unknown): value is Record<string, unknown> =>
	typeof value === 'object' && value !== null;

const isMigrationItemInput = (value: unknown): value is MigrationItemInput => {
	if (!isRecord(value)) {
		return false;
	}

	if (value.slug !== undefined && typeof value.slug !== 'string') {
		return false;
	}
	if (value.order !== undefined && typeof value.order !== 'number') {
		return false;
	}
	if (value.visible !== undefined && typeof value.visible !== 'boolean') {
		return false;
	}
	if (value.keepInArchive !== undefined && typeof value.keepInArchive !== 'boolean') {
		return false;
	}
	const stringFields: Array<keyof MigrationItemInput> = ['title', 'image', 'readMoreUrl', 'body'];
	return stringFields.every((field) => value[field] === undefined || typeof value[field] === 'string');
};

const isMigrationPayload = (value: unknown): value is MigrationPayload => {
	if (!isRecord(value)) {
		return false;
	}
	const maybeItems = value.items;
	return Array.isArray(maybeItems) && maybeItems.every(isMigrationItemInput);
};

export const POST: APIRoute = async ({ request }) => {
	const method = request.method?.toUpperCase();

	if (method === 'OPTIONS') {
		return new Response(null, { status: 204, headers: corsHeaders });
	}

	if (method !== 'POST') {
		return new Response(JSON.stringify({ error: 'method-not-allowed' }), {
			status: 405,
			headers: { ...corsHeaders, 'Content-Type': 'application/json' },
		});
	}

	if (!import.meta.env.DEV) {
		return new Response('Not found', { status: 404 });
	}

	let rawBody: string;
	try {
		rawBody = await request.text();
		console.info('[migration API] method=%s length=%s', method, rawBody?.length ?? 0);
	} catch (error) {
		const message = error instanceof Error ? error.message : 'Unable to read request body.';
		return new Response(JSON.stringify({ error: 'invalid-body', message }), {
			status: 400,
			headers: { ...corsHeaders, 'Content-Type': 'application/json' },
		});
	}

	if (!rawBody) {
		return new Response(JSON.stringify({ error: 'empty-body', message: 'Request body was empty.' }), {
			status: 400,
			headers: { ...corsHeaders, 'Content-Type': 'application/json' },
		});
	}

	let payload: unknown;
	try {
		payload = JSON.parse(rawBody);
	} catch (error) {
		const message = error instanceof Error ? error.message : 'Invalid JSON payload.';
		return new Response(JSON.stringify({ error: 'invalid-json', message }), {
			status: 400,
			headers: { ...corsHeaders, 'Content-Type': 'application/json' },
		});
	}

	if (!isMigrationPayload(payload)) {
		return new Response(JSON.stringify({ error: 'missing-items', message: 'Payload must include an "items" array.' }), {
			status: 400,
			headers: { ...corsHeaders, 'Content-Type': 'application/json' },
		});
	}

	const { items } = payload;

	const updates = items.map((item) => {
		if (!item.slug) {
			throw new Error('Each item must include a slug.');
		}
		if (typeof item.order !== 'number' || Number.isNaN(item.order)) {
			throw new Error(`Item "${item.slug}" is missing a numeric order.`);
		}
		const order = Math.max(1, Math.round(item.order));
		const visible = item.visible !== false;
		const keepInArchive = item.keepInArchive !== false;
		const title = (item.title ?? '').trim();
		const image = (item.image ?? '').trim();
		const readMoreUrl = (item.readMoreUrl ?? '').trim();
		const body = (item.body ?? '').replace(/\r\n/g, '\n');

		return {
			slug: item.slug,
			order,
			visible,
			keepInArchive,
			title: title || undefined,
			image: image || undefined,
			readMoreUrl: readMoreUrl || undefined,
			body,
		};
	});

	try {
		await Promise.all(
			updates.map(async (item) => {
				const filename = ensureMarkdownExtension(item.slug);
				const fullPath = path.join(CONTENT_ROOT, filename);

				await access(fullPath).catch(() => {
					throw new Error(`File not found for slug "${item.slug}".`);
				});

				const existing = await readFile(fullPath, 'utf-8');
				const trimmedBody = item.body.trimEnd();
				const frontmatter = buildFrontmatter(item);
				const content = trimmedBody ? `${frontmatter}\n${trimmedBody}\n` : `${frontmatter}\n`;

				if (existing === content) {
					return;
				}

				await writeFile(fullPath, content, 'utf-8');
			})
		);
	} catch (error) {
		const message = error instanceof Error ? error.message : 'Failed to write content files.';
		return new Response(JSON.stringify({ error: 'write-failed', message }), {
			status: 500,
			headers: { ...corsHeaders, 'Content-Type': 'application/json' },
		});
	}

	return new Response(JSON.stringify({ success: true }), {
		status: 200,
		headers: {
			...corsHeaders,
			'Content-Type': 'application/json',
		},
	});
};
