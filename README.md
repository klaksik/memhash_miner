
# Memhash Miner — Python Miner for Linux or Windows

**Memhash Miner** is a lightweight and easy-to-use mining solution written in Python, designed specifically for Linux. With simple setup and minimal dependencies, it is an ideal choice for both beginners and experienced users.


---

## Recommended Hosting

We recommend using [Aeza.net](https://aeza.net/?ref=522069) — a reliable hosting platform for your mining tasks.

---

## [Donate](https://donatello.to/Klaksik)

---
## Features
- Fully optimized for Linux.
- Fully optimized for Windows.
- Quick and straightforward installation.
- Easy configuration through a single file.
- Seamless integration with popular hosting platforms.

---

## Installation and Setup

1. Download last version for your OS in [Releases](https://github.com/klaksik/memhash_miner/releases/tag/v1.0.0) :

2. Start applicaton:

      on linux:

       1. install python3.12:
         ```bash
          sudo apt update
          sudo apt install -y software-properties-common
          sudo add-apt-repository -y ppa:deadsnakes/ppa
          sudo apt update
          sudo apt install -y python3.12
         ```
       2. install pip:
         ```bash
          sudo apt install -y python3.12-distutils
          wget https://bootstrap.pypa.io/get-pip.py
          sudo python3.12 get-pip.py
         ```
       3. clone repo:
         ```bash
          sudo git clone https://github.com/klaksik/memhash_miner
          cd memhash_miner
         ```
       4.
        ```bash
         pip install -r requirements.txt
         python3.12 miner_linux
        ```
      on windows:
   
       Just open app

4. Configure the URL:
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
   - Copy the URL of the selected element and paste it into `config.json`:

5. Configure the Telegram bot:
   - go to https://t.me/BotFather
   - create bot and paste token into `config.json`
   
6. Start applicaton:

      on linux:
      ```bash
       python3.12 miner_linux
      ```
      on windows:
   
       Just open app
---

## BOT command

/screen - for get screen memhash

---

## License

This project is distributed under the **MIT License**. Feel free to use, modify, and share.

---

## Contact

For inquiries and suggestions:
- Telegram: [@Klaksiks](https://t.me/Klaksiks)

---

Thank you for using Memhash Miner!
