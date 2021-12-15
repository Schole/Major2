from django.test import TestCase

from health_appointment.models.illness_model import (
    Illness,
    get_illness_name,
    create_illnesses,
)


class TestIllnessModel(TestCase):
    def test_illness_default_setting(self) -> None:
        illness = Illness.objects.create()
        self.assertEqual(
            illness.illness_id,
            -1,
        )
        
        self.assertEqual(
            illness.name,
            "",
        )

        self.assertEqual(
            illness.illness_category,
            -1,
        )

    def test_illness_setting(self) -> None:
        
        illness = Illness.objects.create(
            illness_id=1,
            name='test_illness',
            illness_category=123,
        )
        
        self.assertEqual(
            illness.illness_id,
            1,
        )
    
        self.assertEqual(
            illness.name,
            "test_illness",
        )

    def test_get_illness_name(self) -> None:
        Illness.objects.create(
            illness_id=123,
            name='test_illness',
        )
        
        self.assertEqual(
            get_illness_name(
                123,
            ),
            "test_illness"
        )
        
    def test_create_illness(self) -> None:
        create_illnesses()