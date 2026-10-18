CREATE DATABASE IF NOT EXISTS inventario_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE inventario_db;

CREATE TABLE IF NOT EXISTS categorias (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL UNIQUE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS productos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    categoria_id INT NULL,
    nombre VARCHAR(150) NOT NULL,
    descripcion TEXT,
    precio DECIMAL(10, 2) NOT NULL DEFAULT 0.00,
    cantidad INT NOT NULL DEFAULT 0,
    CONSTRAINT fk_productos_categorias FOREIGN KEY (categoria_id) 
        REFERENCES categorias(id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Datos iniciales de prueba
INSERT IGNORE INTO categorias (id, nombre) VALUES 
(1, 'Electrónica'), (2, 'Periféricos'), (3, 'Consumibles');

INSERT INTO productos (nombre, descripcion, precio, cantidad, categoria_id) VALUES
('Teclado Mecánico RGB', 'Teclado switch blue', 45000.00, 12, 2),
('Monitor 24" 144Hz', 'Pantalla IPS Full HD', 185000.00, 3, 1),
('Mouse Inalámbrico', 'Sensor óptico 1600 DPI', 18000.00, 0, 2);