-- Creación de la base de datos
CREATE DATABASE AlkeWallet;
USE AlkeWallet;

-- 1. Tabla Usuario
CREATE TABLE Usuario (
    user_id INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(100) NOT NULL,
    correo_electronico VARCHAR(100) NOT NULL UNIQUE,
    contrasena VARCHAR(255) NOT NULL,
    saldo DECIMAL(15, 2) DEFAULT 0.00,
    fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP -- Agregado como Tarea Plus sugerida
);

-- 2. Tabla Moneda
CREATE TABLE Moneda (
    currency_id INT PRIMARY KEY AUTO_INCREMENT,
    currency_name VARCHAR(50) NOT NULL,
    currency_symbol VARCHAR(5) NOT NULL
);

-- 3. Tabla Transaccion
-- Nota: Agregamos currency_id como Foreign Key según la lógica de la Lección 4
CREATE TABLE Transaccion (
    transaction_id INT PRIMARY KEY AUTO_INCREMENT,
    sender_user_id INT,
    receiver_user_id INT,
    importe DECIMAL(15, 2) NOT NULL,
    transaction_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    currency_id INT,

    -- Definición de Claves Foráneas (Foreign Keys)
    CONSTRAINT fk_sender FOREIGN KEY (sender_user_id) REFERENCES Usuario(user_id),
    CONSTRAINT fk_receiver FOREIGN KEY (receiver_user_id) REFERENCES Usuario(user_id),
    CONSTRAINT fk_currency FOREIGN KEY (currency_id) REFERENCES Moneda(currency_id)
);

-- Insertar Monedas
INSERT INTO Moneda (currency_name, currency_symbol) VALUES
('Dolar Estadounidense', 'USD'),
('Euro', 'EUR'),
('Peso Chileno', 'CLP');

-- Insertar Usuarios
INSERT INTO Usuario (nombre, correo_electronico, contrasena, saldo) VALUES
('Juan Perez', 'juan@test.com', 'pass123', 5000.00),
('Maria Garcia', 'maria@test.com', 'pass456', 3500.00),
('Carlos Lopez', 'carlos@test.com', 'pass789', 1000.00);

-- Insertar Transacciones (Juan le envía a Maria, Maria le envía a Carlos)
INSERT INTO Transaccion (sender_user_id, receiver_user_id, importe, transaction_date, currency_id) VALUES
(1, 2, 100.00, NOW(), 1), -- Juan envia 100 USD a Maria
(2, 3, 50.00, NOW(), 1),  -- Maria envia 50 USD a Carlos
(1, 3, 20000.00, NOW(), 3); -- Juan envia 20000 CLP a Carlos

SELECT DISTINCT m.currency_name
FROM Transaccion t
JOIN Moneda m ON t.currency_id = m.currency_id
WHERE t.sender_user_id = 1; -- Cambiar 1 por el ID del usuario deseado

SELECT
    t.transaction_id,
    u1.nombre AS Emisor,
    u2.nombre AS Receptor,
    t.importe,
    m.currency_name,
    t.transaction_date
FROM Transaccion t
JOIN Usuario u1 ON t.sender_user_id = u1.user_id
JOIN Usuario u2 ON t.receiver_user_id = u2.user_id
JOIN Moneda m ON t.currency_id = m.currency_id;

-- Iniciar la transacción
START TRANSACTION;

-- Paso 1: Descontar saldo al usuario que envía (ID 1)
UPDATE Usuario
SET saldo = saldo - 100
WHERE user_id = 1;

-- Paso 2: Aumentar saldo al usuario que recibe (ID 2)
UPDATE Usuario
SET saldo = saldo + 100
WHERE user_id = 2;

-- Paso 3: Registrar la transacción en el historial
INSERT INTO Transaccion (sender_user_id, receiver_user_id, importe, transaction_date, currency_id)
VALUES (1, 2, 100, NOW(), 1);

-- Si todo salió bien, guardamos los cambios
COMMIT;
-- Si hubo un error, se usaría: ROLLBACK;