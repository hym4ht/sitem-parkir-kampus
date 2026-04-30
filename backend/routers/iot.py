from fastapi import APIRouter, Depends, HTTPException, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session
import asyncio
from core.security import get_petugas

import models
from schemas.parking import GateScanRequest, GateScanResponse
from database import get_db

router = APIRouter(prefix="/api/gate", tags=["IoT Integrations & WebSockets"])

# ConnectionManager manages a pool of WebSockets connected from the Petugas Live Monitor
class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def broadcast(self, message: dict):
        for connection in list(self.active_connections):
            try:
                await connection.send_json(message)
            except Exception:
                self.disconnect(connection)

manager = ConnectionManager()

# ── Petugas notification channel ────────────────────────────
class PetugasNotificationManager:
    """Separate WebSocket channel for real-time notifications to petugas."""
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def notify_new_request(self, data: dict):
        """Broadcast new access request notification to all connected petugas."""
        for connection in list(self.active_connections):
            try:
                await connection.send_json({
                    "type": "new_access_request",
                    **data
                })
            except Exception:
                self.disconnect(connection)

petugas_notifier = PetugasNotificationManager()

@router.websocket("/monitor/live")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            if data == "ping":
                await websocket.send_text("pong")
    except WebSocketDisconnect:
        manager.disconnect(websocket)

@router.websocket("/petugas/notifications")
async def petugas_notification_ws(websocket: WebSocket):
    """WebSocket endpoint for petugas real-time notifications."""
    await petugas_notifier.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            if data == "ping":
                await websocket.send_text("pong")
    except WebSocketDisconnect:
        petugas_notifier.disconnect(websocket)

@router.post("/scan", response_model=GateScanResponse)
async def process_gate_scan(scan: GateScanRequest, db: Session = Depends(get_db)):
    # 1. Find User by RFID tag read
    rfid_card = db.query(models.RFIDCard).filter(models.RFIDCard.rfid_uid == scan.rfid_uid).first()
    
    if not rfid_card:
        await manager.broadcast({
            "type": "error",
            "message": "Unregistered RFID card scanned.",
            "rfid": scan.rfid_uid,
            "plate": scan.plat_nomor_ml
        })
        return {"action": "keep_closed", "message": "RFID not found"}

    user = rfid_card.user
    
    # 2. Check if scanned plate matches an APPROVED vehicle belonging to this user
    target_vehicle = None
    for vehicle in user.vehicles:
        if vehicle.plat_nomor == scan.plat_nomor_ml and vehicle.status_validasi == models.ValidationStatusEnum.disetujui:
            target_vehicle = vehicle
            break
            
    if not target_vehicle:
        await manager.broadcast({
            "type": "error",
            "message": f"Kendaraan {scan.plat_nomor_ml} tidak sesuai atau belum disetujui.",
            "user": user.nama,
            "plate": scan.plat_nomor_ml
        })
        return {"action": "keep_closed", "message": "Vehicle not approved or mismatch"}
        
    # 3. Validated: Create Parking Log entry
    log = models.ParkingLog(
        user_id=user.id,
        vehicle_id=target_vehicle.id,
        jenis_aktivitas=scan.gate_type,
        status_akses=models.AccessStatusEnum.otomatis
    )
    db.add(log)
    db.commit()
    db.refresh(log)
    
    # 4. Broadcast success log to the Live Monitor Socket for petugas dashboard
    await manager.broadcast({
        "type": "success",
        "message": f"Akses {scan.gate_type} diizinkan otomatis.",
        "user": user.nama,
        "plate": target_vehicle.plat_nomor,
        "time": log.waktu.isoformat()
    })
    
    return {"action": "open_gate", "message": "Access granted"}

@router.post("/emergency-action")
async def emergency_gate_action(gate: str, reason: str, db: Session = Depends(get_db), current_user: models.User = Depends(get_petugas)):
    """Petugas manual override to open gate in emergency."""
    if gate not in ["masuk", "keluar"]:
        raise HTTPException(status_code=400, detail="Gate must be 'masuk' or 'keluar'")
        
    # Broadcast to live monitor so it shows up in logs
    await manager.broadcast({
        "type": "error", # Highlight as yellow/warning in UI
        "message": f"🚨 EMERGENCY OVERRIDE ({gate.upper()})",
        "user": current_user.nama,
        "plate": "MANUAL",
        "remark": reason
    })
    
    # Log it as manual_petugas activity
    # Note: We don't have a specific vehicle/user for emergency, 
    # we'll link it to the PETUGAS themselves as user_id for logging.
    new_log = models.ParkingLog(
        user_id=current_user.id,
        vehicle_id=1, # Dummy or generic ID for emergency
        jenis_aktivitas=gate,
        status_akses=models.AccessStatusEnum.manual_petugas
    )
    db.add(new_log)
    db.commit()
    
    return {"status": "success", "message": f"Gate {gate} dibuka manual"}

@router.get("/stats/capacity")
def get_parking_capacity(db: Session = Depends(get_db)):
    """Calculate current parking occupancy."""
    total_capacity = 100 # Default
    
    # Simple occupancy: Entered - Exited
    entered = db.query(models.ParkingLog).filter(models.ParkingLog.jenis_aktivitas == models.ActivityTypeEnum.masuk).count()
    exited = db.query(models.ParkingLog).filter(models.ParkingLog.jenis_aktivitas == models.ActivityTypeEnum.keluar).count()
    
    parked_count = max(0, entered - exited)
    
    return {
        "total": total_capacity,
        "parked": parked_count,
        "available": max(0, total_capacity - parked_count)
    }
