<script lang="ts">
  import type { Archive, Row } from './data';
  import { dates, onDate, number, numericColumns, format, latest } from './data';
  import metadata from './metadata.json';
  import DateControl from './DateControl.svelte';
  import FlowChart from './FlowChart.svelte';
  import Chart from './Chart.svelte';
  import DataTable from './DataTable.svelte';
  import type { Data } from 'plotly.js';
  let { archive }: { archive: Archive } = $props();
  let tab = $state<'ridership' | 'parking' | 'phpdt'>('ridership');
  let chosenDate = $state('');
  let display = $state('both');
  const names: Record<string, string> = metadata.STATION_CODE_TO_NAME;
  const order: Record<string, string[]> = metadata.PHPDT_LINE_STATIONS;
  const labels: Record<string, string> = {
    ...metadata.PAYMENT_METHOD_DISPLAY_NAMES,
    ...metadata.PARKING_COLUMN_DISPLAY_NAMES,
  };
  let available = $derived(
    dates(
      tab === 'phpdt'
        ? archive.phpdt
        : [
            ...archive[(tab + '_daily') as 'ridership_daily'],
            ...archive[(tab + '_hourly') as 'ridership_hourly'],
            ...archive[(tab + '_station') as 'ridership_station'],
          ],
    ),
  );
  let date = $derived(chosenDate || available.at(-1) || '');
  let daily = $derived(
    tab === 'phpdt' ? [] : onDate(archive[(tab + '_daily') as 'ridership_daily'], date),
  );
  let hourly = $derived(
    tab === 'phpdt'
      ? []
      : onDate(archive[(tab + '_hourly') as 'ridership_hourly'], date).sort((a, b) =>
          String(a.Hour).localeCompare(String(b.Hour)),
        ),
  );
  let stations = $derived(
    tab === 'phpdt' ? [] : onDate(archive[(tab + '_station') as 'ridership_station'], date),
  );
  let first = $derived(daily[0]);
  const add = (row: Row | undefined, keys: string[]) => {
    const vals = keys.map((k) => number(row, k));
    return vals.some((v) => v === null) ? null : vals.reduce<number>((a, b) => a + (b ?? 0), 0);
  };
  function correctedParking(row: Row | undefined, key: string) {
    const a = number(row, key);
    const b = number(row, 'fourWheeler');
    return key === 'threeWheeler' ? (a === null || b === null ? null : a - b) : a;
  }
  let headline = $derived(
    tab === 'ridership'
      ? [
          ['Passengers', number(first, 'Total')],
          ['Stored value cards', number(first, 'noOfCards')],
          ['Singara Chennai cards', number(first, 'noOfNCMCcard')],
          ['QR tickets', number(first, 'noOfTotal_QR')],
        ]
      : [
          ['Vehicles', number(first, 'Total Vehicles')],
          [
            'ICE vehicles',
            add(first, ['threeWheeler', 'twoWheeler', 'sixWheeler', 'eightWheeler']),
          ],
          ['Electric', add(first, ['eFourWheeler', 'eTwoWheeler'])],
          ['Hybrid', add(first, ['hFourWheeler', 'hTwoWheeler'])],
        ],
  );
  let breakdown = $derived(
    numericColumns(
      daily,
      tab === 'ridership'
        ? ['Total', 'noOfTotal_QR', 'noOfONDCQR', 'noOfSVC', 'noOfToken']
        : ['Total Vehicles'],
    ).sort((a, b) => (number(first, b) ?? 0) - (number(first, a) ?? 0)),
  );
  function lineStations(line: string) {
    return stations
      .filter((r) => Number(r.Line) === Number(line))
      .sort(
        (a, b) =>
          (order[line]?.indexOf(String(a.Station)) ?? 0) -
          (order[line]?.indexOf(String(b.Station)) ?? 0),
      )
      .map((r) => ({ ...r, StationLabel: names[String(r.Station)] ?? String(r.Station) }));
  }
  function phpdtRows(line: string) {
    return onDate(archive.phpdt, date).filter((r) => Number(r.Line) === Number(line));
  }
  function corridorTraces(line: string): Data[] {
    const rows = phpdtRows(line);
    const stops = order[line] ?? [];
    const traces: Data[] = [];
    for (const direction of ['UP', 'DOWN']) {
      const points = stops.slice(0, -1).map((s, i) => {
        const from = direction === 'UP' ? s : stops[i + 1],
          to = direction === 'UP' ? stops[i + 1] : s;
        const row = rows.find(
          (r) =>
            r.Direction === direction && r['Start Station'] === from && r['End Station'] === to,
        );
        return {
          x: i + 0.5,
          y: number(row, 'PHPDT'),
          text:
            (names[from] ?? from) +
            ' → ' +
            (names[to] ?? to) +
            '<br>Peak: ' +
            (row ? row['Start Hour'] + '–' + row['End Hour'] : 'unavailable'),
        };
      });
      const color =
        line === '1'
          ? direction === 'UP'
            ? '#69b7ff'
            : '#417dd9'
          : direction === 'UP'
            ? '#71dfac'
            : '#35a773';
      for (const type of display === 'both'
        ? ['bar', 'scatter']
        : display === 'bars'
          ? ['bar']
          : ['scatter']) {
        traces.push({
          type,
          x: points.map((p) => p.x),
          y: points.map((p) => p.y),
          customdata: points.map((p) => p.text),
          name: direction,
          legendgroup: direction,
          showlegend: display !== 'both' || type === 'bar',
          marker: { color },
          line: { color, width: 2 },
          mode: 'lines',
          connectgaps: false,
          hovertemplate: '%{customdata}<br>%{y:,} passengers<extra>' + direction + '</extra>',
        } as Data);
      }
    }
    return traces;
  }
</script>

<div class="page-heading">
  <div>
    <p class="eyebrow">THE DAILY PICTURE</p>
    <h1>Historical dashboard</h1>
    <p class="muted">Ridership, parking and peak-hour traffic across Chennai Metro.</p>
  </div>
  <a
    class="badge"
    href="https://github.com/PratyushBalaji/chennai-metro-ridership-tracker"
    target="_blank"
    rel="noreferrer"
    aria-label="Open the Chennai Metro ridership data repository">CMRL archive ↗</a
  >
</div>
<div class="toolbar">
  <div class="tabs" aria-label="Dataset">
    {#each ['ridership', 'parking', 'phpdt'] as key}<button
        class:active={tab === key}
        onclick={() => {
          tab = key as typeof tab;
        }}>{key === 'phpdt' ? 'PHPDT' : key[0].toUpperCase() + key.slice(1)}</button
      >{/each}
  </div>
  <DateControl {available} value={date} onchange={(value) => (chosenDate = value)} />
</div>
{#if !available.includes(date)}<p class="notice">
    No {tab} observations on this date. Choose another date or Latest.
  </p>{/if}
{#if tab !== 'phpdt'}
  <div class="metrics">
    {#each headline as metric, i}<section class="metric">
        <span>{metric[0]}</span><strong
          style:color={['#69b7ff', '#f1b06e', '#5dd7c3', '#b3a0ff'][i]}
          >{format(metric[1] as number | null)}</strong
        >{#if i === 3 && tab === 'ridership'}<small
            >Includes {format(number(first, 'noOfONDCQR'))} ONDC tickets</small
          >{/if}
      </section>{/each}
  </div>
  <section class="panel">
    <h2>{tab === 'ridership' ? 'Payment methods' : 'Vehicle types'}</h2>
    {#if first}<div class="breakdown">
        {#each breakdown as key}<div>
            <span>{labels[key] ?? key}</span><strong
              >{format(
                tab === 'parking' ? correctedParking(first, key) : number(first, key),
              )}</strong
            >
          </div>{/each}
      </div>
      {#if tab === 'parking'}<p class="caption">
          As in the existing dashboard, daily 3-wheeler count subtracts 4-wheelers from the combined
          source field.
        </p>{/if}<DataTable rows={daily} />{:else}<p class="empty">
        No daily aggregate for this date.
      </p>{/if}
  </section>
  <FlowChart
    rows={hourly}
    title={tab === 'ridership' ? 'Hourly passenger flow' : 'Hourly parking'}
    total={tab === 'ridership' ? 'Total' : 'Total Vehicles'}
    exclude={['General Parking']}
  />
  {#each ['1', '2'] as line}<FlowChart
      rows={lineStations(line)}
      title={(line === '1' ? 'Blue' : 'Green') +
        ' line · ' +
        (tab === 'ridership' ? 'station passenger flow' : 'station parking')}
      x="StationLabel"
      total={tab === 'ridership' ? 'Total' : 'Total Vehicles'}
      color={line === '1' ? '#69b7ff' : '#71dfac'}
      exclude={['General Parking', 'Eight Wheleer']}
    />{/each}
{:else}
  <p class="caption">
    Peak Hour Per Direction Traffic · Values describe adjacent station segments, not station
    entries.
  </p>
  <div class="controls">
    <label
      >Display<select bind:value={display}
        ><option value="both">Bars + lines</option><option value="bars">Bars only</option><option
          value="lines">Lines only</option
        ></select
      ></label
    >
  </div>
  {#each ['1', '2'] as line}<section class="panel">
      <h2>{line === '1' ? 'Blue' : 'Green'} line</h2>
      {#if phpdtRows(line).length}<Chart
          traces={corridorTraces(line)}
          height={570}
          layout={{
            barmode: 'group',
            xaxis: {
              range: [-0.5, order[line].length - 0.5],
              tickmode: 'array',
              tickvals: order[line].map((_, i) => i),
              ticktext: order[line].map((s) => names[s] ?? s),
              tickangle: -40,
              automargin: true,
            },
            yaxis: {
              title: { text: 'Peak-hour passengers' },
              gridcolor: '#28313e',
              rangemode: 'tozero',
            },
          }}
        /><DataTable rows={phpdtRows(line)} />{:else}<p class="empty">
          No PHPDT data for this line and date.
        </p>{/if}
    </section>{/each}
{/if}
