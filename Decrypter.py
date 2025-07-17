import cryptography
import cryptography.fernet
import platform
import GPUtil
import os
import sys
import threading
import time
from pathlib import Path

def masaustu_yolu() -> str:
    masaustu = Path.home() / "Desktop"
    if masaustu.exists():
        return masaustu
    else:
        return None

def dosya_decrypt(klasor_yolu: str, key: bytes) -> list:
    file_list = []
    dosyaklasor_list = os.walk(klasor_yolu)
    for root, dirs, files in dosyaklasor_list:
        for file in files:
            if file == "Decrypter.py":
                continue
            full_path = os.path.join(root, file)
            file_list.append(full_path)

    i = 0
    while i < len(file_list):
        try:
            with open(file_list[i], 'rb') as okunan_dosya:
                icerik = okunan_dosya.read()
            cozulmus_icerik = cryptography.fernet.Fernet(key).decrypt(icerik)
            with open(file_list[i], 'wb') as yazilan_dosya:
                yazilan_dosya.write(cozulmus_icerik)
            time.sleep(0.3)
            print("[*] Dosya çözüldü! : {}".format(file_list[i]))

        except Exception as err:
            print(f"[!] Hata oluştu {file_list[i]}: {err}")
            continue
        finally:
            i = i + 1

def gpname() -> str:
    gpus = GPUtil.getGPUs()
    for gpu in gpus:
        return gpu.name

if __name__ == '__main__':
    if platform.system().lower() == "windows": os.system("cls")
    else: os.system("clear")
  
    platform.gpname = gpname
  
    print(f"[^] OS : {platform.system()}")
    print(f"[^] CPU : {platform.processor()}")
    print(f"[^] GPU : {platform.gpname()}")
    key = input("[-] Anahtarı Giriniz: ").encode("utf-8")
    print("\n########################################################################")
    
    suanki_klasor = os.getcwd()
    yol = masaustu_yolu()
    thread_1: threading.Thread
    
    if yol is not None:
        thread_1 = threading.Thread(target=dosya_decrypt, args=(yol, key,))
        
    else:
        thread_1 = threading.Thread(target=dosya_decrypt, args=(suanki_klasor, key,))

    thread_1.daemon = False
    thread_1.start()
    thread_1.join()

    print("İşlem sona erdi.")

    sys.exit(0)
