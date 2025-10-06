from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_final_email_validation_triggers'),
    ]

    operations = [
        migrations.RunSQL(
            """
            DROP PROCEDURE IF EXISTS SubmitDonation;
            
            CREATE PROCEDURE SubmitDonation(
                IN p_donor_id INT,
                IN p_title VARCHAR(255),
                IN p_description TEXT,
                IN p_category VARCHAR(50),
                IN p_quantity INT,
                IN p_city VARCHAR(100),
                IN p_image_url VARCHAR(255)
            )
            BEGIN
                DECLARE v_ngo_id INT;
                
                START TRANSACTION;
                    -- Auto-assign NGO based on donor's city
                    SELECT ngo_id INTO v_ngo_id
                    FROM api_ngo
                    WHERE city = p_city
                    ORDER BY ngo_id
                    LIMIT 1;
                    
                    -- Insert donation
                    INSERT INTO api_donation (donor_id, ngo_id, title, description, category, quantity, status, image_url, created_at)
                    VALUES (p_donor_id, v_ngo_id, p_title, p_description, p_category, p_quantity, 'pending', p_image_url, NOW());
                COMMIT;
            END
            """,
            reverse_sql="DROP PROCEDURE IF EXISTS SubmitDonation;"
        ),
    ]