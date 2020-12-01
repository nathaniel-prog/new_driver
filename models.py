from django.db import models
from django.contrib.auth.models import User
from datetime import date
from twilio.rest import Client
from twilio.twiml.voice_response import VoiceResponse, Say

import phonenumbers
import phonenumber_field
from django.conf import settings
from django.core import validators
from phonenumbers.util import unicod
from phonenumber_field.modelfields import PhoneNumberField









class Post(models.Model):
    titre= models.CharField(max_length=150,default='it was nice', null=True)
    author= models.ForeignKey(User,on_delete=models.CASCADE)
    body= models.TextField(default='whats in your mind ')
    other= models.CharField(max_length=225, default='yes')









class Chauffeur(models.Model):
    name= models.CharField(max_length=125 , null=False)
    date_of_birth=models.DateField(default=date.today())
    date_inscription=models.DateField(default=date.today())

    num_phone=PhoneNumberField(unique=True , null=True , default='+972')
    car= models.CharField(max_length=255 ,default='Regular car', null=False)
    car_image = models.ImageField(default='hotelsample.jpg', upload_to='images/', null=True)



    def __str__(self):
        return str(self.name)

    def save(self , *args , **kwargs):
        if self.name and self.num_phone:
            account_sid = 'AC0bfa41e3d8d3f121949b600d9b3d5831'
            auth_token = 'd06b042acf3776f1c57bf14278b8dbde'
            client = Client(account_sid, auth_token)

            message = client.messages.create(
                body=f'mnt  {self.name} je vais coder',
                from_='+12543312099',
                to=f'{self.num_phone}',

            )
            print(message.sid)

        return super().save(*args, **kwargs)


class Score(models.Model):
    result= models.PositiveIntegerField()

    def __str__(self):
        return str(self.result)

    def save(self, *args, **kwargs):
        if self.result:
            self.result+=5
            account_sid = 'AC0bfa41e3d8d3f121949b600d9b3d5831'
            auth_token = 'd06b042acf3776f1c57bf14278b8dbde'
            client = Client(account_sid, auth_token)

            message = client.messages.create(
                body=f' {self.result } minutes , ne bouger pas ',
                from_='+12543312099',
                to='+972585230351'
        )
            print(message.sid)

        return super().save(*args,**kwargs)



class PhoneNumber(phonenumbers.PhoneNumber):
    """
    A extended version of phonenumbers.PhoneNumber that provides
    some neat and more pythonic, easy to access methods. This makes using a
    PhoneNumber instance much easier, especially in templates and such.
    """

    format_map = {
        "E164": phonenumbers.PhoneNumberFormat.E164,
        "INTERNATIONAL": phonenumbers.PhoneNumberFormat.INTERNATIONAL,
        "NATIONAL": phonenumbers.PhoneNumberFormat.NATIONAL,
        "RFC3966": phonenumbers.PhoneNumberFormat.RFC3966,
    }

    @classmethod
    def from_string(cls, phone_number, region=None):
        phone_number_obj = cls()
        if region is None:
            region = getattr(settings, "PHONENUMBER_DEFAULT_REGION", None)
        phonenumbers.parse(
            number=phone_number,
            region=region,
            keep_raw_input=True,
            numobj=phone_number_obj,
        )
        return phone_number_obj

    def __str__(self):
        if self.is_valid():
            format_string = getattr(settings, "PHONENUMBER_DEFAULT_FORMAT", "E164")
            fmt = self.format_map[format_string]
            return self.format_as(fmt)
        else:
            return self.raw_input

    def __repr__(self):
        if not self.is_valid():
            return unicod(
                "Invalid{}(raw_input={})".format(type(self).__name__, self.raw_input)
            )
        return super().__repr__()

    def is_valid(self):
        """
        checks whether the number supplied is actually valid
        """
        return phonenumbers.is_valid_number(self)

    def format_as(self, format):
        return phonenumbers.format_number(self, format)

    @property
    def as_international(self):
        return self.format_as(phonenumbers.PhoneNumberFormat.INTERNATIONAL)

    @property
    def as_e164(self):
        return self.format_as(phonenumbers.PhoneNumberFormat.E164)

    @property
    def as_national(self):
        return self.format_as(phonenumbers.PhoneNumberFormat.NATIONAL)

    @property
    def as_rfc3966(self):
        return self.format_as(phonenumbers.PhoneNumberFormat.RFC3966)

    def __len__(self):
        return len(str(self))

    def __eq__(self, other):
        """
        Override parent equality because we store only string representation
        of phone number, so we must compare only this string representation
        """
        if other in validators.EMPTY_VALUES:
            return False
        elif isinstance(other, str):
            default_region = getattr(settings, "PHONENUMBER_DEFAULT_REGION", None)
            other = to_python(other, region=default_region)
        elif isinstance(other, self.__class__):
            # Nothing to do. Good to compare.
            pass
        elif isinstance(other, phonenumbers.PhoneNumber):
            # The parent class of PhoneNumber does not have .is_valid().
            # We need to make it match ours.
            old_other = other
            other = self.__class__()
            other.merge_from(old_other)
        else:
            return False

        format_string = getattr(settings, "PHONENUMBER_DB_FORMAT", "E164")
        fmt = self.format_map[format_string]
        self_str = self.format_as(fmt) if self.is_valid() else self.raw_input
        other_str = other.format_as(fmt) if other.is_valid() else other.raw_input
        return self_str == other_str

    def __hash__(self):
        return hash(str(self))


def to_python(value, region=None):
    if value in validators.EMPTY_VALUES:  # None or ''
        phone_number = value
    elif isinstance(value, str):
        try:
            phone_number = PhoneNumber.from_string(phone_number=value, region=region)
        except phonenumbers.NumberParseException:
            # the string provided is not a valid PhoneNumber.
            phone_number = PhoneNumber(raw_input=value)
    elif isinstance(value, PhoneNumber):
        phone_number = value
    elif isinstance(value, phonenumbers.PhoneNumber):
        phone_number = PhoneNumber()
        phone_number.merge_from(value)
    else:
        raise TypeError("Can't convert %s to PhoneNumber." % type(value).__name__)
    return phone_number


def validate_region(region):
    if (
        region is not None
        and region not in phonenumbers.shortdata._AVAILABLE_REGION_CODES
    ):
        raise ValueError(
            "“%s” is not a valid region code. Choices are %r"
            % (region, phonenumbers.shortdata._AVAILABLE_REGION_CODES)
        )






