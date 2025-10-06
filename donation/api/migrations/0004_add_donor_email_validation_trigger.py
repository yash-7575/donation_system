# Generated migration for adding donor email validation trigger

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_ngo_password_recipient_password_alter_donor_password'),
    ]

    operations = [
        migrations.RunSQL(
            # Forward migration - Create the trigger
            sql="""
                CREATE TRIGGER validate_donor_email
                BEFORE INSERT ON api_donor
                FOR EACH ROW
                BEGIN
                    IF NEW.email NOT LIKE '%@%.%' THEN
                        SIGNAL SQLSTATE '45000' 
                        SET MESSAGE_TEXT = 'Invalid email format. Email must contain @ and domain.';
                    END IF;
                END
            """,
            # Reverse migration - Drop the trigger
            reverse_sql="DROP TRIGGER IF EXISTS validate_donor_email;"
        ),
    ]