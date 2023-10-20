from datetime import datetime

from mongoengine import Document, StringField, EmailField, DateTimeField
from flask_bcrypt import generate_password_hash

from config import Config

class User(Document):
    registered_date = DateTimeField(default=datetime.now)

    first_name = StringField(required=True, regex="^[a-zA-Z \-]+$", max_length=20)

    last_name = StringField(required=True, regex="^[a-zA-Z \-]+$", max_length=20)

    email = EmailField(unique=True, required=True, max_length=50)
    
    # length: 8-25 characters
    # At least 1 uppercase letter
    # At least 1 lowercase letter
    # At least 1 number
    # At least 1 special character
    password = StringField(required=True, regex="^(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9])(?=.*[@#$%^&+=]).{8,25}$", min_length=10)

    # USER ROLES:
    #   regular - no event creation allowed
    #   organization - event creation allowed
    role = StringField(required=True, default="regular")

    meta = {
        'db_alias': Config.MONGODB_SETTINGS['alias'],
        'collection': 'users'
    }

    def save(self, *args, **kwargs):
        self.password = generate_password_hash(password=self.password).decode("utf-8")
        self.validate_email()
        super().save(args, kwargs)

    def validate(self, *args, **kwargs):
        self.validate_email()
        super().validate()

    def validate_email(self):
         # validate email properly
        email_valid = False
        email_domain = self.email.rsplit("@", 1)
        if len(email_domain) != 2:
            raise  Exception(f"'{self.email}' not a valid email (email validation failed)")
        email_domain_part = email_domain[-1].lower()
        for domain in Config.DOMAIN_WHITELIST:  
            if domain == email_domain_part:
                email_valid = True
                break
        if email_valid == False:
            raise Exception(f"'{email_domain_part}' not a valid domain (email validation failed)")
        return email_valid