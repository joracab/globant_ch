CREATE DATABASE globant_challenge;
USE globant_challenge;

-- Tabla de departamentos
CREATE TABLE departments (
    id INT PRIMARY KEY,
    department VARCHAR(255) NOT NULL
);

-- Tabla de trabajos
CREATE TABLE jobs (
    id INT PRIMARY KEY,
    job VARCHAR(255) NOT NULL
);

-- Tabla de empleados contratados
CREATE TABLE hired_employees (
    id INT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    datetime DATETIME NOT NULL,
    department_id INT NOT NULL,
    job_id INT NOT NULL,
    FOREIGN KEY (department_id) REFERENCES departments(id),
    FOREIGN KEY (job_id) REFERENCES jobs(id)
);

-- Índices para mejorar la consulta
CREATE INDEX idx_hired_employees_datetime ON hired_employees(datetime);
CREATE INDEX idx_hired_employees_department ON hired_employees(department_id);
CREATE INDEX idx_hired_employees_job ON hired_employees(job_id);