<script lang="ts">
  import { onMount } from 'svelte';
  import { page } from '$app/stores';
  import { goto } from '$app/navigation';
  import { getEquipment, toggleEquipmentStatus, deleteEquipment } from '$lib/equipment/api';
  import type { Equipment } from '$lib/equipment/types';

  let equipment: Equipment | null = null;
  let notFound = false;
  let loading = true;
  let error = '';
  let toggling = false;
  let deleting = false;

  $: id = $page.params.id;

  onMount(async () => {
    try {
      equipment = await getEquipment(id);
    } catch (e) {
      const msg = e instanceof Error ? e.message : '';
      if (msg.includes('404') || msg.toLowerCase().includes('not found')) {
        notFound = true;
      } else {
        error = msg || 'Failed to load equipment.';
      }
    } finally {
      loading = false;
    }
  });

  async function handleToggle() {
    if (!equipment) return;
    toggling = true;
    try {
      equipment = await toggleEquipmentStatus(equipment.id);
    } catch (e) {
      error = e instanceof Error ? e.message : 'Failed to toggle status.';
    } finally {
      toggling = false;
    }
  }

  async function handleDelete() {
    if (!equipment) return;
    if (!confirm(`Permanently delete "${equipment.name}"? This cannot be undone.`)) return;
    deleting = true;
    try {
      await deleteEquipment(equipment.id);
      goto('/equipment');
    } catch (e) {
      error = e instanceof Error ? e.message : 'Failed to delete equipment.';
      deleting = false;
    }
  }
</script>

<div class="page">
  <a href="/equipment" class="back-link">← Back to list</a>

  {#if loading}
    <p>Loading...</p>
  {:else if notFound}
    <p class="not-found">Equipment not found.</p>
  {:else if error}
    <p class="error">{error}</p>
  {:else if equipment}
    <div class="detail-card">
      <div class="detail-header">
        <h1>{equipment.name}</h1>
        <span class="status-badge" class:active={equipment.status === 'ACTIVE'} class:inactive={equipment.status === 'INACTIVE'}>
          {equipment.status}
        </span>
      </div>
      <dl class="detail-fields">
        <dt>ID</dt><dd>{equipment.id}</dd>
        <dt>Description</dt><dd>{equipment.description || '—'}</dd>
        <dt>Category</dt><dd>{equipment.category.replace(/_/g, ' ')}</dd>
        <dt>Daily Rental Price</dt><dd>${Number(equipment.daily_rental_price).toFixed(2)}/day</dd>
        <dt>Status</dt><dd>{equipment.status}</dd>
      </dl>
      <div class="actions">
        <a href="/equipment/{equipment.id}/edit" class="btn-secondary">Edit</a>
        <button
          class="btn-toggle"
          class:deactivate={equipment.status === 'ACTIVE'}
          class:reactivate={equipment.status === 'INACTIVE'}
          on:click={handleToggle}
          disabled={toggling || deleting}
        >
          {toggling ? 'Updating...' : equipment.status === 'ACTIVE' ? 'Deactivate' : 'Reactivate'}
        </button>
        <button
          class="btn-delete"
          on:click={handleDelete}
          disabled={deleting || toggling}
        >
          {deleting ? 'Deleting...' : 'Delete'}
        </button>
      </div>
    </div>
  {/if}
</div>

<style>
  .page { padding: 2rem; max-width: 700px; margin: 0 auto; }
  .back-link { display: inline-block; margin-bottom: 1.5rem; color: #555; text-decoration: none; }
  .detail-card { background: white; border: 1px solid #ddd; border-radius: 8px; padding: 1.5rem 2rem; }
  .detail-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.5rem; }
  h1 { margin: 0; }
  .status-badge { padding: 0.2rem 0.6rem; border-radius: 12px; font-size: 0.8rem; font-weight: 600; text-transform: uppercase; }
  .active { background: #d4edda; color: #155724; }
  .inactive { background: #e2e3e5; color: #383d41; }
  dl { display: grid; grid-template-columns: 160px 1fr; gap: 0.5rem 1rem; }
  dt { font-weight: 600; color: #444; }
  dd { margin: 0; color: #222; }
  .actions { margin-top: 1.5rem; display: flex; gap: 1rem; }
  .btn-secondary { padding: 0.5rem 1.25rem; border: 1px solid #2c3e50; color: #2c3e50; border-radius: 4px; text-decoration: none; }
  .btn-toggle { padding: 0.5rem 1.25rem; border: none; border-radius: 4px; font-size: 0.95rem; cursor: pointer; }
  .deactivate { background: #e74c3c; color: white; }
  .reactivate { background: #27ae60; color: white; }
  .btn-toggle:disabled { opacity: 0.6; cursor: not-allowed; }
  .btn-delete { padding: 0.5rem 1.25rem; border: none; border-radius: 4px; font-size: 0.95rem; cursor: pointer; background: #7f8c8d; color: white; }
  .btn-delete:hover { background: #636e72; }
  .btn-delete:disabled { opacity: 0.6; cursor: not-allowed; }
  .not-found, .error { color: #c0392b; font-size: 1.1rem; }
</style>
