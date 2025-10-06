# Generated migration with proper email validation triggers

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_improve_email_validation_triggers'),
    ]

    operations = [
        # Drop existing triggers
        migrations.RunSQL(
            sql="DROP TRIGGER IF EXISTS validate_donor_email;",
            reverse_sql=""
        ),
        migrations.RunSQL(
            sql="DROP TRIGGER IF EXISTS validate_ngo_email;",
            reverse_sql=""
        ),
        migrations.RunSQL(
            sql="DROP TRIGGER IF EXISTS validate_recipient_email;",
            reverse_sql=""
        ),
        migrations.RunSQL(
            sql="DROP TRIGGER IF EXISTS validate_donor_email_update;",
            reverse_sql=""
        ),
        migrations.RunSQL(
            sql="DROP TRIGGER IF EXISTS validate_ngo_email_update;",
            reverse_sql=""
        ),
        migrations.RunSQL(
            sql="DROP TRIGGER IF EXISTS validate_recipient_email_update;",
            reverse_sql=""
        ),
        
        # Create final triggers with balanced validation
        # (Based on your original simple but effective approach)
        
        # Donor INSERT trigger
        migrations.RunSQL(
            sql="""
                CREATE TRIGGER validate_donor_email
                BEFORE INSERT ON api_donor
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
                END
            """,
            reverse_sql="DROP TRIGGER IF EXISTS validate_donor_email;"
        ),
        
        # NGO INSERT trigger
        migrations.RunSQL(
            sql="""
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
                END
            """,
            reverse_sql="DROP TRIGGER IF EXISTS validate_ngo_email;"
        ),
        
        # Recipient INSERT trigger
        migrations.RunSQL(
            sql="""
                CREATE TRIGGER validate_recipient_email
                BEFORE INSERT ON api_recipient
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
                END
            """,
            reverse_sql="DROP TRIGGER IF EXISTS validate_recipient_email;"
        ),
        
        # UPDATE triggers
        # Donor UPDATE trigger
        migrations.RunSQL(
            sql="""
                CREATE TRIGGER validate_donor_email_update
                BEFORE UPDATE ON api_donor
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
                END
            """,
            reverse_sql="DROP TRIGGER IF EXISTS validate_donor_email_update;"
        ),
        
        # NGO UPDATE trigger
        migrations.RunSQL(
            sql="""
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
                END
            """,
            reverse_sql="DROP TRIGGER IF EXISTS validate_ngo_email_update;"
        ),
        
        # Recipient UPDATE trigger
        migrations.RunSQL(
            sql="""
                CREATE TRIGGER validate_recipient_email_update
                BEFORE UPDATE ON api_recipient
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
                END
            """,
            reverse_sql="DROP TRIGGER IF EXISTS validate_recipient_email_update;"
        ),
    ]