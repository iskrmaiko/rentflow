export type EquipmentCategory =
  | 'POWER_TOOLS'
  | 'HAND_TOOLS'
  | 'CONSTRUCTION'
  | 'LANDSCAPING'
  | 'LIGHTING'
  | 'AUDIO_VISUAL'
  | 'CLEANING'
  | 'SAFETY'
  | 'TRANSPORTATION'
  | 'OTHER';

export type EquipmentStatus = 'ACTIVE' | 'INACTIVE';

export interface Equipment {
  id: string;
  name: string;
  description: string;
  category: EquipmentCategory;
  daily_rental_price: number;
  status: EquipmentStatus;
}

export interface CreateEquipmentPayload {
  name: string;
  description: string;
  category: EquipmentCategory;
  daily_rental_price: number;
}

export type UpdateEquipmentPayload = CreateEquipmentPayload;
