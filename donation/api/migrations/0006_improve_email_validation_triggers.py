# Generated migration to improve email validation trigger logic

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_add_all_email_validation_triggers'),
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
        
        # Create improved triggers with better validation
        # Donor INSERT trigger
        migrations.RunSQL(
            sql="""
                CREATE TRIGGER validate_donor_email
                BEFORE INSERT ON api_donor
                FOR EACH ROW
                BEGIN
                    IF NEW.email NOT REGEXP '^[a-zA-Z0-9][a-zA-Z0-9._-]*@[a-zA-Z0-9][a-zA-Z0-9.-]*\\.[a-zA-Z]{2,}$' THEN
                        SIGNAL SQLSTATE '45000' 
                        SET MESSAGE_TEXT = 'Invalid email format. Email must be in format: user@domain.com';
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
                    IF NEW.email NOT REGEXP '^[a-zA-Z0-9][a-zA-Z0-9._-]*@[a-zA-Z0-9][a-zA-Z0-9.-]*\\.[a-zA-Z]{2,}$' THEN
                        SIGNAL SQLSTATE '45000' 
                        SET MESSAGE_TEXT = 'Invalid email format. Email must be in format: user@domain.com';
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
                    IF NEW.email NOT REGEXP '^[a-zA-Z0-9][a-zA-Z0-9._-]*@[a-zA-Z0-9][a-zA-Z0-9.-]*\\.[a-zA-Z]{2,}$' THEN
                        SIGNAL SQLSTATE '45000' 
                        SET MESSAGE_TEXT = 'Invalid email format. Email must be in format: user@domain.com';
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
                    IF NEW.email NOT REGEXP '^[a-zA-Z0-9][a-zA-Z0-9._-]*@[a-zA-Z0-9][a-zA-Z0-9.-]*\\.[a-zA-Z]{2,}$' THEN
                        SIGNAL SQLSTATE '45000' 
                        SET MESSAGE_TEXT = 'Invalid email format. Email must be in format: user@domain.com';
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
                    IF NEW.email NOT REGEXP '^[a-zA-Z0-9][a-zA-Z0-9._-]*@[a-zA-Z0-9][a-zA-Z0-9.-]*\\.[a-zA-Z]{2,}$' THEN
                        SIGNAL SQLSTATE '45000' 
                        SET MESSAGE_TEXT = 'Invalid email format. Email must be in format: user@domain.com';
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
                    IF NEW.email NOT REGEXP '^[a-zA-Z0-9][a-zA-Z0-9._-]*@[a-zA-Z0-9][a-zA-Z0-9.-]*\\.[a-zA-Z]{2,}$' THEN
                        SIGNAL SQLSTATE '45000' 
                        SET MESSAGE_TEXT = 'Invalid email format. Email must be in format: user@domain.com';
                    END IF;
                END
            """,
            reverse_sql="DROP TRIGGER IF EXISTS validate_recipient_email_update;"
        ),
    ]