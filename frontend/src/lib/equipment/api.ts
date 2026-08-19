import type {
  Equipment,
  CreateEquipmentPayload,
  UpdateEquipmentPayload,
} from './types';

const BASE_URL = 'http://localhost:8000';

async function handleResponse<T>(response: Response): Promise<T> {
  if (!response.ok) {
    let detail = `HTTP error ${response.status}`;
    try {
      const body = await response.json();
      if (body.detail) detail = body.detail;
    } catch {
      // ignore JSON parse failure
    }
    throw new Error(detail);
  }
  return response.json() as Promise<T>;
}

export async function listEquipment(): Promise<Equipment[]> {
  const response = await fetch(`${BASE_URL}/equipment`);
  return handleResponse<Equipment[]>(response);
}

export async function getEquipment(id: string): Promise<Equipment> {
  const response = await fetch(`${BASE_URL}/equipment/${id}`);
  return handleResponse<Equipment>(response);
}

export async function createEquipment(payload: CreateEquipmentPayload): Promise<Equipment> {
  const response = await fetch(`${BASE_URL}/equipment`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  });
  return handleResponse<Equipment>(response);
}

export async function updateEquipment(id: string, payload: UpdateEquipmentPayload): Promise<Equipment> {
  const response = await fetch(`${BASE_URL}/equipment/${id}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  });
  return handleResponse<Equipment>(response);
}

export async function toggleEquipmentStatus(id: string): Promise<Equipment> {
  const response = await fetch(`${BASE_URL}/equipment/${id}/toggle-status`, {
    method: 'PATCH',
  });
  return handleResponse<Equipment>(response);
}

export async function deleteEquipment(id: string): Promise<void> {
  const response = await fetch(`${BASE_URL}/equipment/${id}`, {
    method: 'DELETE',
  });
  if (!response.ok) {
    let detail = `HTTP error ${response.status}`;
    try {
      const body = await response.json();
      if (body.detail) detail = body.detail;
    } catch { /* ignore */ }
    throw new Error(detail);
  }
}
