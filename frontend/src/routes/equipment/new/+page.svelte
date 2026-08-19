<script lang="ts">
  import { goto } from '$app/navigation';
  import EquipmentForm from '$lib/equipment/components/EquipmentForm.svelte';
  import { createEquipment } from '$lib/equipment/api';
  import type { CreateEquipmentPayload } from '$lib/equipment/types';

  let submitError = '';

  async function handleSubmit(payload: CreateEquipmentPayload): Promise<void> {
    submitError = '';
    try {
      await createEquipment(payload);
      goto('/equipment');
    } catch (e) {
      submitError = e instanceof Error ? e.message : 'Failed to create equipment.';
      throw e;
    }
  }
</script>

<div class="page">
  <a href="/equipment" class="back-link">← Back to list</a>
  <h1>Add New Equipment</h1>
  {#if submitError}
    <p class="error" role="alert">{submitError}</p>
  {/if}
  <EquipmentForm onSubmit={handleSubmit} />
</div>

<style>
  .page { padding: 2rem; max-width: 600px; margin: 0 auto; }
  .back-link { display: inline-block; margin-bottom: 1rem; color: #555; text-decoration: none; }
  h1 { margin-bottom: 1.5rem; }
  .error { color: #c0392b; }
</style>
