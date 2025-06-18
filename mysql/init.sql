
SET NAMES utf8mb4;
SET CHARACTER SET utf8mb4;
USE webapp;

CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
TRUNCATE TABLE users;

INSERT INTO users (name, email) VALUES 
('Иван Иванов', 'ivan@example.com'),
('Мария Петрова', 'maria@example.com'),
('Алексей Сидоров', 'alexey@example.com');
DESCRIBE users;

SELECT id, name, email, created_at FROM users; 