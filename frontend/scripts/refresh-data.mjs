import { mkdir, writeFile } from 'node:fs/promises';
const base =
  'https://raw.githubusercontent.com/PratyushBalaji/chennai-metro-ridership-tracker/main/';
const paths = [
  'Ridership/ChennaiMetro_Daily_Ridership.csv',
  'Ridership/ChennaiMetro_Hourly_Ridership.csv',
  'Ridership/ChennaiMetro_Station_Ridership.csv',
  'Parking/ChennaiMetro_Daily_Parking.csv',
  'Parking/ChennaiMetro_Hourly_Parking.csv',
  'Parking/ChennaiMetro_Station_Parking.csv',
  'PHPDT/ChennaiMetro_Daily_PHPDT.csv',
];
await mkdir('static/data', { recursive: true });
for (const path of paths) {
  const response = await fetch(base + path);
  if (!response.ok) throw new Error(path + ': ' + response.status);
  const csv = await response.text();
  if (!csv.startsWith('Date,')) throw new Error('Unexpected CSV: ' + path);
  await writeFile('static/data/' + path.split('/').at(-1), csv);
  console.log(path);
}
await writeFile(
  'static/data/snapshot.json',
  JSON.stringify({ downloadedAt: new Date().toISOString() }),
);
