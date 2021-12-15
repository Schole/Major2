from django.db import models


class Specialty(models.Model):
    specialty_id = models.IntegerField(
        default=-1
    )
    name = models.CharField(max_length=50, default='')
    specialty_category = models.IntegerField(default=-1)
    """illness_category; CharField, contains the id of the specialty category it belongs to."""


class SpecialtyCategory(models.Model):
    specialty_category_id = models.IntegerField(
        default=-1
    )
    name = models.CharField(max_length=50, default='')
    illness_category = models.CharField(max_length=1600, default='')
    """illness_category; CharField, contains a 'list' of the ids of illness category
    that the specialty category contains."""
    specialties = models.CharField(max_length=1600, default='')
    """specialties; CharField, contains a 'list' of the ids of specialties that the category contains."""

    @staticmethod
    def get_illness_category(illness_category):
        return [int(x) for x in illness_category.split(',')]

def create_specialty_category():
    indexes = [1, 2, 3]
    names = [
        "specialty_category_1",
        "specialty_category_2",
        "specialty_category_3",
    ]
    illness_categories = ['1,2', '3', '4']
    specialties = [
        ",".join(
            [
                "1",
                "2",
                "3"
            ]
        ),
        ",".join(
            [
                "4",
                "5"
            ]
        ),
        "6",
        ",".join(
            [
                "7",
                "8"
            ]
        ),
    ]
    for name, index, illness_category, specialty in zip(names, indexes, illness_categories, specialties):
        SpecialtyCategory.objects.create(
            specialty_category_id=index,
            name=name,
            illness_category=illness_category,
            specialties=specialty,
        )

def create_specialty():
    indexes = [1, 2, 3, 4, 5, 6, 7, 8]
    names = [
        "specialty_1",
        "specialty_2",
        "specialty_3",
        "specialty_4",
        "specialty_5",
        "specialty_6",
        "specialty_7",
        "specialty_8",
    ]
    specialty_categories = ['1', '1', '1', '2', '2', '3', '4', '4']
    for name, index, specialty_category in zip(names, indexes, specialty_categories):
        Specialty.objects.create(
            specialty_id=index,
            name=name,
            specialty_category=specialty_category,
        )