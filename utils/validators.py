from settings.database import user_collection, organisation_collection, permissions_collection
from bson.objectid import ObjectId
from dto.permissions import AccessLevelEnum
from .types import CustomException
from typing import List
from fastapi import HTTPException
import re

email_pattern = r"^[\w\.\+\-]+\@[\w]+\.[a-z]{2,3}$"

class Validator:
    def is_valid_email(self, value):
        if not re.match(email_pattern, value):
            raise HTTPException(status_code=400, detail="Invalid email address")
        return value
    
    def is_duplicate_email(email: str) -> bool:
        user = user_collection.find_one({"email": email})
        if user:
            raise CustomException(status_code=400, detail="Email address already exists")
        
    def is_duplicate_org(name: str) -> bool:
        organisation = organisation_collection.find_one({"name": name})
        if organisation:
            raise CustomException(status_code=400, detail="Organisation already exists")

    def check_org(org_id: str) -> dict:
        org = organisation_collection.find_one({"_id": ObjectId(org_id)})
        if not org:
            raise CustomException(status_code=404, detail="Organization not found")
        return org
    
    def check_user(user_id: str) -> dict:
        user = user_collection.find_one({"_id": ObjectId(user_id)})
        print(user)
        if not user:
            raise CustomException(status_code=404, detail="User not found")
        return user


    def check_users(user_ids: List[str]) -> dict:
        users = {}
        for user_id in user_ids:
            user = user_collection.find_one({"_id": ObjectId(user_id)})
            if not user:
                raise CustomException(status_code=404, detail=f"User {user_id} not found")
            users[user_id] = user
        return users


    def check_access_level(access_level: AccessLevelEnum) -> None:
        if access_level not in [AccessLevelEnum.READ, AccessLevelEnum.WRITE, AccessLevelEnum.ADMIN]:
            raise CustomException(status_code=400, detail="Invalid access level")

