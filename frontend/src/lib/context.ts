import type { Archive } from './data';
export type ArchiveContext = () => {
  archive: Archive | null;
  loading: boolean;
  error: string;
  fallback: boolean;
};
