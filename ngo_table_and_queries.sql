-- NGO Table and Related Queries
-- This file contains only the NGO table creation and queries specifically related to the NGO dashboard

-- 1. Create NGO table
CREATE TABLE api_ngo (
    ngo_id INT AUTO_INCREMENT PRIMARY KEY,
    ngo_name VARCHAR(200),
    email VARCHAR(254) UNIQUE,
    phone VARCHAR(20),
    website VARCHAR(254),
    address TEXT,
    city VARCHAR(100),
    state VARCHAR(100),
    pincode VARCHAR(12),
    password VARCHAR(128)
);

-- 2. Email Validation Triggers for NGO table

-- Trigger for validating NGO email on insert
CREATE TRIGGER validate_ngo_email
BEFORE INSERT ON api_ngo
FOR EACH ROW
BEGIN
    IF NEW.email NOT LIKE '%@%.%' OR 
       NEW.email LIKE '@%' OR 
       NEW.email LIKE '%@' OR
       NEW.email LIKE '.@%' OR
       NEW.email LIKE '%@.' OR
       CHAR_LENGTH(NEW.email) < 5 THEN
        SIGNAL SQLSTATE '45000' 
        SET MESSAGE_TEXT = 'Invalid email format. Email must contain @ and domain.';
    END IF;
END;

-- Trigger for validating NGO email on update
CREATE TRIGGER validate_ngo_email_update
BEFORE UPDATE ON api_ngo
FOR EACH ROW
BEGIN
    IF NEW.email NOT LIKE '%@%.%' OR 
       NEW.email LIKE '@%' OR 
       NEW.email LIKE '%@' OR
       NEW.email LIKE '.@%' OR
       NEW.email LIKE '%@.' OR
       CHAR_LENGTH(NEW.email) < 5 THEN
        SIGNAL SQLSTATE '45000' 
        SET MESSAGE_TEXT = 'Invalid email format. Email must contain @ and domain.';
    END IF;
END;

-- 3. Queries for NGO Dashboard

-- Query 1: Overall Statistics for NGO Dashboard
SELECT 
    (SELECT COUNT(*) FROM api_donation d JOIN api_ngo n ON d.ngo_id = n.ngo_id WHERE n.ngo_id = ?) AS total_donations,
    (SELECT COUNT(*) FROM api_recipient) AS total_requests,
    (SELECT COUNT(*) FROM api_donation d JOIN api_ngo n ON d.ngo_id = n.ngo_id WHERE n.ngo_id = ? AND d.status = 'delivered') AS successful_matches,
    (SELECT COUNT(DISTINCT d.donor_id) FROM api_donation d JOIN api_ngo n ON d.ngo_id = n.ngo_id WHERE n.ngo_id = ? AND d.status = 'delivered') AS families_helped;

-- Query 2: Pending Donations for NGO
SELECT 
    d.donation_id,
    d.title,
    d.category,
    d.quantity,
    d.created_at,
    dr.name AS donor_name,
    dr.city AS donor_city
FROM api_donation d
JOIN api_donor dr ON d.donor_id = dr.donor_id
WHERE d.ngo_id = ? AND d.status = 'pending'
ORDER BY d.created_at DESC
LIMIT 10;

-- Query 3: Pending Requests for NGO
SELECT 
    r.recipient_id,
    r.name AS recipient_name,
    r.family_size,
    r.urgency,
    r.city,
    r.state
FROM api_recipient r
WHERE r.recipient_id IN (
    SELECT DISTINCT recipient_id 
    FROM api_donation 
    WHERE ngo_id = ? AND status = 'pending'
)
ORDER BY r.urgency DESC, r.family_size DESC
LIMIT 10;

-- Query 4: Available Donations for Matching
SELECT 
    d.donation_id,
    d.title,
    d.category,
    d.quantity,
    d.created_at,
    dr.name AS donor_name,
    dr.city AS donor_city
FROM api_donation d
JOIN api_donor dr ON d.donor_id = dr.donor_id
WHERE d.ngo_id = ? AND d.status = 'pending'
ORDER BY d.created_at ASC;

-- Query 5: Pending Recipient Requests for Matching
SELECT 
    r.recipient_id,
    r.name AS recipient_name,
    r.family_size,
    r.urgency,
    r.city,
    r.state,
    COUNT(d.donation_id) AS matched_donations
FROM api_recipient r
LEFT JOIN api_donation d ON r.recipient_id = d.donor_id AND d.status != 'pending'
WHERE r.recipient_id NOT IN (
    SELECT DISTINCT donor_id 
    FROM api_donation 
    WHERE ngo_id = ? AND status = 'delivered'
)
GROUP BY r.recipient_id, r.name, r.family_size, r.urgency, r.city, r.state
ORDER BY r.urgency DESC, r.family_size DESC;

-- Query 6: User Management for NGO
SELECT 
    'donor' AS user_type,
    d.donor_id AS user_id,
    d.name AS user_name,
    d.email,
    d.city,
    d.state,
    'Active' AS status,
    d.created_at AS joined_date
FROM api_donor d
JOIN api_donation don ON d.donor_id = don.donor_id
WHERE don.ngo_id = ?
UNION ALL
SELECT 
    'recipient' AS user_type,
    r.recipient_id AS user_id,
    r.name AS user_name,
    r.email,
    r.city,
    r.state,
    'Active' AS status,
    r.created_at AS joined_date
FROM api_recipient r
WHERE r.recipient_id IN (
    SELECT DISTINCT donor_id 
    FROM api_donation 
    WHERE ngo_id = ?
)
ORDER BY user_type, user_name;

-- Query 7: NGO Profile Information
SELECT 
    ngo_id,
    ngo_name,
    email,
    phone,
    website,
    address,
    city,
    state,
    pincode
FROM api_ngo
WHERE ngo_id = ?;

-- Query 8: Monthly Impact Statistics for NGO
SELECT 
    DATE_FORMAT(d.created_at, '%Y-%m') AS month,
    COUNT(*) AS donations_count,
    SUM(d.quantity) AS items_count,
    COUNT(DISTINCT d.donor_id) AS unique_donors
FROM api_donation d
WHERE d.ngo_id = ? AND d.status = 'delivered'
    AND d.created_at >= DATE_SUB(NOW(), INTERVAL 12 MONTH)
GROUP BY DATE_FORMAT(d.created_at, '%Y-%m')
ORDER BY month DESC;