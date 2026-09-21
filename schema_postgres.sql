-- PostgreSQL Schema for Anndaan (Compatible with Supabase / Neon / Render)

CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    phone TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    role TEXT NOT NULL,               -- donor / ngo
    verified INTEGER DEFAULT 0,       -- 0 = not verified, 1 = verified NGO
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS donations (
    id SERIAL PRIMARY KEY,
    donor_id INTEGER NOT NULL,
    food_item TEXT NOT NULL,
    food_type TEXT NOT NULL,          -- veg / non-veg
    quantity TEXT NOT NULL,           -- e.g. "serves 20"
    pickup_address TEXT NOT NULL,
    expiry_time TEXT NOT NULL,        -- pickup-by, ISO-ish string
    notes TEXT,
    status TEXT NOT NULL DEFAULT 'available',  -- available / claimed / completed / expired
    claimed_by_id INTEGER,
    created_at TEXT NOT NULL,
    claimed_at TEXT,
    expires_at TEXT,                  -- when donation expires
    latitude DOUBLE PRECISION,        -- latitude coordinate
    longitude DOUBLE PRECISION,       -- longitude coordinate
    FOREIGN KEY (donor_id) REFERENCES users (id) ON DELETE CASCADE,
    FOREIGN KEY (claimed_by_id) REFERENCES users (id) ON DELETE SET NULL
);

CREATE INDEX IF NOT EXISTS idx_donations_status ON donations (status);
CREATE INDEX IF NOT EXISTS idx_donations_donor_id ON donations (donor_id);
CREATE INDEX IF NOT EXISTS idx_donations_claimed_by_id ON donations (claimed_by_id);
CREATE INDEX IF NOT EXISTS idx_users_email ON users (email);
