from django.db.models import Q

from ..models.illness_model import IllnessCategory


def find_specialty_category(category: int) -> int:
    illness_category = IllnessCategory.objects.filter(
        Q(illness_category_id__exact=category)
    )
    
    if len(illness_category) != 1:
        raise ValueError(f"Cannot find illness category for category {category}!")
    
    illness_category = illness_category[0]
    
    specialty_category = illness_category.specialty_category
    return specialty_category