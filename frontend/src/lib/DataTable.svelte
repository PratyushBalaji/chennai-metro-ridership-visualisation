<script lang="ts">
  import type { Row } from './data';
  import { format } from './data';
  let { rows, label = 'View source values' }: { rows: Row[]; label?: string } = $props();
  let columns = $derived([...new Set(rows.flatMap((r) => Object.keys(r)))]);
</script>

<details class="table-details">
  <summary>{label} · {rows.length} rows</summary>
  <div class="table-scroll">
    <table>
      <thead
        ><tr
          >{#each columns as column}<th>{column}</th>{/each}</tr
        ></thead
      ><tbody
        >{#each rows as row}<tr
            >{#each columns as column}<td
                >{typeof row[column] === 'number'
                  ? format(row[column] as number)
                  : (row[column] ?? '—')}</td
              >{/each}</tr
          >{/each}</tbody
      >
    </table>
  </div>
</details>
