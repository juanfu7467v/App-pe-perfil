CREATE TABLE IF NOT EXISTS perfiles (
    id SERIAL PRIMARY KEY,
    numero_whatsapp TEXT UNIQUE NOT NULL,
    nombre TEXT,
    genero TEXT,
    edad INTEGER,
    descripcion TEXT
);
