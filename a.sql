CREATE DATABASE givehope_core;
USE givehope_core;

CREATE TABLE auth_user (
    id INT AUTO_INCREMENT PRIMARY KEY,
    password VARCHAR(128) NOT NULL,
    last_login DATETIME NULL,
    is_superuser BOOLEAN NOT NULL DEFAULT 0,
    username VARCHAR(150) UNIQUE NOT NULL,
    first_name VARCHAR(150) NOT NULL,
    last_name VARCHAR(150) NOT NULL,
    email VARCHAR(254) NOT NULL,
    is_staff BOOLEAN NOT NULL DEFAULT 0,
    is_active BOOLEAN NOT NULL DEFAULT 1,
    date_joined DATETIME NOT NULL
);

CREATE TABLE core_userprofile (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    role VARCHAR(20) CHECK (role IN ('donor', 'ngo', 'recipient')),
    FOREIGN KEY (user_id) REFERENCES auth_user(id) ON DELETE CASCADE
);

CREATE TABLE core_donor (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT UNIQUE,
    name VARCHAR(150),
    phone VARCHAR(20),
    address TEXT,
    city VARCHAR(100),
    state VARCHAR(100),
    pincode VARCHAR(12),
    FOREIGN KEY (user_id) REFERENCES auth_user(id) ON DELETE CASCADE
);

CREATE TABLE core_ngo (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT UNIQUE,
    ngo_name VARCHAR(200),
    phone VARCHAR(20),
    website VARCHAR(255),
    address TEXT,
    city VARCHAR(100),
    state VARCHAR(100),
    pincode VARCHAR(12),
    FOREIGN KEY (user_id) REFERENCES auth_user(id) ON DELETE CASCADE
);

CREATE TABLE core_recipient (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT UNIQUE,
    name VARCHAR(150),
    phone VARCHAR(20),
    family_size INT DEFAULT 1,
    urgency VARCHAR(20) DEFAULT 'medium',
    address TEXT,
    city VARCHAR(100),
    state VARCHAR(100),
    pincode VARCHAR(12),
    FOREIGN KEY (user_id) REFERENCES auth_user(id) ON DELETE CASCADE
);

CREATE TABLE core_donation (
    donation_id INT AUTO_INCREMENT PRIMARY KEY,
    donor_id INT NOT NULL,
    ngo_id INT NULL,
    title VARCHAR(200),
    description TEXT,
    category VARCHAR(50),
    quantity INT DEFAULT 1,
    status VARCHAR(30) DEFAULT 'pending',
    image_url VARCHAR(500),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (donor_id) REFERENCES core_donor(id) ON DELETE CASCADE,
    FOREIGN KEY (ngo_id) REFERENCES core_ngo(id) ON DELETE SET NULL
);

CREATE TABLE core_feedback (
    feedback_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    match_id INT NULL,
    rating INT CHECK (rating BETWEEN 1 AND 5),
    comment TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE core_request (
    id INT AUTO_INCREMENT PRIMARY KEY,
    recipient_id INT NOT NULL,
    title VARCHAR(255),
    description TEXT,
    category VARCHAR(50),
    urgency VARCHAR(20) DEFAULT 'medium',
    status VARCHAR(20) DEFAULT 'open',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (recipient_id) REFERENCES core_recipient(id) ON DELETE CASCADE
);

CREATE TABLE core_match (
    id INT AUTO_INCREMENT PRIMARY KEY,
    donation_id INT NOT NULL,
    request_id INT NOT NULL,
    ngo_id INT NOT NULL,
    status VARCHAR(20) DEFAULT 'matched',   -- matched / delivered / cancelled
    matched_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    delivered_at DATETIME NULL,
    FOREIGN KEY (donation_id) REFERENCES core_donation(donation_id) ON DELETE CASCADE,
    FOREIGN KEY (request_id) REFERENCES core_request(id) ON DELETE CASCADE,
    FOREIGN KEY (ngo_id) REFERENCES core_ngo(id) ON DELETE CASCADE
);

INSERT INTO core_request (recipient_id, title, description, category, urgency)
VALUES (3, 'Warm Blankets', 'Need warm blankets for kids', 'Clothing', 'high');

INSERT INTO core_donation (donor_id, title, description, category, quantity, status)
VALUES (2, 'Winter Jackets', 'Set of jackets in good condition', 'Clothing', 5, 'pending');
