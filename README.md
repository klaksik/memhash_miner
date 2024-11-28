
# Memhash Miner — Python Miner for Linux

**Memhash Miner** is a lightweight and easy-to-use mining solution written in Python, designed specifically for Linux. With simple setup and minimal dependencies, it is an ideal choice for both beginners and experienced users.


---

## Recommended Hosting

We recommend using [Aeza.net](https://aeza.net/?ref=522069) — a reliable hosting platform for your mining tasks.

---

## Features
- Fully optimized for Linux.
- Quick and straightforward installation.
- Easy configuration through a single file.
- Seamless integration with popular hosting platforms.

---

## Installation and Setup
1.
   install python3.10
  Ubuntu:
  ```bash
   sudo apt update
   sudo apt install -y software-properties-common
   sudo add-apt-repository -y ppa:deadsnakes/ppa
   sudo apt update
   sudo apt install -y python3.10 python3.10-venv python3.10-distutils
   apt install python3-pip
  ``` 
2.
   install Chrome
  Ubuntu:
  ```bash
  # Установить зависимости
   sudo apt-get install -y libxss1 libappindicator1 libindicator7

   # Скачиваем Google Chrome
   wget https://dl.google.com/linux/chrome/deb/pool/main/g/google-chrome-stable/google-chrome-stable_131.0.6778.85-1_amd64.deb
   sudo apt install ./google-chrome-stable_131.0.6778.85-1_amd64.deb

   sudo apt-get install -f
  ```
4. Clone the repository and install dependencies:
   ```bash
   git clone https://github.com/klaksik/memhash_miner.git
   cd memhash_miner
   pip3 install -r requirements.txt
   ```

5. Configure the URL:
   - Open the web.telegram.org website, and open memhash.
     
     ![image](https://github.com/user-attachments/assets/ead90574-dcef-49db-8a36-faae099812d6)
     
     ![image](https://github.com/user-attachments/assets/b66d7683-f1a3-4425-92f5-7fdbc1a63ee6)
   - Press `F12` to open Developer Tools.
   - Navigate to the **Elements** tab.
     
     ![image](https://github.com/user-attachments/assets/34f8ea10-4f18-4ab7-bd41-89e3c5e3845b)
   - Select the element picker tool and click on the **Memhash** window.
     
     ![image](https://github.com/user-attachments/assets/aaa12d6d-2efc-4318-b17e-6b2c9f472671)
     
     ![image](https://github.com/user-attachments/assets/cd84aaff-95b9-4145-9cf5-e56ff9389a52)
     
     ![image](https://github.com/user-attachments/assets/8360ce65-bfad-4a65-a1e3-819cbff70da1)
   - Copy the URL of the selected element and paste it into `main.py`:

6. Configure the Telegram bot:
   - go to https://t.me/BotFather
   - create bot and paste token into script
   
7. Run the miner:
   ```bash
   python3 main.py
   ```


## Screenshots

### Selecting the Memhash Window
![Selecting the Memhash Window](https://github.com/user-attachments/assets/aaa12d6d-2efc-4318-b17e-6b2c9f472671)

### Configuration Example
![Configuration Example](https://github.com/user-attachments/assets/8360ce65-bfad-4a65-a1e3-819cbff70da1)

---

## License

This project is distributed under the **MIT License**. Feel free to use, modify, and share.

---

## Contact

For inquiries and suggestions:
- Telegram: [@Klaksiks](https://t.me/Klaksiks)

---

Thank you for using Memhash Miner!
