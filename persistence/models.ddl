-- Create the Permiso table
CREATE TABLE Permiso (
    id NUMBER PRIMARY KEY,
    clase VARCHAR2(15) NOT NULL,
    nombre VARCHAR2(50) NOT NULL,
    CONSTRAINT Permiso_unique UNIQUE (clase, nombre)
);

-- Create the Rol table
CREATE TABLE Rol (
    id NUMBER PRIMARY KEY,
    nombre VARCHAR2(15) NOT NULL,
    CONSTRAINT Rol_unique UNIQUE (nombre)
);

-- Create the RolPermiso table
CREATE TABLE RolPermiso (
    id NUMBER PRIMARY KEY,
    rol_id NUMBER REFERENCES Rol (id) NOT NULL,
    permiso_id NUMBER REFERENCES Permiso (id) NOT NULL,
    CONSTRAINT RolPermiso_unique UNIQUE (rol_id, permiso_id)
);

-- Create the User table
CREATE TABLE "User" (
    id NUMBER PRIMARY KEY,
    username VARCHAR2(30) NOT NULL,
    name VARCHAR2(20) NOT NULL,
    apellidos VARCHAR2(30) NOT NULL,
    email VARCHAR2(254) UNIQUE NOT NULL,
    is_staff NUMBER(1,0) DEFAULT 0 NOT NULL,
    is_active NUMBER(1,0) DEFAULT 1 NOT NULL,
    date_joined TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    roles_id NUMBER REFERENCES Rol (id) NOT NULL
);

-- Create the Cliente table
CREATE TABLE Cliente (
    id NUMBER PRIMARY KEY,
    user_id NUMBER REFERENCES "User" (id) NOT NULL,
    rut VARCHAR2(10) NOT NULL,
    sexo VARCHAR2(10) NOT NULL
);

-- Create the Reserva table
CREATE TABLE Reserva (
    id NUMBER PRIMARY KEY,
    cliente_id NUMBER REFERENCES Cliente (id) NOT NULL,
    agenda_id NUMBER REFERENCES Agenda (id) NOT NULL,
    dia DATE NOT NULL,
    estado VARCHAR2(20) DEFAULT 'disponible' NOT NULL,
    CONSTRAINT Reserva_unique UNIQUE (agenda_id, cliente_id, dia)
);

-- Create the Ticket table
CREATE TABLE Ticket (
    id NUMBER PRIMARY KEY,
    cliente_id NUMBER REFERENCES Cliente (id) NOT NULL,
    codigo VARCHAR2(10) NOT NULL,
    fecha_envio TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    reserva_id NUMBER REFERENCES Reserva (id) NOT NULL
);

-- Create the Boleta table
CREATE TABLE Boleta (
    id NUMBER PRIMARY KEY,
    fecha_emision TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    cliente_id NUMBER REFERENCES Cliente (id) NOT NULL,
    reserva_id NUMBER REFERENCES Reserva (id) NOT NULL,
    total NUMBER(10, 2) NOT NULL
);

-- Create the TipoCancha table
CREATE TABLE TipoCancha (
    id NUMBER PRIMARY KEY,
    nombre VARCHAR2(50) NOT NULL,
    precio NUMBER(8, 0) NOT NULL,
    descripcion CLOB
);

-- Create the Cancha table
CREATE TABLE Cancha (
    id NUMBER PRIMARY KEY,
    numeracion VARCHAR2(10) NOT NULL,
    tipo_id NUMBER REFERENCES TipoCancha (id) NOT NULL
);

-- Create the Horario table
CREATE TABLE Horario (
    id NUMBER PRIMARY KEY,
    hora_inicio TIMESTAMP,
    hora_fin TIMESTAMP,
    meridiem VARCHAR2(2) DEFAULT 'PM'
);

-- Create the Agenda table
CREATE TABLE Agenda (
    id NUMBER PRIMARY KEY,
    cancha_id NUMBER REFERENCES Cancha (id) NOT NULL,
    horario_id NUMBER REFERENCES Horario (id) NOT NULL,
    disponible NUMBER(1,0) DEFAULT 1 NOT NULL,
    CONSTRAINT Agenda_unique UNIQUE (cancha_id, horario_id)
);
