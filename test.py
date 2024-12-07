import requests
import time
import webbrowser
import threading
import assemblyai as aai

# Causality API credentials
API_KEY = "$2y$10$C.IvXuRfZAGt83YHcDTJH.92nB/InfS4ZfF0H0BIe25jKmzw3A2h6"
API_TOKEN = "XfJhqj07"

# Causality API endpoints
REQUEST_QR_CODE_URL = "https://causality.xyz/api/requestQrCode"
API_STATUS_CHECK_URL = "https://causality.xyz/api/apiStatusCheck"

# AssemblyAI API key
aai.settings.api_key = "db64f091a37e454982cfbff54d76621f"

# Shared state
transcription_active = threading.Event()
full_transcript = []
lock = threading.Lock()  # Prevent overlapping NFC actions

def request_qr_code():
    """
    Request a QR code session for the experience.
    Automatically opens the QR code in a web browser.
    """
    payload = {
        "key": API_KEY,
        "token": API_TOKEN
    }
    
    response = requests.post(REQUEST_QR_CODE_URL, data=payload)
    if response.status_code == 200:
        data = response.json()
        qr_code_url = data['qrCodeLink']
        print(f"QR Code URL: {qr_code_url}")
        webbrowser.open(qr_code_url)  # Automatically open the QR code in a web browser
        return data['qrcode']
    else:
        print("Failed to generate QR code:", response.json())
        return None

def check_status():
    """
    Manage the QR code lifecycle by refreshing it every 30 seconds
    and activating transcription when NFC is scanned.
    """
    while True:
        print("Requesting QR Code...")
        qrcode = request_qr_code()
        if not qrcode:
            print("Failed to create QR code. Retrying...")
            time.sleep(1)
            continue

        payload = {"code": qrcode}
        start_time = time.time()
        timeout = 30  # QR code timeout in seconds

        while time.time() - start_time < timeout:
            response = requests.post(API_STATUS_CHECK_URL, data=payload)
            if response.status_code == 200:
                data = response.json()
                if data.get("message") == "true":
                    nfc_tag = data.get("nfc_tag")
                    product_name = data.get("product_name")
                    print(f"NFC Tag Scanned: {nfc_tag}")
                    print(f"Product Name: {product_name}")
                    with lock:  # Prevent overlapping NFC actions
                        if product_name.lower() == "start recording":
                            print("Start Recording Action Triggered!")
                            transcription_active.set()  # Activate transcription
                        elif product_name.lower() in ["stop recording", "stop recoring"]:
                            print("Stop Recording Action Triggered!")
                            transcription_active.clear()  # Stop transcription
                            return  # Exit the QR code loop
                else:
                    print("Waiting for a valid NFC scan...")
            else:
                print("Error checking status:", response.json())
            time.sleep(5)