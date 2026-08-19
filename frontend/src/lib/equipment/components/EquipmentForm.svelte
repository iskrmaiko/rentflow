<script lang="ts">
  import type { Equipment, CreateEquipmentPayload, EquipmentCategory } from '$lib/equipment/types';

  export let initialValues: Equipment | undefined = undefined;
  export let onSubmit: (payload: CreateEquipmentPayload) => Promise<void>;

  const CATEGORIES: EquipmentCategory[] = [
    'POWER_TOOLS',
    'HAND_TOOLS',
    'CONSTRUCTION',
    'LANDSCAPING',
    'LIGHTING',
    'AUDIO_VISUAL',
    'CLEANING',
    'SAFETY',
    'TRANSPORTATION',
    'OTHER',
  ];

  let name = initialValues?.name ?? '';
  let description = initialValues?.description ?? '';
  let category: EquipmentCategory | '' = initialValues?.category ?? '';
  let daily_rental_price = initialValues?.daily_rental_price?.toString() ?? '';

  let nameError = '';
  let categoryError = '';
  let priceError = '';
  let submitting = false;

  function validate(): boolean {
    nameError = '';
    categoryError = '';
    priceError = '';

    if (!name || name.trim() === '') {
      nameError = 'Name is required.';
    }
    if (!category) {
      categoryError = 'Category is required.';
    }
    const priceNum = parseFloat(daily_rental_price);
    if (daily_rental_price === '' || isNaN(priceNum) || priceNum < 0) {
      priceError = 'Price must be a non-negative number.';
    }

    return !nameError && !categoryError && !priceError;
  }

  async function handleSubmit(event: SubmitEvent) {
    event.preventDefault();
    if (!validate()) return;

    submitting = true;
    try {
      const payload: CreateEquipmentPayload = {
        name: name.trim(),
        description,
        category: category as EquipmentCategory,
        daily_rental_price: parseFloat(daily_rental_price),
      };
      await onSubmit(payload);
    } finally {
      submitting = false;
    }
  }
</script>

<form on:submit={handleSubmit} novalidate>
  <div class="field">
    <label for="name">Name</label>
    <input id="name" type="text" bind:value={name} />
    {#if nameError}
      <p class="error" role="alert">{nameError}</p>
    {/if}
  </div>

  <div class="field">
    <label for="description">Description</label>
    <textarea id="description" bind:value={description}></textarea>
  </div>

  <div class="field">
    <label for="category">Category</label>
    <select id="category" bind:value={category}>
      <option value="">-- Select a category --</option>
      {#each CATEGORIES as cat}
        <option value={cat}>{cat.replace(/_/g, ' ')}</option>
      {/each}
    </select>
    {#if categoryError}
      <p class="error" role="alert">{categoryError}</p>
    {/if}
  </div>

  <div class="field">
    <label for="price">Daily Rental Price</label>
    <input id="price" type="number" min="0" step="0.01" bind:value={daily_rental_price} />
    {#if priceError}
      <p class="error" role="alert">{priceError}</p>
    {/if}
  </div>

  <button type="submit" disabled={submitting}>
    {submitting ? 'Saving...' : initialValues ? 'Update Equipment' : 'Add Equipment'}
  </button>
</form>

<style>
  .field {
    margin-bottom: 1rem;
    display: flex;
    flex-direction: column;
    gap: 0.25rem;
  }
  .error {
    color: #c0392b;
    font-size: 0.875rem;
    margin: 0;
  }
  input, select, textarea {
    padding: 0.5rem;
    font-size: 1rem;
    border: 1px solid #ccc;
    border-radius: 4px;
  }
  button {
    padding: 0.5rem 1.5rem;
    font-size: 1rem;
    background-color: #2c3e50;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
  }
  button:disabled {
    opacity: 0.6;
    cursor: not-allowed;
  }
</style>
