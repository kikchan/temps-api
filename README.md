# 🌡️ Speedforce Temp API

A lightweight Flask API that bridges system hardware data (`lm-sensors` and `nvidia-smi`) to Dashy widgets.

## 📋 Prerequisites
Ensure your Linux environment has the necessary tools:
* **Python 3 & Pip**
* **lm-sensors**: `sudo apt install lm-sensors && sudo sensors-detect`
* **NVIDIA Drivers**: (Only for GPU tracking) `nvidia-smi` must be functional.

## 🚀 Quick Start
1. **Install Dependencies**:
   ```bash
   # Install the venv tool if you don't have it
    sudo apt update && sudo apt install python3-venv -y

    # Create the environment (folder named 'venv')
    python3 -m venv venv

    # Install the packages into that environment
    ./venv/bin/pip install flask flask-cors
   ````
2. **Test the Script**:
   ```bash
   python3 temp_api.py
   ````
3. **Verify**:
    
    Open in your browser:
    ```bash 
    http://localhost:2013/api/temps/cpu 
    ````

## ⚙️ Deployment (Systemd)
To ensure the API runs 24/7 and starts on boot:

1. Create `temp_api.service` in `/etc/systemd/system/`.

2. Add
    ````bash
    [Unit]
    Description=Speedforce Hardware Temp API for Dashy
    After=network.target

    [Service]
    # Replace 'kikchan' with your actual linux username
    User=kikchan
    # Replace with the actual directory where your script is located
    WorkingDirectory=/home/kikchan/.local/bin
    # Ensure the path to python3 and the script are absolute
    ExecStart=/usr/bin/python3 /home/kikchan/.local/bin/temp_api.py
    Restart=always
    RestartSec=5

    [Install]
    WantedBy=multi-user.target
    ````

3. Run:
    ````bash
    sudo systemctl daemon-reload
    sudo systemctl enable temp_api.service
    sudo systemctl start temp_api.service
    ````

## 📊 Dashy Config
Add this to your `conf.yml`:
````bash
  - name: System Temps
    icon: fas fa-thermometer-half
    widgets:
      - type: iframe
        options:
          url: http://192.168.1.20:2013
          height: 300
````