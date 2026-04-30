from pydantic import BaseModel
from typing import Optional
from models import RoleEnum

class UserBase(BaseModel):
    nim_npp: str
    nama: str
    prodi_id: Optional[int] = None
    angkatan: Optional[int] = None
    rfid_uid: Optional[str] = None
    role: RoleEnum

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    nim_npp: Optional[str] = None
    nama: Optional[str] = None
    prodi_id: Optional[int] = None
    angkatan: Optional[int] = None
    rfid_uid: Optional[str] = None
    role: Optional[RoleEnum] = None
    password: Optional[str] = None

class UserResponse(UserBase):
    id: int
    prodi_nama: Optional[str] = None
    semester: Optional[int] = None

    @classmethod
    def from_orm(cls, obj):
        # Custom logic for prodi_nama and semester
        res = super().from_orm(obj)
        if obj.prodi:
            res.prodi_nama = obj.prodi.nama
        
        if obj.angkatan:
            from datetime import datetime
            now = datetime.now()
            # Simplistic 2 sem/year logic starting from Sept
            months = (now.year - obj.angkatan) * 12 + (now.month - 9)
            res.semester = max(1, (months // 6) + 1)
        return res

    class Config:
        from_attributes = True

class ProdiBase(BaseModel):
    nama: str

class ProdiCreate(ProdiBase):
    pass

class ProdiResponse(ProdiBase):
    id: int
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str
    role: RoleEnum
    nama: str
    nim_npp: str

class TokenData(BaseModel):
    nim_npp: Optional[str] = None

class UserProfile(BaseModel):
    id: int
    nim_npp: str
    nama: str
    role: RoleEnum
    is_flagged: bool
    flag_reason: Optional[str] = None
    prodi_nama: Optional[str] = None
    semester: Optional[int] = None

    @classmethod
    def from_orm(cls, obj):
        res = UserProfile(
            id=obj.id,
            nim_npp=obj.nim_npp,
            nama=obj.nama,
            role=obj.role,
            is_flagged=obj.is_flagged,
            flag_reason=obj.flag_reason
        )
        if obj.prodi:
            res.prodi_nama = obj.prodi.nama
        
        if obj.angkatan:
            from datetime import datetime
            now = datetime.now()
            months = (now.year - obj.angkatan) * 12 + (now.month - 9)
            res.semester = max(1, (months // 6) + 1)
        return res
