# Alke Wallet - Database & Backend System


# Descripción del Proyecto:

Alke Wallet es una solución de base de datos relacional diseñada para simular el núcleo de una billetera virtual. Este proyecto fue desarrollado como parte de una Evaluación Integradora, enfocándose en la integridad de los datos, la seguridad transaccional y la manipulación eficiente de información financiera.

El sistema permite la gestión de usuarios, el manejo de múltiples divisas y el registro histórico de transacciones, asegurando el cumplimiento de las propiedades ACID (Atomicidad, Consistencia, Aislamiento y Durabilidad).

# Características Principales:

Gestión de Usuarios: Registro, autenticación y manejo de saldos individuales.

Transacciones Seguras: Registro de envíos y recepciones de dinero entre usuarios.

Soporte Multimoneda: Capacidad para operar con diferentes divisas (USD, EUR, CLP, etc.).

Integración con Python: Scripts automatizados para conectar la base de datos y ejecutar operaciones CRUD.

Consultas Avanzadas: Uso de JOINS, subconsultas y funciones de agregación para reportes financieros.

# Tecnologías Utilizadas:

Motor de Base de Datos: MySQL / MariaDB

Lenguaje de Consultas: SQL (DDL, DML)

Lenguaje de Programación: Python 3.x

Librerías: mysql-connector-python

Herramientas: Visual Studio Code, SQLTools / MySQL Workbench

# Estructura de la Base de Datos (ERD)

El modelo de datos sigue las reglas de normalización (3FN) y consta de tres entidades principales:

Usuario: Almacena la información personal y el saldo actual.

Moneda: Catálogo de divisas disponibles en la plataforma.

Transaccion: Tabla central que registra los movimientos financieros, relacionando al emisor y receptor con una moneda específica.

Nota: Puedes visualizar el diagrama entidad-relación en el archivo diagrama_ER.pdf o en la carpeta /docs.

El proyecto incluye consultas optimizadas para la toma de decisiones:

Obtener historial de un usuario:

SQL
SELECT * FROM Transaccion WHERE sender_user_id = 1;
Verificar monedas utilizadas:

SQL
SELECT DISTINCT m.currency_name 
FROM Transaccion t
JOIN Moneda m ON t.currency_id = m.currency_id;



# erDiagram

    %% Entidades y Atributos
    USUARIO {
        int user_id PK "Identificador único"
        string nombre "Nombre completo"
        string correo_electronico "Email único"
        string contrasena "Password encriptada"
        decimal saldo "Dinero actual"
        datetime fecha_creacion "Fecha registro"
    }

    MONEDA {
        int currency_id PK "Identificador moneda"
        string currency_name "Ej: Dolar"
        string currency_symbol "Ej: USD"
    }

    TRANSACCION {
        int transaction_id PK "Identificador único"
        int sender_user_id FK "Quién envía"
        int receiver_user_id FK "Quién recibe"
        decimal importe "Monto transferido"
        datetime transaction_date "Fecha y hora"
        int currency_id FK "Moneda usada"
    }

    %% Relaciones y Cardinalidades
    %% Un Usuario puede enviar 0 o muchas (o{) transacciones
     USUARIO ||--o{ TRANSACCION : "envía"
    
    %% Un Usuario puede recibir 0 o muchas (o{) transacciones
    USUARIO ||--o{ TRANSACCION : "recibe"

    %% Una Moneda puede ser usada en 0 o muchas (o{) transacciones
    MONEDA ||--o{ TRANSACCION : "utilizada en"

    
