<script lang="ts">
  import { onMount } from 'svelte';
  import { goto } from '$app/navigation';
  import { listEquipment } from '$lib/equipment/api';
  import type { Equipment } from '$lib/equipment/types';

  let equipment: Equipment[] = [];
  let loading = true;
  let error = '';

  onMount(async () => {
    try {
      equipment = await listEquipment();
    } catch (e) {
      error = e instanceof Error ? e.message : 'Failed to load equipment.';
    } finally {
      loading = false;
    }
  });
</script>

<div class="page">
  <div class="header">
    <h1>Equipment Catalog</h1>
    <a href="/equipment/new" class="btn-primary">Add Equipment</a>
  </div>

  {#if loading}
    <p>Loading...</p>
  {:else if error}
    <p class="error">{error}</p>
  {:else if equipment.length === 0}
    <p class="empty-state">No equipment has been added yet.</p>
  {:else}
    <div class="equipment-list">
      {#each equipment as item (item.id)}
        <div
          class="equipment-card"
          class:inactive={item.status === 'INACTIVE'}
          on:click={() => goto(`/equipment/${item.id}`)}
          on:keydown={(e) => e.key === 'Enter' && goto(`/equipment/${item.id}`)}
          role="button"
          tabindex="0"
          aria-label="View {item.name}"
        >
          <div class="card-header">
            <h2>{item.name}</h2>
            <span class="status-badge" class:active={item.status === 'ACTIVE'} class:inactive-badge={item.status === 'INACTIVE'}>
              {item.status}
            </span>
          </div>
          <div class="card-body">
            <span class="category">{item.category.replace(/_/g, ' ')}</span>
            <span class="price">${Number(item.daily_rental_price).toFixed(2)}/day</span>
          </div>
        </div>
      {/each}
    </div>
  {/if}
</div>

<style>
  .page { padding: 2rem; max-width: 900px; margin: 0 auto; }
  .header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.5rem; }
  h1 { margin: 0; }
  .btn-primary { padding: 0.5rem 1.25rem; background-color: #2c3e50; color: white; text-decoration: none; border-radius: 4px; }
  .equipment-list { display: grid; gap: 1rem; }
  .equipment-card { background: white; border: 1px solid #ddd; border-radius: 8px; padding: 1rem 1.25rem; cursor: pointer; transition: box-shadow 0.15s; }
  .equipment-card:hover { box-shadow: 0 2px 8px rgba(0,0,0,0.1); }
  .equipment-card.inactive { opacity: 0.55; }
  .card-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem; }
  h2 { margin: 0; font-size: 1.1rem; }
  .status-badge { padding: 0.2rem 0.6rem; border-radius: 12px; font-size: 0.75rem; font-weight: 600; text-transform: uppercase; }
  .active { background: #d4edda; color: #155724; }
  .inactive-badge { background: #e2e3e5; color: #383d41; }
  .card-body { display: flex; gap: 1.5rem; color: #555; font-size: 0.9rem; }
  .empty-state { color: #777; font-style: italic; }
  .error { color: #c0392b; }
</style>
