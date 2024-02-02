import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    # Since we're using email as the username, we don't need a separate field for it in the model
    # Ensure email field is unique and required
    email = models.EmailField(unique=True)

    license_code = models.CharField(max_length=255, unique=True, editable=False)
    tokens = models.IntegerField(default=2000)

    # Set the email field as the username field
    USERNAME_FIELD = 'email'

    # Remove email from REQUIRED_FIELDS if it's present (since it's now the USERNAME_FIELD)
    REQUIRED_FIELDS = [
        'username']  # username is kept here just to satisfy the createsuperuser command; adjust as needed

    def charge_tokens(self, token_cost):
        if self.tokens < token_cost:
            return False  # Indicating the user doesn't have enough tokens
        self.tokens -= token_cost
        self.save()
        return True

    def save(self, *args, **kwargs):
        if not self.license_code:
            # Generate a UUID and prepend with 'MM_'
            self.license_code = 'MM_' + str(uuid.uuid4())
        super(User, self).save(*args, **kwargs)
