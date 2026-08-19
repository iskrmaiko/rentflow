CREATE TABLE equipment (
    id                 UUID        PRIMARY KEY DEFAULT gen_random_uuid(),
    name               TEXT        NOT NULL,
    description        TEXT        NOT NULL DEFAULT '',
    category           TEXT        NOT NULL,
    daily_rental_price NUMERIC(12,2) NOT NULL CHECK (daily_rental_price >= 0),
    status             TEXT        NOT NULL DEFAULT 'ACTIVE',
    created_at         TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at         TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
