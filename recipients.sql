-
--- AGGREGATE FUNCTION ---

SELECT
    COUNT(*) AS total_requests,
    SUM(CASE WHEN status = 'pending' THEN 1 ELSE 0 END) AS pending_requests,
    SUM(CASE WHEN status = 'accepted' THEN 1 ELSE 0 END) AS fulfilled_requests
FROM core_request
WHERE recipient_id = <RECIPIENT_ID>;

-- WHERE CLAUSE -- 
SELECT 
    id,
    title,
    description,
    category,
    urgency,
    status,
    created_at
FROM core_request
WHERE recipient_id = <RECIPIENT_ID>
  AND category = 'Books';
  
  
--- Procedure to insert the request data ---
DELIMITER $$

CREATE PROCEDURE CreateRequest(
    IN p_title VARCHAR(255),
    IN p_description TEXT,
    IN p_category VARCHAR(100),
    IN p_urgency VARCHAR(20),
    IN p_status VARCHAR(20),
    IN p_recipient_id BIGINT
)
BEGIN
    INSERT INTO core_request (title, description, category, urgency, status, created_at, recipient_id)
    VALUES (p_title, p_description, p_category, p_urgency, p_status, NOW(), p_recipient_id);
END $$

DELIMITER ;

CALL CreateRequest(
    'Need Clothes',
    'Winter clothes needed for kids',
    'Clothes',
    'medium',
    'pending',
    12
);



--- UPDATE A REQUEST ---
 UPDATE core_request
SET 
    title = 'Updated Title',
    description = 'Updated description here',
    category = 'Food',
    urgency = 'high',
    status = 'pending'
WHERE id = 5 AND recipient_id = 12;


--- DELETE REQUEST --- 
DELETE FROM core_request
WHERE id = 5 AND recipient_id = 12;




--  JOINS QUERIES ---
-- Example 1: INNER JOIN - Recipient Dashboard (Show all requests)
SELECT 
    r.id,
    r.title,
    r.category,
    r.urgency,
    r.status,
    recipient.name,
    recipient.family_size
FROM core_request r
INNER JOIN core_recipient recipient ON r.recipient_id = recipient.id
WHERE recipient.id = 1;


-- Example 2: LEFT JOIN - Show requests and available donations
SELECT 
    r.id,
    r.title,
    d.donation_id,
    d.title AS donation_title,
    d.quantity
FROM core_request r
LEFT JOIN core_donation d ON d.category = r.category AND d.status = 'pending'
WHERE r.recipient_id = 1;


-- Example 3: SELF JOIN - Find requests from other recipients in same city
SELECT 
    r1.id AS my_request_id,
    r1.title AS my_request,
    r2.id AS other_request_id,
    r2.title AS other_request,
    rec2.name AS other_recipient
FROM core_request r1
INNER JOIN core_recipient rec1 ON r1.recipient_id = rec1.id
INNER JOIN core_recipient rec2 ON rec1.city = rec2.city AND rec1.id != rec2.id
INNER JOIN core_request r2 ON rec2.id = r2.recipient_id
WHERE rec1.id = 1;


-- Example 4: EQUI JOIN - Get requests with donors and donations
SELECT 
    r.id,
    r.title,
    donor.name AS donor_name,
    d.title AS donation_title
FROM core_request r, core_recipient recipient, core_donation d, core_donor donor
WHERE r.recipient_id = recipient.id
  AND d.category = r.category
  AND d.donor_id = donor.id
  AND recipient.id = 1;


