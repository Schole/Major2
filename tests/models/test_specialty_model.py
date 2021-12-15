from django.test import TestCase

from health_appointment.models.specialty_model import (
    Specialty,
    SpecialtyCategory,
    create_specialty_category,
    create_specialty,
)


class TestSpecialtyModel(TestCase):
    def test_specialty_default_setting(self) -> None:
        specialty = Specialty.objects.create()
        self.assertEqual(
            specialty.specialty_id,
            -1,
        )
        
        self.assertEqual(
            specialty.name,
            "",
        )
        
        self.assertEqual(
            specialty.specialty_category,
            -1,
        )
    
    def test_specialty_setting(self) -> None:
        specialty = Specialty.objects.create(
            specialty_id=1,
            name='test_specialty',
            specialty_category=123,
        )
        
        self.assertEqual(
            specialty.specialty_id,
            1,
        )
        
        self.assertEqual(
            specialty.name,
            "test_specialty",
        )
        
        self.assertEqual(
            specialty.specialty_category,
            123,
        )
        
    def test_create_specialty(self) -> None:
        create_specialty()


class TestSpecialtyCategoryModel(TestCase):
    def test_specialty_category_default_setting(self) -> None:
        specialty_category = SpecialtyCategory.objects.create()
        self.assertEqual(
            specialty_category.specialty_category_id,
            -1,
        )
        
        self.assertEqual(
            specialty_category.name,
            "",
        )
        
        self.assertEqual(
            specialty_category.illness_category,
            "",
        )

        self.assertEqual(
            specialty_category.specialties,
            "",
        )
        
    def test_specialty_category_setting(self) -> None:
        specialty_category = SpecialtyCategory.objects.create(
            specialty_category_id=1,
            name='test_specialty',
            illness_category="test_category",
            specialties='test_specialties'
        )
        
        self.assertEqual(
            specialty_category.specialty_category_id,
            1,
        )
        
        self.assertEqual(
            specialty_category.name,
            "test_specialty",
        )
        
        self.assertEqual(
            specialty_category.illness_category,
            "test_category",
        )

        self.assertEqual(
            specialty_category.specialties,
            "test_specialties",
        )
        
    def test_create_specialty_category(self) -> None:
        create_specialty_category()