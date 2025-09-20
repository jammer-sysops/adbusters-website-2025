import { useEffect, useMemo, useState } from 'react';
import type { DragEvent } from 'react';

type MigrationItem = {
	id: string;
	slug: string;
	displaySlug: string;
	title?: string;
	image?: string;
	readMoreUrl?: string;
	body: string;
	excerpt: string;
	order?: number;
	visible: boolean;
	keepInArchive: boolean;
};

type DashboardItem = {
	id: string;
	slug: string;
	displaySlug: string;
	order: number;
	visible: boolean;
	keepInArchive: boolean;
	expanded: boolean;
	title?: string;
	image?: string;
	readMoreUrl?: string;
	draft: {
		title: string;
		image: string;
		readMoreUrl: string;
		body: string;
	};
	excerpt: string;
};

type Props = {
	items: MigrationItem[];
};

const excerptFromMarkdown = (markdown: string) => {
	if (!markdown) return '';
	const withoutCode = markdown.replace(/```[\s\S]*?```/g, ' ');
	const withoutImages = withoutCode.replace(/!\[[^\]]*\]\([^)]*\)/g, ' ');
	const withoutLinks = withoutImages.replace(/\[([^\]]*)\]\([^)]*\)/g, '$1');
	const withoutHtml = withoutLinks.replace(/<[^>]+>/g, ' ');
	const withoutMarkup = withoutHtml.replace(/[-#*_>`~]/g, ' ');
	const collapsed = withoutMarkup.replace(/\s+/g, ' ').trim();
	if (!collapsed) return '';
	const preview = collapsed.slice(0, 160).trim();
	return collapsed.length > 160 ? `${preview}…` : preview;
};

const resequence = (list: DashboardItem[]) =>
	list.map((entry, index) => ({ ...entry, order: index + 1 }));

const MigrationDashboard = ({ items }: Props) => {
	const initialState = useMemo<DashboardItem[]>(
		() =>
			resequence(
				items.map((item, index) => ({
					id: item.id,
					slug: item.slug,
					displaySlug: item.displaySlug,
					order: item.order ?? index + 1,
					visible: item.visible,
					keepInArchive: item.keepInArchive,
					expanded: false,
					title: item.title,
					image: item.image,
					readMoreUrl: item.readMoreUrl,
					draft: {
						title: item.title ?? '',
						image: item.image ?? '',
						readMoreUrl: item.readMoreUrl ?? '',
						body: item.body ?? '',
					},
					excerpt: item.excerpt,
				}))
			),
		[items]
	);

	const [entries, setEntries] = useState<DashboardItem[]>(initialState);
	const [draggedIndex, setDraggedIndex] = useState<number | null>(null);
	const [dirty, setDirty] = useState(false);
	const [saving, setSaving] = useState(false);
	const [status, setStatus] = useState<{ type: 'idle' | 'success' | 'error'; message: string | null }>(
		{ type: 'idle', message: null }
	);

	useEffect(() => {
		setEntries(initialState);
		setDirty(false);
		setStatus({ type: 'idle', message: null });
	}, [initialState]);

	const markDirty = () => {
		setDirty(true);
		setStatus({ type: 'idle', message: null });
	};

	const handleToggleExpand = (index: number) => {
		setEntries((prev) =>
			prev.map((entry, i) =>
				i === index ? { ...entry, expanded: !entry.expanded } : entry
			)
		);
	};

	const handleToggleVisible = (index: number) => {
		setEntries((prev) =>
			prev.map((entry, i) =>
				i === index ? { ...entry, visible: !entry.visible } : entry
			)
		);
		markDirty();
	};

	const handleToggleArchive = (index: number) => {
		setEntries((prev) =>
			prev.map((entry, i) =>
				i === index
					? { ...entry, keepInArchive: !entry.keepInArchive }
					: entry
			)
		);
		markDirty();
	};

	const handleDraftChange = (
		index: number,
		key: keyof DashboardItem['draft'],
		value: string
	) => {
		setEntries((prev) =>
			prev.map((entry, i) =>
				i === index
					? { ...entry, draft: { ...entry.draft, [key]: value } }
					: entry
			)
		);
		markDirty();
	};

	const handleDragStart = (event: DragEvent<HTMLDivElement>, index: number) => {
		setDraggedIndex(index);
		event.dataTransfer.effectAllowed = 'move';
		event.dataTransfer.setData('text/plain', String(index));
	};

	const handleDragOver = (event: DragEvent<HTMLDivElement>) => {
		event.preventDefault();
		event.dataTransfer.dropEffect = 'move';
	};

	const handleDrop = (event: DragEvent<HTMLDivElement>, index: number) => {
		event.preventDefault();
		const fromData = event.dataTransfer.getData('text/plain');
		const fromIndex = draggedIndex ?? (fromData ? parseInt(fromData, 10) : NaN);
		if (Number.isNaN(fromIndex) || fromIndex === index) {
			setDraggedIndex(null);
			return;
		}
		setEntries((prev) => {
			const clone = [...prev];
			const [moved] = clone.splice(fromIndex, 1);
			clone.splice(index, 0, moved);
			return resequence(clone);
		});
		setDraggedIndex(null);
		markDirty();
	};

	const handleDragEnd = () => {
		setDraggedIndex(null);
	};

	const handleCollapseAll = () => {
		setEntries((prev) => prev.map((entry) => ({ ...entry, expanded: false })));
	};

	const handleReset = () => {
		setEntries(initialState);
		setDirty(false);
		setStatus({ type: 'idle', message: null });
	};

	const handleSave = async () => {
		setSaving(true);
		setStatus({ type: 'idle', message: null });
		try {
			const payload = {
				items: entries.map((entry, index) => ({
					slug: entry.displaySlug,
					order: index + 1,
					visible: entry.visible,
					keepInArchive: entry.keepInArchive,
					title: entry.draft.title.trim(),
					image: entry.draft.image.trim(),
					readMoreUrl: entry.draft.readMoreUrl.trim(),
					body: entry.draft.body.replace(/\r\n/g, '\n'),
				})),
			};

			const response = await fetch('/api/dev/migration', {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json',
				},
				body: JSON.stringify(payload),
			});

			if (!response.ok) {
				const errorText = await response.text();
				throw new Error(errorText || 'Failed to update migration files.');
			}

			await response.json();

			setEntries((prev) =>
				prev.map((entry, index) => {
					const trimmedTitle = entry.draft.title.trim();
					const trimmedImage = entry.draft.image.trim();
					const trimmedReadMore = entry.draft.readMoreUrl.trim();
					const body = entry.draft.body.replace(/\r\n/g, '\n');
					return {
						...entry,
						order: index + 1,
						title: trimmedTitle || undefined,
						image: trimmedImage || undefined,
						readMoreUrl: trimmedReadMore || undefined,
						excerpt: excerptFromMarkdown(body) || entry.excerpt,
						draft: {
							title: trimmedTitle,
							image: trimmedImage,
							readMoreUrl: trimmedReadMore,
							body,
						},
					};
				})
			);

			setDirty(false);
			setStatus({ type: 'success', message: 'Saved changes to markdown files.' });
		} catch (error) {
			const message = error instanceof Error ? error.message : 'Unknown error.';
			setStatus({ type: 'error', message });
		} finally {
			setSaving(false);
		}
	};

	return (
		<section className="space-y-8">
			<header className="rounded-lg border border-dashed border-slate-300 bg-slate-50 p-6">
				<div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
					<div>
						<h1 className="text-2xl font-semibold text-slate-900">Homepage Migration Dashboard</h1>
						<p className="mt-2 max-w-2xl text-sm text-slate-600">
							Preview, reorder, and edit the homepage migration blocks. Saving will overwrite the corresponding markdown files under
							{' '}
							<code className="rounded bg-slate-200 px-1.5 py-0.5 text-xs text-slate-700">src/content/migration/homepage</code>.
						</p>
					</div>
					<div className="flex flex-wrap items-center gap-2">
						<button
							type="button"
							onClick={handleReset}
							disabled={!dirty || saving}
							className={`rounded-md border px-4 py-2 text-sm font-medium transition ${
								dirty && !saving
									? 'border-slate-300 bg-white text-slate-700 hover:border-slate-400 hover:text-slate-900'
									: 'cursor-not-allowed border-slate-200 bg-slate-100 text-slate-400'
							}`}
						>
							Reset
						</button>
						<button
							type="button"
							onClick={handleSave}
							disabled={!dirty || saving}
							className={`rounded-md px-4 py-2 text-sm font-semibold text-white transition ${
								dirty && !saving
									? 'bg-blue-600 hover:bg-blue-700'
									: 'cursor-not-allowed bg-blue-300'
							}`}
						>
							{saving ? 'Saving…' : 'Save changes'}
						</button>
					</div>
				</div>
				<div className="mt-4 flex flex-wrap gap-2 text-xs text-slate-500">
					<span className="inline-flex items-center gap-1 rounded-full bg-slate-200 px-3 py-1">
						<span className="h-2 w-2 rounded-full bg-emerald-500" aria-hidden />
						Drag cards to adjust order
					</span>
					<span className="inline-flex items-center gap-1 rounded-full bg-slate-200 px-3 py-1">
						<span className="h-2 w-2 rounded-full bg-blue-500" aria-hidden />
						Toggle visibility &amp; archive flags
					</span>
					<button
						type="button"
						onClick={handleCollapseAll}
						className="inline-flex items-center rounded-md border border-slate-300 px-3 py-1 font-medium text-slate-700 transition hover:border-slate-400 hover:text-slate-900"
					>
						Collapse all
					</button>
					{status.type !== 'idle' && status.message ? (
						<span
							className={`inline-flex items-center gap-1 rounded-md px-3 py-1 text-xs font-medium ${
								status.type === 'success'
									? 'bg-emerald-100 text-emerald-700'
									: 'bg-rose-100 text-rose-700'
							}`}
						>
							{status.message}
						</span>
					) : null}
				</div>
			</header>

			<div className="space-y-4">
				{entries.map((entry, index) => {
					const displayTitle = entry.draft.title.trim() || entry.title || entry.slug;
					const bodyExcerpt = excerptFromMarkdown(entry.draft.body) || entry.excerpt;
					return (
						<div
							key={entry.slug}
							className={`group rounded-lg border bg-white shadow-sm transition ${
								entry.expanded ? 'border-blue-400 shadow-md' : 'border-slate-200 hover:border-blue-300'
							} ${draggedIndex === index ? 'opacity-70' : ''}`}
							draggable={!entry.expanded}
							onDragStart={(event) => handleDragStart(event, index)}
							onDragOver={handleDragOver}
							onDrop={(event) => handleDrop(event, index)}
							onDragEnd={handleDragEnd}
						>
							<div
								className="flex items-start justify-between gap-4 p-4"
								onClick={() => handleToggleExpand(index)}
								role="button"
								tabIndex={0}
								onKeyDown={(event) => {
									if (event.key === 'Enter' || event.key === ' ') {
										event.preventDefault();
										handleToggleExpand(index);
									}
								}}
							>
								<div className="flex flex-1 items-start gap-4">
					<div className="flex h-10 w-10 items-center justify-center rounded-md bg-slate-100 text-sm font-semibold text-slate-600">
						#{entry.order}
					</div>
					{entry.image ? (
										<img
											src={entry.image}
											alt="Preview"
											className="hidden h-16 w-16 flex-shrink-0 rounded-md object-cover sm:block"
											loading="lazy"
										/>
									) : null}
					<div className="flex-1">
						<div className="flex flex-wrap items-center gap-3">
							<h2 className="text-lg font-semibold text-slate-900">{displayTitle}</h2>
							<span className="rounded-full bg-slate-100 px-2 py-0.5 text-[11px] font-medium uppercase tracking-wide text-slate-500">
								{entry.displaySlug}
							</span>
						</div>
										<p className="mt-1 line-clamp-2 text-sm text-slate-600">
											{bodyExcerpt || 'No body content detected. Click to add copy.'}
										</p>
									</div>
								</div>
								<div className="flex items-center gap-2">
									<button
										type="button"
										onClick={(event) => {
											event.stopPropagation();
											handleToggleVisible(index);
										}}
										className={`rounded-md border px-3 py-1 text-xs font-semibold transition ${
											entry.visible
												? 'border-emerald-400 bg-emerald-50 text-emerald-700 hover:bg-emerald-100'
												: 'border-slate-300 bg-white text-slate-600 hover:bg-slate-100'
										}`}
									>
										{entry.visible ? 'Visible' : 'Hidden'}
									</button>
									<button
										type="button"
										onClick={(event) => {
											event.stopPropagation();
											handleToggleArchive(index);
										}}
										className={`rounded-md border px-3 py-1 text-xs font-semibold transition ${
											entry.keepInArchive
												? 'border-blue-400 bg-blue-50 text-blue-700 hover:bg-blue-100'
												: 'border-slate-300 bg-white text-slate-600 hover:bg-slate-100'
										}`}
									>
										{entry.keepInArchive ? 'Archive ✓' : 'Archive ✗'}
									</button>
								</div>
							</div>

							{entry.expanded ? (
								<div className="border-t border-slate-200 bg-slate-50 p-4">
									<div className="grid gap-4 sm:grid-cols-2">
										<label className="flex flex-col text-sm font-medium text-slate-700">
											<span>Title</span>
											<input
												type="text"
												value={entry.draft.title}
												onChange={(event) => handleDraftChange(index, 'title', event.target.value)}
												className="mt-1 rounded-md border border-slate-300 bg-white px-3 py-2 text-sm text-slate-900 shadow-sm focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-200"
											/>
										</label>
										<label className="flex flex-col text-sm font-medium text-slate-700">
											<span>Hero image URL</span>
											<input
												type="url"
												value={entry.draft.image}
												onChange={(event) => handleDraftChange(index, 'image', event.target.value)}
												className="mt-1 rounded-md border border-slate-300 bg-white px-3 py-2 text-sm text-slate-900 shadow-sm focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-200"
											/>
										</label>
										<label className="flex flex-col text-sm font-medium text-slate-700 sm:col-span-2">
											<span>Read more URL</span>
											<input
												type="url"
												value={entry.draft.readMoreUrl}
												onChange={(event) => handleDraftChange(index, 'readMoreUrl', event.target.value)}
												className="mt-1 rounded-md border border-slate-300 bg-white px-3 py-2 text-sm text-slate-900 shadow-sm focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-200"
											/>
										</label>
									</div>
									<label className="mt-4 block text-sm font-medium text-slate-700">
										<span>Markdown body</span>
										<textarea
											value={entry.draft.body}
											onChange={(event) => handleDraftChange(index, 'body', event.target.value)}
											rows={Math.min(Math.max(Math.ceil(entry.draft.body.length / 120), 6), 20)}
											className="mt-1 w-full rounded-md border border-slate-300 bg-white px-3 py-2 text-sm text-slate-900 shadow-sm focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-200"
										/>
									</label>
								</div>
							) : null}
						</div>
					);
				})}
			</div>
		</section>
	);
};

export default MigrationDashboard;
