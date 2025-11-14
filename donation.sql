-- -------------------------------------------------------
-- Database: givehope_core
-- Purpose: Procedures, Joins, Aggregates, Triggers, Views for Donation Management
-- Author: (Add your name/date if needed)
-- -------------------------------------------------------

-- USE THE CORRECT DATABASE
USE givehope_core;

-- -------------------------------------------------------
-- 1. STORED PROCEDURES
-- -------------------------------------------------------

-- Insert new donation into core_donation, default status pending
DELIMITER $$
CREATE PROCEDURE InsertDonation (
    IN p_donor_id BIGINT,
    IN p_ngo_id BIGINT,
    IN p_title VARCHAR(255),
    IN p_description TEXT,
    IN p_category VARCHAR(100),
    IN p_quantity INT,
    IN p_image_url VARCHAR(255)
)
BEGIN
    INSERT INTO core_donation (
        donor_id, ngo_id, title, description, category, quantity, image_url, status
    ) VALUES (
        p_donor_id, p_ngo_id, p_title, p_description, p_category, p_quantity, p_image_url, 'pending'
    );
END$$

-- Update the status of a donation by id
CREATE PROCEDURE UpdateDonationStatus (
    IN p_donation_id BIGINT,
    IN p_status VARCHAR(20)
)
BEGIN
    UPDATE core_donation
    SET status = p_status
    WHERE id = p_donation_id;
END$$

-- Delete a donation by id
CREATE PROCEDURE DeleteDonation (
    IN p_donation_id BIGINT
)
BEGIN
    DELETE FROM core_donation
    WHERE id = p_donation_id;
END$$
DELIMITER ;

-- -------------------------------------------------------
-- 2. JOINS
-- -------------------------------------------------------

-- (A) Donor + Donation: Show donation details with donor info
-- Columns: donation_id, title, status, donor_name, phone, city
SELECT d.id AS donation_id, d.title, d.status,
       dr.name AS donor_name, dr.phone, dr.city
FROM core_donation d
INNER JOIN core_donor dr ON d.donor_id = dr.id;

-- (B) Donations + NGO (LEFT JOIN): Donations with assigned NGO (if any)
SELECT d.id AS donation_id, d.title, d.status,
       n.ngo_name, n.city, n.phone
FROM core_donation d
LEFT JOIN core_ngo n ON d.ngo_id = n.id;

-- (C) Donor + Donation + NGO: Complete donation assignments with donor & NGO (if any)
SELECT d.id AS donation_id, d.title, d.category, d.status,
       dr.name AS donor_name,
       n.ngo_name AS assigned_ngo
FROM core_donation d
INNER JOIN core_donor dr ON d.donor_id = dr.id
LEFT JOIN core_ngo n ON d.ngo_id = n.id;

-- -------------------------------------------------------
-- 3. AGGREGATE FUNCTIONS
-- -------------------------------------------------------

-- 1. Total donations for each donor
SELECT 
    d.donor_id,
    dr.name AS donor_name,
    COUNT(*) AS total_donations
FROM core_donation d
JOIN core_donor dr ON d.donor_id = dr.id
GROUP BY d.donor_id, dr.name;

-- 2. Donations count by category
SELECT category, COUNT(*) AS total_items
FROM core_donation
GROUP BY category;

-- 3. Total quantity donated by each donor
SELECT 
    dr.name AS donor_name,
    SUM(d.quantity) AS total_quantity
FROM core_donation d
JOIN core_donor dr ON d.donor_id = dr.id
GROUP BY dr.name;

-- 4. Number of donations by status
SELECT status, COUNT(*) AS total
FROM core_donation
GROUP BY status;

-- 5. Total delivered quantity (status = 'accepted')
SELECT SUM(quantity) AS total_accepted_quantity
FROM core_donation
WHERE status = 'accepted';

-- -------------------------------------------------------
-- 4. TRIGGERS
-- -------------------------------------------------------

-- Log table to record donation status changes
CREATE TABLE IF NOT EXISTS DonationLog (
    log_id INT AUTO_INCREMENT PRIMARY KEY,
    donation_id BIGINT,
    old_status VARCHAR(20),
    new_status VARCHAR(20),
    changed_at DATETIME
);

-- Trigger 1: Log when status changes on core_donation
DELIMITER $$
CREATE TRIGGER LogDonationStatusChange
AFTER UPDATE ON core_donation
FOR EACH ROW
BEGIN
    IF OLD.status <> NEW.status THEN
        INSERT INTO DonationLog (donation_id, old_status, new_status, changed_at)
        VALUES (OLD.id, OLD.status, NEW.status, NOW());
    END IF;
END$$

-- Trigger 2: Reset status to pending if ngo_id is removed
CREATE TRIGGER ResetStatusWhenNGORemoved
BEFORE UPDATE ON core_donation
FOR EACH ROW
BEGIN
    IF NEW.ngo_id IS NULL AND OLD.ngo_id IS NOT NULL THEN
        SET NEW.status = 'pending';
    END IF;
END$$

-- Trigger 3: Auto-set created_at before insert into core_donation (if null)
CREATE TRIGGER SetCreatedAtBeforeInsert
BEFORE INSERT ON core_donation
FOR EACH ROW
BEGIN
    IF NEW.created_at IS NULL THEN
        SET NEW.created_at = NOW();
    END IF;
END$$
DELIMITER ;

-- -------------------------------------------------------
-- 5. VIEWS
-- -------------------------------------------------------

-- View 1: Donation summary with donor names
CREATE OR REPLACE VIEW vw_donation_summary AS
SELECT
    d.id AS donation_id,
    d.title,
    d.category,
    d.quantity,
    d.status,
    d.created_at,
    dr.name AS donor_name
FROM core_donation d
INNER JOIN core_donor dr ON d.donor_id = dr.id;

-- View 2: Donations with donor and assigned NGO if any
CREATE OR REPLACE VIEW vw_donation_ngo AS
SELECT
    d.id AS donation_id,
    d.title,
    d.category,
    d.status,
    dr.name AS donor_name,
    n.ngo_name,
    d.created_at
FROM core_donation d
INNER JOIN core_donor dr ON d.donor_id = dr.id
LEFT JOIN core_ngo n ON d.ngo_id = n.id;

-- View 3: Number of donations by category
CREATE OR REPLACE VIEW vw_donation_by_category AS
SELECT
    category,
    COUNT(*) AS total_donations
FROM core_donation
GROUP BY category;

-- View 4: Pending donations (latest first)
CREATE OR REPLACE VIEW vw_pending_donations AS
SELECT
    id AS donation_id,
    title,
    category,
    quantity,
    donor_id,
    created_at
FROM core_donation
WHERE status = 'pending'
ORDER BY created_at DESC;

-- where clause (filter)
SELECT 
    title,
    category,
    quantity,
    status,
    created_at
FROM core_donation
WHERE donor_id = 2 AND category = 'Clothing';

-- -------------------------------------------------------
-- END OF FILE
-- -------------------------------------------------------
