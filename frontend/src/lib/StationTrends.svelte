<script lang="ts">
  import { dates, numericColumns, stationHistory, number, type Row } from './data';
  import metadata from './metadata.json';
  import Chart from './Chart.svelte';
  import DataTable from './DataTable.svelte';
  import type { Data } from 'plotly.js';
  let { rows }: { rows: Row[] } = $props();
  const names: Record<string, string> = metadata.STATION_CODE_TO_NAME;
  let available = $derived(dates(rows));
  let start = $state('');
  let end = $state('');
  let station = $state('');
  let days = $state('all');
  let modes = $state<string[]>(['Total']);
  let choices = $derived(
    [...new Set(rows.map((r) => String(r.Station)))].sort((a, b) =>
      (names[a] ?? a).localeCompare(names[b] ?? b),
    ),
  );
  let selectedStation = $derived(station || choices[0] || '');
  let from = $derived(start || available[0] || '');
  let to = $derived(end || available.at(-1) || '');
  let filtered = $derived(stationHistory(rows, selectedStation, from, to, days));
  let columns = $derived(numericColumns(rows));
  let traces = $derived([
    {
      type: 'bar',
      x: filtered.map((r) => r.Date),
      y: filtered.map((r) => number(r, 'Total')),
      name: 'Total passengers',
      marker: { color: '#69b7ff' },
      opacity: 0.5,
    },
    ...modes.map((column) => ({
      type: 'scatter',
      mode: 'lines+markers',
      x: filtered.map((r) => r.Date),
      y: filtered.map((r) => number(r, column)),
      name: column,
      line: { width: 2 },
      marker: { size: 4 },
      connectgaps: false,
    })),
  ] as Data[]);
</script>

<div class="page-heading">
  <div>
    <p class="eyebrow">FOLLOW THE PATTERN</p>
    <h1>Station trends</h1>
    <p class="muted">Explore a station’s ridership history by fare mode and day of the week.</p>
  </div>
</div>
<div class="explorer-grid">
  <aside class="panel filters">
    <h2>Explore</h2>
    <label
      >Station<select value={selectedStation} onchange={(e) => (station = e.currentTarget.value)}
        >{#each choices as code}<option value={code}>{names[code] ?? code} ({code})</option
          >{/each}</select
      ></label
    ><label
      >From<input
        type="date"
        value={from}
        min={available[0]}
        max={to}
        onchange={(e) => (start = e.currentTarget.value)}
      /></label
    ><label
      >To<input
        type="date"
        value={to}
        min={from}
        max={available.at(-1)}
        onchange={(e) => (end = e.currentTarget.value)}
      /></label
    ><label
      >Days<select bind:value={days}
        ><option value="all">All days</option><option value="weekdays">Weekdays only</option><option
          value="weekends">Weekends only</option
        ></select
      ></label
    >
    <fieldset>
      <legend>Fare modes (lines)</legend>{#each columns as column}<label class="check"
          ><input type="checkbox" bind:group={modes} value={column} />{column}</label
        >{/each}
    </fieldset>
  </aside>
  <section class="panel">
    <h2>{names[selectedStation] ?? selectedStation}</h2>
    <p class="caption">
      {filtered.length} observed days · Interchange line records are combined, matching the existing trends
      view.
    </p>
    {#if filtered.length}<Chart
        {traces}
        height={570}
        layout={{
          xaxis: { type: 'date', title: { text: 'Date' }, gridcolor: '#28313e' },
          yaxis: { title: { text: 'Passengers' }, gridcolor: '#28313e' },
        }}
      /><DataTable rows={filtered} />{:else}<p class="empty">
        No observations match this station and date range.
      </p>{/if}
  </section>
</div>
