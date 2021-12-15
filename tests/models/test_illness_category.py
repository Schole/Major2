from django.test import TestCase

from health_appointment.models.illness_model import (
    IllnessCategory,
    get_illness_category_name,
    create_illness_category
)


class TestIllnessCategoryModel(TestCase):
    def test_illness_category_default_setting(self) -> None:
        illness = IllnessCategory.objects.create()
        self.assertEqual(
            illness.illness_category_id,
            -1,
        )
        
        self.assertEqual(
            illness.name,
            "",
        )
        
        self.assertEqual(
            illness.illness,
            "",
        )
        
        self.assertEqual(
            illness.specialty_category,
            -1,
        )
    
    def test_illness_category_setting(self) -> None:
        illness_category = IllnessCategory.objects.create(
            illness_category_id=1,
            name='test_illness',
            illness=123,
            specialty_category=12345,
        )
        
        self.assertEqual(
            illness_category.illness_category_id,
            1,
        )
        
        self.assertEqual(
            illness_category.name,
            "test_illness",
        )
        
        self.assertEqual(
            illness_category.illness,
            123,
        )
        
        self.assertEqual(
            illness_category.specialty_category,
            12345,
        )
    
    def test_get_illness_category_name(self) -> None:
        IllnessCategory.objects.create(
            illness_category_id=123,
            name='test_illness_category',
        )
        
        self.assertEqual(
            get_illness_category_name(
                123,
            ),
            "test_illness_category"
        )
    
    def test_create_illness_category(self) -> None:
        create_illness_category()