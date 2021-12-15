from __future__ import annotations

import sys
from typing import List, Union, Any

import uuid

from django.db import models


class User(models.Model):
    """Base users for doctors, patient and staffs."""
    user_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    
    login_name = models.CharField(max_length=50, default='', unique=False)
    
    name = models.CharField(max_length=50, default='')
    
    contact = models.CharField(max_length=50, default='')
    
    bio_gender = models.BooleanField(default=True)
    
    type = models.CharField(max_length=50, default='')
    
    def is_allowed_register(self) -> bool:
        """Check if the user is qualified for appointment registration
        this can be done based on the type attribute.
        """
        return True
    
    @classmethod
    def get_users(cls, user_ids: List[uuid.UUID]) -> List[User]:
        return [
            cls.get_class().get_user(user_id) for user_id in user_ids
        ]
    
    @classmethod
    def get_user(cls, user_id: Union[uuid.UUID, str]) -> User:
        if isinstance(
            user_id,
            uuid.UUID,
        ):
            objects = cls.get_class().objects.filter(
                user_id__exact=user_id
            )
        elif isinstance(
            user_id,
            str,
        ):
            objects = cls.get_class().objects.filter(
                login_name=user_id,
            )
        else:
            raise ValueError(f"Cannot receive user_id {user_id} in type {type(user_id)}!")
        
        if len(objects) == 0:
            raise ValueError(f"Cannot find user with user id {user_id}!")
    
        return objects[0]

    @classmethod
    def get_class(cls) -> Any:
        return getattr(sys.modules[__name__], cls.__name__)

    @classmethod
    def update_attribute(
        cls,
        user: Union[User, uuid.UUID],
        attribute: str,
        value: Any,
    ) -> None:
        if isinstance(
            user,
            uuid.UUID,
        ):
            user = cls.get_user(user)
            
        setattr(user, attribute, value)
        user.save()
        
    @classmethod
    def get_attribute(cls, user: Union[User, uuid.UUID], attribute: str) -> Any:
        if isinstance(
            user,
            uuid.UUID,
        ):
            user = cls.get_user(user)
        
        return getattr(user, attribute)
        
    @classmethod
    def get_name(cls, user: Union[User, uuid.UUID]) -> str:
        return cls.get_attribute(user, "name")

    @classmethod
    def get_type(cls, user: Union[User, uuid.UUID]) -> str:
        return cls.get_attribute(user, "type")

    @classmethod
    def get_contact(cls, user: Union[User, uuid.UUID]) -> str:
        return cls.get_attribute(user, "contact")

    @classmethod
    def get_bio_gender(cls, user: Union[User, uuid.UUID]) -> bool:
        return cls.get_attribute(user, "bio_gender")

    @classmethod
    def update_name(
        cls,
        user: Union[User, uuid.UUID],
        name,
    ):
        cls.update_attribute(
            user,
            "name",
            name,
        )
    
    @classmethod
    def update_contact(
        cls,
        user: Union[User, uuid.UUID],
        contact,
    ):
        cls.update_attribute(
            user,
            "contact",
            contact,
        )
    