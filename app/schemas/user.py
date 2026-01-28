from pydantic import BaseModel


class UserSchema(BaseModel):
    first_name:str
    last_name:str
    username:str
    chat_id:str
    phone_number:str
