import type { AstroGlobal } from 'astro';
import { dividerAssets, type DividerAsset } from '../data/dividers';

type DividerClaimOptions = {
  preferredId?: string;
  instanceKey?: string;
};

type DividerDeckState = {
  seed: string;
  deck: DividerAsset[];
  cursor: number;
  claims: Map<string, DividerAsset>;
  usedIds: Set<string>;
};

type AstroLike = Pick<AstroGlobal, 'locals' | 'url'>;

type SeedInput = {
  seedKey?: string;
  url?: URL;
};

const LOCALS_KEY = 'adbusters.dividers' as const;

export type ClaimedDivider = DividerAsset & { index: number };

export function getDividerDeck(astro: AstroLike, input?: SeedInput): DividerDeckState | null {
  if (!dividerAssets.length) return null;

  const astroWithLocals = astro as unknown as {
    locals: Record<string, unknown> | undefined;
  };

  if (!astroWithLocals.locals) {
    astroWithLocals.locals = {};
  }

  const locals = astroWithLocals.locals as Record<string, unknown> & {
    [LOCALS_KEY]?: DividerDeckState;
  };
  const existing = locals[LOCALS_KEY];
  if (existing) {
    return existing;
  }

  const seedKey = input?.seedKey ?? astro.url?.pathname ?? 'default';
  const deck = shuffleWithSeed(dividerAssets, seedKey);

  const deckState: DividerDeckState = {
    seed: seedKey,
    deck,
    cursor: 0,
    claims: new Map(),
    usedIds: new Set(),
  };

  locals[LOCALS_KEY] = deckState;

  return deckState;
}

export function claimDivider(
  astro: AstroLike,
  options?: DividerClaimOptions & SeedInput
): ClaimedDivider | null {
  const deckState = getDividerDeck(astro, options);
  if (!deckState) return null;

  const { deck, claims, usedIds } = deckState;

  if (!deck.length) return null;

  const preferredId = options?.preferredId?.trim();
  const instanceKey = options?.instanceKey ?? preferredId ?? `auto-${claims.size}`;

  const existing = claims.get(instanceKey);
  if (existing) {
    return { ...existing, index: deck.indexOf(existing) };
  }

  let chosen: DividerAsset | undefined;

  if (preferredId) {
    chosen = deck.find((asset) => asset.id === preferredId);
  }

  if (!chosen) {
    chosen = nextDividerFromDeck(deckState);
  } else {
    usedIds.add(chosen.id);
  }

  if (!chosen) {
    const nextIndex = deckState.cursor % deck.length;
    chosen = deck[nextIndex];
    deckState.cursor = (deckState.cursor + 1) % deck.length;
  }

  claims.set(instanceKey, chosen);

  return { ...chosen, index: deck.indexOf(chosen) };
}

function nextDividerFromDeck(deckState: DividerDeckState): DividerAsset | undefined {
  const { deck, usedIds } = deckState;
  const total = deck.length;
  for (let attempt = 0; attempt < total; attempt += 1) {
    const index = deckState.cursor % total;
    deckState.cursor += 1;
    const candidate = deck[index];
    if (!usedIds.has(candidate.id)) {
      usedIds.add(candidate.id);
      return candidate;
    }
  }
  return undefined;
}

function shuffleWithSeed(items: DividerAsset[], seedKey: string): DividerAsset[] {
  const seed = hashStringToSeed(seedKey);
  const rng = mulberry32(seed);
  const copy = [...items];
  for (let i = copy.length - 1; i > 0; i -= 1) {
    const j = Math.floor(rng() * (i + 1));
    [copy[i], copy[j]] = [copy[j], copy[i]];
  }
  return copy;
}

function hashStringToSeed(str: string): number {
  let h1 = 0xdeadbeef;
  let h2 = 0x41c6ce57;
  for (let i = 0; i < str.length; i += 1) {
    const ch = str.charCodeAt(i);
    h1 = Math.imul(h1 ^ ch, 2654435761);
    h2 = Math.imul(h2 ^ ch, 1597334677);
  }
  h1 = Math.imul(h1 ^ (h1 >>> 16), 2246822507) ^ Math.imul(h2 ^ (h2 >>> 13), 3266489909);
  h2 = Math.imul(h2 ^ (h2 >>> 16), 2246822507) ^ Math.imul(h1 ^ (h1 >>> 13), 3266489909);
  const combined = 4294967296 * (2097151 & h2) + (h1 >>> 0);
  return combined >>> 0;
}

function mulberry32(a: number) {
  return function random(): number {
    let t = (a += 0x6d2b79f5);
    t = Math.imul(t ^ (t >>> 15), t | 1);
    t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}
