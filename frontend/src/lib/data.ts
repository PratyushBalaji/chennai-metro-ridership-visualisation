import Papa from 'papaparse';
export type Row = Record<string, string | number | null>;
export type Dataset =
  | 'ridership_daily'
  | 'ridership_hourly'
  | 'ridership_station'
  | 'parking_daily'
  | 'parking_hourly'
  | 'parking_station'
  | 'phpdt';
export type Archive = Record<Dataset, Row[]>;
export const source =
  'https://raw.githubusercontent.com/PratyushBalaji/chennai-metro-ridership-tracker/main/';
export const files: Record<Dataset, string> = {
  ridership_daily: 'data/ridership/ChennaiMetro_Daily_Ridership.csv',
  ridership_hourly: 'data/ridership/ChennaiMetro_Hourly_Ridership.csv',
  ridership_station: 'data/ridership/ChennaiMetro_Station_Ridership.csv',
  parking_daily: 'data/parking/ChennaiMetro_Daily_Parking.csv',
  parking_hourly: 'data/parking/ChennaiMetro_Hourly_Parking.csv',
  parking_station: 'data/parking/ChennaiMetro_Station_Parking.csv',
  phpdt: 'data/phpdt/ChennaiMetro_Daily_PHPDT.csv',
};
const dimensions = new Set([
  'Date',
  'Hour',
  'Line',
  'Station',
  'Direction',
  'Start Station',
  'End Station',
  'Start Hour',
  'End Hour',
]);
export function parseCSV(text: string): Row[] {
  const result = Papa.parse<Record<string, string>>(text.replace(/^\uFEFF/, ''), {
    header: true,
    skipEmptyLines: 'greedy',
  });
  if (result.errors.length) throw new Error('Invalid CSV: ' + result.errors[0].message);
  if (!result.meta.fields?.includes('Date')) throw new Error('Dataset has no Date column');
  return result.data
    .filter((row) => /^\d{4}-\d{2}-\d{2}$/.test(row.Date))
    .map((row) =>
      Object.fromEntries(
        Object.entries(row).map(([key, value]) => {
          if (dimensions.has(key)) return [key, value];
          const n = Number(value);
          return [key, value.trim() === '' ? null : Number.isFinite(n) ? n : value];
        }),
      ),
    );
}
export function dates(rows: Row[]) {
  return [...new Set(rows.map((r) => String(r.Date)))].sort();
}
export function latest(rows: Row[]) {
  return dates(rows).at(-1) ?? '';
}
export function onDate(rows: Row[], date: string) {
  return rows.filter((r) => r.Date === date);
}
export function number(row: Row | undefined, key: string): number | null {
  const v = row?.[key];
  return typeof v === 'number' && Number.isFinite(v) ? v : null;
}
export function numericColumns(rows: Row[], exclude: string[] = []): string[] {
  return [...new Set(rows.flatMap((r) => Object.keys(r)))].filter(
    (k) => !dimensions.has(k) && !exclude.includes(k) && rows.some((r) => typeof r[k] === 'number'),
  );
}
export function sum(rows: Row[], key: string): number | null {
  const vals = rows.map((r) => number(r, key)).filter((v): v is number => v !== null);
  return vals.length ? vals.reduce((a, b) => a + b, 0) : null;
}
export function byStation(rows: Row[]): Row[] {
  return [...new Set(rows.map((r) => String(r.Station)))].map((station) => {
    const parts = rows.filter((r) => r.Station === station);
    return {
      Station: station,
      ...Object.fromEntries(numericColumns(parts).map((k) => [k, sum(parts, k)])),
    };
  });
}
export function stationHistory(
  rows: Row[],
  station: string,
  start: string,
  end: string,
  dayFilter: string,
): Row[] {
  const matching = rows.filter(
    (r) => r.Station === station && String(r.Date) >= start && String(r.Date) <= end,
  );
  return dates(matching)
    .filter((date) => {
      const day = new Date(date + 'T12:00:00Z').getUTCDay();
      return (
        dayFilter === 'all' ||
        (dayFilter === 'weekdays' ? day !== 0 && day !== 6 : day === 0 || day === 6)
      );
    })
    .map((date) => {
      const parts = onDate(matching, date);
      return {
        Date: date,
        ...Object.fromEntries(numericColumns(parts).map((k) => [k, sum(parts, k)])),
      };
    });
}
export const format = (n: number | null | undefined) =>
  n == null ? '—' : new Intl.NumberFormat('en-IN', { maximumFractionDigits: 0 }).format(n);
export const prettyDate = (date: string) =>
  date
    ? new Intl.DateTimeFormat('en-IN', {
        day: 'numeric',
        month: 'short',
        year: 'numeric',
        timeZone: 'UTC',
      }).format(new Date(date + 'T12:00:00Z'))
    : 'No date';
export async function loadArchive(
  signal: AbortSignal,
): Promise<{ archive: Archive; fallback: boolean }> {
  const entries = Object.entries(files) as [Dataset, string][];
  async function get(local: boolean) {
    return Object.fromEntries(
      await Promise.all(
        entries.map(async ([key, path]) => {
          const response = await fetch(local ? '/data/' + path.split('/').at(-1) : source + path, {
            signal: AbortSignal.any([signal, AbortSignal.timeout(15000)]),
          });
          if (!response.ok) throw new Error('Could not load ' + path);
          return [key, parseCSV(await response.text())];
        }),
      ),
    ) as Archive;
  }
  try {
    return { archive: await get(false), fallback: false };
  } catch (error) {
    if (signal.aborted) throw error;
    return { archive: await get(true), fallback: true };
  }
}
