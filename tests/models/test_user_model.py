import uuid
from django.test import TestCase

from health_appointment.models.doctor_model import (
    User
)


class TestUserModel(TestCase):
    def setUp(self) -> None:
        self.user_id = uuid.uuid4()
        self.name = "test_name"
        self.contact = "Rutgers University"
        self.bio_gender = False
        self.type = "doctor"
    
        self.user = User.objects.create(
            user_id=self.user_id,
            name=self.name,
            contact=self.contact,
            bio_gender=self.bio_gender,
            type=self.type,
        )
        
    def test_user_default_setting(self) -> None:
        user = User.objects.create()
        
        self.assertEqual(
            user.bio_gender,
            True,
        )
        
        self.assertEqual(
            user.name,
            '',
        )
        
        self.assertEqual(
            user.contact,
            '',
        )
        
        self.assertEqual(
            user.type,
            '',
        )
    
    def test_user_setting(self) -> None:
        user_id = uuid.uuid4()
        name = "test_name"
        contact = "Rutgers University"
        bio_gender = False
        type = "doctor"
        
        user = User.objects.create(
            user_id=user_id,
            name=name,
            contact=contact,
            bio_gender=bio_gender,
            type=type,
        )
        
        self.assertEqual(
            user.user_id,
            user_id,
        )
        
        self.assertEqual(
            user.name,
            name,
        )
        
        self.assertEqual(
            user.contact,
            contact
        )
        
        self.assertEqual(
            user.bio_gender,
            bio_gender,
        )
        
        self.assertEqual(
            user.type,
            type
        )

    def test_get_name(self) -> None:
        self.assertEqual(
            self.name,
            User.get_name(
                self.user,
            ),
        )

        self.assertEqual(
            self.name,
            User.get_name(
                self.user.user_id,
            ),
        )
        
    def test_get_contact(self) -> None:
        self.assertEqual(
            self.contact,
            User.get_contact(
                self.user,
            ),
        )

        self.assertEqual(
            self.contact,
            User.get_contact(
                self.user.user_id,
            ),
        )
        
    def test_get_bio_gender(self) -> None:
        self.assertEqual(
            self.bio_gender,
            User.get_bio_gender(
                self.user,
            ),
        )

        self.assertEqual(
            self.bio_gender,
            User.get_bio_gender(
                self.user.user_id,
            ),
        )

    def test_update_name(self) -> None:
        user = User.objects.create()
        User.update_name(
            user,
            "updated_name"
        ),
    
        self.assertEqual(
            user.name,
            "updated_name",
        )

    def test_update_contact(self) -> None:
        user = User.objects.create()
        User.update_contact(
            user,
            "updated_contact"
        ),
    
        self.assertEqual(
            user.contact,
            "updated_contact",
        )
        
    def test_is_allowed_register(self) -> None:
        self.assertEqual(
            User.objects.create().is_allowed_register(),
            True
        )