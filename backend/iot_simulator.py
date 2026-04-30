import requests
import time
import json
import random

BASE_URL = "http://127.0.0.1:8000/api"

print("="*50)
print("🤖 IoT GATE SIMULATOR (SMART CAMPUS PARKING)")
print("="*50)
print("Simulator ini berfungsi seperti kamera pemindai plat nomor (ALPR)")
print("atau mesin tap kartu RFID di gerbang.")
print("-" * 50)

while True:
    try:
        print("\nOpsi:")
        print("1. Scan Kendaraan (Masuk/Keluar)")
        print("2. Keluar")
        choice = input("Pilih aksi (1/2): ")
        
        if choice == '2':
            break
            
        if choice == '1':
            plat = input("Masukkan Plat Nomor yang terdeteksi kamera: ")
            rfid = input("Masukkan UID RFID (opsional, kosongkan jika tidak ada): ")
            if not rfid:
                rfid = "NO_RFID"
                
            gate_type = input("Gerbang (masuk/keluar): ").lower()
            if gate_type not in ['masuk', 'keluar']:
                print("Gerbang tidak valid.")
                continue
                
            payload = {
                "rfid_uid": rfid,
                "plat_nomor_ml": plat,
                "gate_type": gate_type
            }
            
            print(f"\n📡 Mengirim data ke server: {payload}")
            try:
                response = requests.post(f"{BASE_URL}/gate/scan", json=payload)
                data = response.json()
                
                print("\n[RESPON SERVER]")
                if response.status_code == 200:
                    if data.get("action") == "open_gate":
                        print("✅ AKSES DIIZINKAN. GERBANG TERBUKA.")
                    else:
                        print(f"❌ AKSES DITOLAK. ALASAN: {data.get('message')}")
                else:
                    print(f"⚠️ Error {response.status_code}: {data}")
            except Exception as e:
                print(f"Gagal terhubung ke server: {e}")
                
        time.sleep(1)
    except KeyboardInterrupt:
        break
