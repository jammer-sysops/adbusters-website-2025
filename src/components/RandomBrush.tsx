import { useState, useEffect, useRef } from 'react';
import { Img } from 'react-image';

// Global state to track used brushes across all instances
const globalUsedBrushes = new Set<string>();
let globalBrushPool: BrushData[] = [];

interface BrushData {
  id: string;
  data: {
    width: number;
    src: string;
    topPadding: number;
    bottomPadding: number;
    category: string;
  };
}

interface RandomBrushProps {
  brushes: BrushData[];
  className?: string;
  alt?: string;
  instanceId?: string; // Optional ID for persistence
  category?: string; // Optional filter by category
}

export default function RandomBrush({ 
  brushes,
  className = '', 
  alt = 'Brush separator',
  instanceId,
  category 
}: RandomBrushProps) {
  const [selectedBrush, setSelectedBrush] = useState<BrushData | null>(null);
  const instanceRef = useRef<string>(instanceId || `brush-${Math.random().toString(36).substring(2, 11)}`);
  const currentInstanceId = instanceRef.current;

  // Get or set persisted brush for this instance
  const getPersistedBrush = (): string | null => {
    if (typeof window === 'undefined') return null;
    return localStorage.getItem(`random-brush-${currentInstanceId}`);
  };

  const setPersistedBrush = (brushId: string) => {
    if (typeof window === 'undefined') return;
    localStorage.setItem(`random-brush-${currentInstanceId}`, brushId);
  };

  // Select a random unused brush
  const selectRandomBrush = (): BrushData => {
    // Filter brushes by category if specified
    let availableBrushes = category 
      ? brushes.filter(brush => brush.data.category === category)
      : brushes;

    // Filter out used brushes
    availableBrushes = availableBrushes.filter(
      brush => !globalUsedBrushes.has(brush.id)
    );

    // If no available brushes, reset the pool
    if (availableBrushes.length === 0) {
      globalUsedBrushes.clear();
      availableBrushes = category 
        ? brushes.filter(brush => brush.data.category === category)
        : brushes;
    }

    // Select random brush from available pool
    const randomIndex = Math.floor(Math.random() * availableBrushes.length);
    const selectedBrush = availableBrushes[randomIndex];

    // Mark as used
    globalUsedBrushes.add(selectedBrush.id);

    return selectedBrush;
  };

  useEffect(() => {
    // Initialize global pool 
    globalBrushPool = brushes;

    // Try to get persisted brush first
    let persistedBrushId = getPersistedBrush();
    let brushToUse: BrushData;

    if (persistedBrushId) {
      // Find the persisted brush in the collection
      const persistedBrush = brushes.find(brush => brush.id === persistedBrushId);
      
      if (persistedBrush && (!category || persistedBrush.data.category === category)) {
        // Use the persisted brush for this instance
        globalUsedBrushes.add(persistedBrushId);
        brushToUse = persistedBrush;
      } else {
        // Persisted brush is invalid, select new one
        brushToUse = selectRandomBrush();
        setPersistedBrush(brushToUse.id);
      }
    } else {
      // No persisted brush, select new one
      brushToUse = selectRandomBrush();
      setPersistedBrush(brushToUse.id);
    }

    setSelectedBrush(brushToUse);

    // Cleanup: remove from used set when component unmounts
    return () => {
      if (brushToUse) {
        globalUsedBrushes.delete(brushToUse.id);
      }
    };
  }, [currentInstanceId, category]); // Remove brushes dependency to prevent re-runs

  if (!selectedBrush) {
    return null;
  }

  const { width, src, topPadding, bottomPadding } = selectedBrush.data;

  return (
    <div 
      style={{
        paddingTop: `${topPadding}px`,
        paddingBottom: `${bottomPadding}px`,
      }}
      className={className}
    >
      <Img
        src={src}
        alt={alt}
        style={{ width: `${width}px` }}
        className="block mx-auto"
        loading="lazy"
        loader={
          <div 
            style={{ width: `${width}px`, height: '60px' }}
            className="block mx-auto bg-gray-100 animate-pulse rounded"
          />
        }
        unloader={
          <div 
            style={{ width: `${width}px`, height: '60px' }}
            className="mx-auto bg-gray-200 rounded flex items-center justify-center text-gray-500 text-sm"
          >
            Brush unavailable
          </div>
        }
        decode={false}
      />
    </div>
  );
}