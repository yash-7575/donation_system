# Generated migration for adding email validation triggers for NGO and Recipient

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_add_donor_email_validation_trigger'),
    ]

    operations = [
        # NGO email validation trigger
        migrations.RunSQL(
            sql="""
                CREATE TRIGGER validate_ngo_email
                BEFORE INSERT ON api_ngo
                FOR EACH ROW
                BEGIN
                    IF NEW.email NOT LIKE '%@%.%' THEN
                        SIGNAL SQLSTATE '45000' 
                        SET MESSAGE_TEXT = 'Invalid email format. Email must contain @ and domain.';
                    END IF;
                END
            """,
            reverse_sql="DROP TRIGGER IF EXISTS validate_ngo_email;"
        ),
        
        # Recipient email validation trigger
        migrations.RunSQL(
            sql="""
                CREATE TRIGGER validate_recipient_email
                BEFORE INSERT ON api_recipient
                FOR EACH ROW
                BEGIN
                    IF NEW.email NOT LIKE '%@%.%' THEN
                        SIGNAL SQLSTATE '45000' 
                        SET MESSAGE_TEXT = 'Invalid email format. Email must contain @ and domain.';
                    END IF;
                END
            """,
            reverse_sql="DROP TRIGGER IF EXISTS validate_recipient_email;"
        ),
        
        # Update triggers for existing records
        migrations.RunSQL(
            sql="""
                CREATE TRIGGER validate_donor_email_update
                BEFORE UPDATE ON api_donor
                FOR EACH ROW
                BEGIN
                    IF NEW.email NOT LIKE '%@%.%' THEN
                        SIGNAL SQLSTATE '45000' 
                        SET MESSAGE_TEXT = 'Invalid email format. Email must contain @ and domain.';
                    END IF;
                END
            """,
            reverse_sql="DROP TRIGGER IF EXISTS validate_donor_email_update;"
        ),
        
        migrations.RunSQL(
            sql="""
                CREATE TRIGGER validate_ngo_email_update
                BEFORE UPDATE ON api_ngo
                FOR EACH ROW
                BEGIN
                    IF NEW.email NOT LIKE '%@%.%' THEN
                        SIGNAL SQLSTATE '45000' 
                        SET MESSAGE_TEXT = 'Invalid email format. Email must contain @ and domain.';
                    END IF;
                END
            """,
            reverse_sql="DROP TRIGGER IF EXISTS validate_ngo_email_update;"
        ),
        
        migrations.RunSQL(
            sql="""
                CREATE TRIGGER validate_recipient_email_update
                BEFORE UPDATE ON api_recipient
                FOR EACH ROW
                BEGIN
                    IF NEW.email NOT LIKE '%@%.%' THEN
                        SIGNAL SQLSTATE '45000' 
                        SET MESSAGE_TEXT = 'Invalid email format. Email must contain @ and domain.';
                    END IF;
                END
            """,
            reverse_sql="DROP TRIGGER IF EXISTS validate_recipient_email_update;"
        ),
    ]