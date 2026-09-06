<script lang="ts">
  import { prettyDate } from './data';
  let {
    available,
    value,
    onchange,
  }: { available: string[]; value: string; onchange: (date: string) => void } = $props();
  let index = $derived(available.indexOf(value));
</script>

<div class="date-control">
  <button
    aria-label="Previous available date"
    disabled={index <= 0}
    onclick={() => onchange(available[index - 1])}>←</button
  >
  <label
    ><span class="sr-only">Dataset date</span><input
      type="date"
      {value}
      min={available[0]}
      max={available.at(-1)}
      onchange={(e) => {
        if (e.currentTarget.value) onchange(e.currentTarget.value);
      }}
    /></label
  >
  <button
    aria-label="Next available date"
    disabled={index < 0 || index >= available.length - 1}
    onclick={() => onchange(available[index + 1])}>→</button
  >
  <button
    onclick={() => {
      const last = available.at(-1);
      if (last) onchange(last);
    }}>Latest</button
  >
  <span class="muted">{prettyDate(value)}</span>
</div>
