from pydantic import BaseModel
from datetime import datetime
from models import ActivityTypeEnum, AccessStatusEnum

class ParkingLogResponse(BaseModel):
    id: int
    user_id: int
    vehicle_id: int
    waktu: datetime
    jenis_aktivitas: ActivityTypeEnum
    status_akses: AccessStatusEnum

    class Config:
        from_attributes = True

class GateScanRequest(BaseModel):
    rfid_uid: str
    plat_nomor_ml: str
    gate_type: ActivityTypeEnum # 'masuk' or 'keluar'

class GateScanResponse(BaseModel):
    action: str # 'open_gate' or 'keep_closed'
    message: str
