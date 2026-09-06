<script lang="ts">
  import Chart from './Chart.svelte';
  import DataTable from './DataTable.svelte';
  import { numericColumns, number, sum, type Row } from './data';
  import metadata from './metadata.json';
  import type { Data } from 'plotly.js';
  let {
    rows,
    title,
    x = 'Hour',
    total = 'Total',
    color = '#69b7ff',
    exclude = [],
  }: {
    rows: Row[];
    title: string;
    x?: string;
    total?: string;
    color?: string;
    exclude?: string[];
  } = $props();
  const labels: Record<string, string> = {
    ...metadata.PAYMENT_METHOD_DISPLAY_NAMES,
    ...metadata.PARKING_COLUMN_DISPLAY_NAMES,
  };
  let series = $derived(
    numericColumns(rows, [total, ...exclude]).sort(
      (a, b) => (sum(rows, b) ?? 0) - (sum(rows, a) ?? 0),
    ),
  );
  let traces = $derived([
    {
      type: 'bar',
      x: rows.map((r) => r[x]),
      y: rows.map((r) => number(r, total)),
      name: total,
      marker: { color },
      opacity: 0.65,
    },
    ...series.map((column) => ({
      type: 'scatter',
      mode: 'lines',
      x: rows.map((r) => r[x]),
      y: rows.map((r) => number(r, column)),
      name: labels[column] ?? column,
      connectgaps: false,
      line: { width: 2 },
    })),
  ] as Data[]);
</script>

<section class="panel">
  <h2>{title}</h2>
  {#if rows.length}<Chart
      {traces}
      height={x === 'Hour' ? 450 : 540}
      layout={{
        xaxis: { type: 'category', automargin: true, tickangle: x === 'Hour' ? 0 : -35 },
        yaxis: {
          title: { text: total === 'Total' ? 'Passengers' : 'Vehicles' },
          gridcolor: '#28313e',
        },
      }}
    /><DataTable {rows} />{:else}<p class="empty">No observations for this date.</p>{/if}
</section>
