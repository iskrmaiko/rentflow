<script lang="ts">
  import { onMount } from 'svelte';
  import { page } from '$app/stores';
  import { goto } from '$app/navigation';
  import EquipmentForm from '$lib/equipment/components/EquipmentForm.svelte';
  import { getEquipment, updateEquipment } from '$lib/equipment/api';
  import type { Equipment, CreateEquipmentPayload } from '$lib/equipment/types';

  let equipment: Equipment | null = null;
  let loading = true;
  let loadError = '';
  let submitError = '';

  $: id = $page.params.id;

  onMount(async () => {
    try {
      equipment = await getEquipment(id);
    } catch (e) {
      loadError = e instanceof Error ? e.message : 'Failed to load equipment.';
    } finally {
      loading = false;
    }
  });

  async function handleSubmit(payload: CreateEquipmentPayload): Promise<void> {
    submitError = '';
    try {
      await updateEquipment(id, payload);
      goto(`/equipment/${id}`);
    } catch (e) {
      submitError = e instanceof Error ? e.message : 'Failed to update equipment.';
      throw e;
    }
  }
</script>

<div class="page">
  <a href="/equipment/{id}" class="back-link">← Back to detail</a>
  <h1>Edit Equipment</h1>

  {#if loading}
    <p>Loading...</p>
  {:else if loadError}
    <p class="error">{loadError}</p>
  {:else if equipment}
    {#if submitError}
      <p class="error" role="alert">{submitError}</p>
    {/if}
    <EquipmentForm initialValues={equipment} onSubmit={handleSubmit} />
  {/if}
</div>

<style>
  .page { padding: 2rem; max-width: 600px; margin: 0 auto; }
  .back-link { display: inline-block; margin-bottom: 1rem; color: #555; text-decoration: none; }
  h1 { margin-bottom: 1.5rem; }
  .error { color: #c0392b; }
</style>
