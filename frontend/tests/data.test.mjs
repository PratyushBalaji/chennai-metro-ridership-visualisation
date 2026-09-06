import test from 'node:test';
import assert from 'node:assert/strict';
import { parseCSV, latest, number, sum, byStation, stationHistory } from '../src/lib/data.ts';

test('CSV preserves official codes, quoted labels, missing values and zero', () => {
  const [row] = parseCSV('Date,Line,Station,Total,"Fare, mode",Missing\n2026-09-05,01,SCC,0,12,\n');
  assert.equal(row.Line, '01');
  assert.equal(row.Station, 'SCC');
  assert.equal(number(row, 'Total'), 0);
  assert.equal(number(row, 'Missing'), null);
  assert.equal(row['Fare, mode'], 12);
});
test('latest date comes from available records regardless of order', () => {
  assert.equal(
    latest([{ Date: '2026-02-12' }, { Date: '2026-09-05' }, { Date: '2026-03-01' }]),
    '2026-09-05',
  );
  assert.equal(latest([]), '');
});
test('unavailable totals do not turn into zero', () => {
  assert.equal(sum([{ Total: null }], 'Total'), null);
  assert.equal(sum([{ Total: 0 }], 'Total'), 0);
});
test('map combines interchange line records but keeps other stations separate', () => {
  const result = byStation([
    { Station: 'SCC', Line: '01', Total: 12 },
    { Station: 'SCC', Line: '02', Total: 8 },
    { Station: 'SAL', Total: 0 },
  ]);
  assert.equal(result.find((r) => r.Station === 'SCC').Total, 20);
  assert.equal(result.find((r) => r.Station === 'SAL').Total, 0);
});
test('station histories apply inclusive dates and UTC-stable weekday filters', () => {
  const rows = [
    { Station: 'SCC', Date: '2026-09-04', Total: 12 },
    { Station: 'SCC', Date: '2026-09-04', Total: 8 },
    { Station: 'SCC', Date: '2026-09-05', Total: 30 },
    { Station: 'SAL', Date: '2026-09-04', Total: 900 },
  ];
  assert.deepEqual(stationHistory(rows, 'SCC', '2026-09-04', '2026-09-05', 'weekdays'), [
    { Date: '2026-09-04', Total: 20 },
  ]);
  assert.deepEqual(stationHistory(rows, 'SCC', '2026-09-04', '2026-09-05', 'weekends'), [
    { Date: '2026-09-05', Total: 30 },
  ]);
  assert.deepEqual(stationHistory(rows, 'SCC', '2026-09-05', '2026-09-04', 'all'), []);
});
test('malformed CSV is rejected instead of displayed as observations', () => {
  assert.throws(() => parseCSV('<html>not data</html>'), /Date|Invalid CSV/);
  assert.throws(() => parseCSV('Date,Total\n2026-09-05,1,2\n'), /Invalid CSV/);
});
