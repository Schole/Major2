from django.db import models


class Illness(models.Model):
    illness_id = models.IntegerField(
        default=-1
    )
    name = models.CharField(max_length=50, default='')
    illness_category = models.IntegerField(
        default=-1
    )
    """illness_category; IntegerField, contains an id of the illness category that it belongs to."""


class IllnessCategory(models.Model):
    illness_category_id = models.IntegerField(
        default=-1
    )
    name = models.CharField(max_length=50, default='')
    illness = models.CharField(default='', max_length=1600)
    """illness; CharField, contains a 'list' of the ids of illnesses that the category contains."""
    specialty_category = models.IntegerField(
        default=-1
    )
    """specialty_category; IntegerField, contains an id of the specialty category that it belongs to."""


def create_illness_category():
    indexes = [1, 2, 3]
    names = [
        "illness_category_1",
        "illness_category_2",
        "illness_category_3",
    ]
    illnesses = [
        ",".join(["1",
         "2",
         "3"]),
        ",".join(["4",
         "5"]),
        ",".join(["6",
         "7",
         "8"]),
    ]
    specialty_categories = [1, 2, 2]
    for name, index, illness, specialty_category in zip(names, indexes, illnesses, specialty_categories):
        IllnessCategory.objects.create(
            illness_category_id=index,
            name=name,
            illness=illness,
            specialty_category=specialty_category,
        )


def create_illnesses():
    from health_appointment.models.model_illness import Illness

    indexes = [1, 2, 3, 4, 5, 6, 7, 8]
    names = [
        "illness_1",
        "illness_2",
        "illness_3",
        "illness_4",
        "illness_5",
        "illness_6",
        "illness_7",
        "illness_8",
    ]
    illness_categories = [1, 1, 1, 2, 2, 3, 3, 3]
    for name, index, illness_category in zip(names, indexes, illness_categories):
        Illness.objects.create(
            illness_id=index,
            name=name,
            illness_category=illness_category,
        )
    print("created!")
    # Bar.objects.all().delete()