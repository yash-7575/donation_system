-- Total Donors
SELECT COUNT(DISTINCT donor_id) AS total_donors FROM donors;

-- Total Recipients
SELECT COUNT(DISTINCT recipient_id) AS total_recipients FROM recipients;

-- Total Donations
SELECT COUNT(*) AS total_donations FROM donations;

-- Average Rating (rounded to two decimals)
SELECT ROUND(AVG(rating), 2) AS average_rating FROM donations WHERE rating IS NOT NULL;

-- Total Items Donated
SELECT SUM(quantity) AS items_donated FROM donation_items;

-- Delivered Donations
SELECT COUNT(*) AS delivered_donations FROM donations WHERE status = 'Delivered';

-- Pending Donations
SELECT COUNT(*) AS pending_donations FROM donations WHERE status = 'Pending';

-- Donations By City (Top Cities)
SELECT city, COUNT(*) AS donations
FROM donations
GROUP BY city
ORDER BY donations DESC
LIMIT 5;

-- Donations By Category
SELECT category, COUNT(*) AS count
FROM donation_items
GROUP BY category
ORDER BY count DESC;
