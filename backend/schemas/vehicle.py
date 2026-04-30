from pydantic import BaseModel
from typing import Optional
from models import VehicleTypeEnum, ValidationStatusEnum

class VehicleBase(BaseModel):
    jenis_kendaraan: VehicleTypeEnum
    plat_nomor: str
    merek: Optional[str] = None
    foto_stnk: Optional[str] = None

class VehicleCreate(VehicleBase):
    pass

class VehicleResponse(VehicleBase):
    id: int
    user_id: int
    status_validasi: ValidationStatusEnum

    class Config:
        from_attributes = True
