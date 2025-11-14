
-- Update feedback
UPDATE core_feedback
SET rating = 5, comment = 'Updated comment'
WHERE feedback_id = 12 AND user_id = 3;

-- Delete feedback
DELETE FROM core_feedback
WHERE feedback_id = 12 AND user_id = 3;