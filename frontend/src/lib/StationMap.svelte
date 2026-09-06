<script lang="ts">
  import { dates, byStation, onDate, number, format, prettyDate, type Row } from './data';
  import metadata from './metadata.json';
  import Chart from './Chart.svelte';
  import DataTable from './DataTable.svelte';
  import type { Data } from 'plotly.js';
  let { rows }: { rows: Row[] } = $props();
  const names: Record<string, string> = metadata.STATION_CODE_TO_NAME;
  const coordinates: Record<string, number[]> = metadata.STATION_COORDINATES;
  let allDates = $derived(dates(rows));
  let start = $state('');
  let end = $state('');
  let selected = $state('');
  let from = $derived(start || allDates[0] || '');
  let to = $derived(end || allDates.at(-1) || '');
  let available = $derived(allDates.filter((d) => d >= from && d <= to));
  let date = $derived(available.includes(selected) ? selected : available.at(-1) || '');
  let stations = $derived(byStation(onDate(rows, date)));
  let mapped = $derived(
    stations.filter((r) => coordinates[String(r.Station)] && number(r, 'Total') !== null),
  );
  let unknown = $derived(stations.filter((r) => !coordinates[String(r.Station)]));
  let scaleMax = $derived.by(() => {
    // Hold the scale constant through the selected range, including interchange aggregation.
    const totals = new Map<string, number>();
    for (const row of rows) {
      if (String(row.Date) < from || String(row.Date) > to) continue;
      const value = number(row, 'Total');
      if (value === null) continue;
      const key = row.Date + ':' + row.Station;
      totals.set(key, (totals.get(key) ?? 0) + value);
    }
    return Math.max(1, ...totals.values());
  });
  const minimumZoom = 10.4;
  let traces = $derived([
    {
      type: 'densitymap',
      lat: mapped.map((r) => coordinates[String(r.Station)][0]),
      lon: mapped.map((r) => coordinates[String(r.Station)][1]),
      z: mapped.map((r) => number(r, 'Total')),
      zmin: 0,
      zmax: scaleMax,
      radius: 28,
      colorscale: [
        [0, '#0d0887'],
        [0.2, '#6a00a8'],
        [0.4, '#b12a90'],
        [0.6, '#e16462'],
        [0.8, '#fca636'],
        [1, '#f0f921'],
      ],
      colorbar: { title: { text: 'Passengers' }, thickness: 12 },
      hoverinfo: 'skip',
    },
    {
      type: 'scattermap',
      lat: mapped.map((r) => coordinates[String(r.Station)][0]),
      lon: mapped.map((r) => coordinates[String(r.Station)][1]),
      mode: 'markers',
      marker: { size: 7, color: '#e7efff', opacity: 0.85 },
      text: mapped.map((r) => (names[String(r.Station)] ?? r.Station) + ' (' + r.Station + ')'),
      customdata: mapped.map((r) => number(r, 'Total')),
      hovertemplate: '%{text}<br>%{customdata:,} passengers<extra></extra>',
      showlegend: false,
    },
  ] as Data[]);
</script>

<div class="page-heading">
  <div>
    <p class="eyebrow">CHENNAI, STATION BY STATION</p>
    <h1>Ridership heatmap</h1>
    <p class="muted">Scrub through the archive to see how station activity changes.</p>
  </div>
  <span class="badge">Geographic view</span>
</div>
<div class="controls">
  <label
    >From<input
      type="date"
      value={from}
      min={allDates[0]}
      max={to}
      onchange={(e) => (start = e.currentTarget.value)}
    /></label
  ><label
    >To<input
      type="date"
      value={to}
      min={from}
      max={allDates.at(-1)}
      onchange={(e) => (end = e.currentTarget.value)}
    /></label
  >
  <div class="map-date">
    <strong>{prettyDate(date)}</strong><span class="muted"
      >{stations.length} stations with records</span
    >
  </div>
</div>
<section class="panel map-panel">
  {#if mapped.length}<Chart
      {traces}
      height={660}
      layout={{
        map: {
          // Keep Plotly's reliable dark basemap for now. A reviewed, bundled
          // label-free route basemap can replace this without changing the data layer.
          style: 'carto-darkmatter',
          center: { lat: 13.0827, lon: 80.2307 },
          zoom: minimumZoom,
        },
        uirevision: 'chennai-station-map',
        margin: { l: 0, r: 0, t: 0, b: 0 },
        hovermode: 'closest',
      }}
      minMapZoom={minimumZoom}
    />{:else}<p class="empty">No mapped station observations for this date range.</p>{/if}
  <div class="scrubber">
    <button
      aria-label="Previous day"
      disabled={available.indexOf(date) <= 0}
      onclick={() => (selected = available[available.indexOf(date) - 1])}>←</button
    ><input
      aria-label="Map date"
      type="range"
      min="0"
      max={Math.max(0, available.length - 1)}
      value={Math.max(0, available.indexOf(date))}
      oninput={(e) => (selected = available[Number(e.currentTarget.value)])}
    /><button
      aria-label="Next day"
      disabled={available.indexOf(date) >= available.length - 1}
      onclick={() => (selected = available[available.indexOf(date) + 1])}>→</button
    >
  </div>
  <p class="caption">
    Fixed scale across this range: 0–{format(scaleMax)} passengers. Heat shows station activity, not routes
    or journeys. Basemap © CARTO / OpenStreetMap contributors.
  </p>
  {#if unknown.length}<p class="notice">
      {unknown.length} stations have no coordinates and appear only in the table.
    </p>{/if}<DataTable
    rows={stations.map((r) => ({
      Station: r.Station,
      Name: names[String(r.Station)] ?? r.Station,
      Total: r.Total,
    }))}
  />
</section>
