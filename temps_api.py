from flask import Flask
import subprocess
import re

app = Flask(__name__)


# ---------- CPU TEMP ----------
def get_cpu_temp():
    out = subprocess.getoutput("sensors")
    match = re.search(r"Package id 0:\s+\+?([\d\.]+)", out)
    return match.group(1) if match else "N/A"


# ---------- CPU USAGE ----------
def get_cpu_usage():
    # uses top for accurate system-wide %
    out = subprocess.getoutput("top -bn1 | grep 'Cpu(s)'")
    match = re.search(r"(\d+\.\d+)\s*id", out)
    if match:
        idle = float(match.group(1))
        return round(100 - idle, 1)
    return "N/A"


# ---------- GPU ----------
def get_gpu_stats():
    try:
        out = subprocess.getoutput(
            "nvidia-smi --query-gpu=temperature.gpu,utilization.gpu --format=csv,noheader,nounits"
        )
        temp, usage = out.split(",")
        return temp.strip(), usage.strip()
    except:
        return "N/A", "N/A"


@app.route("/")
def index():
    cpu_temp = get_cpu_temp()
    cpu_usage = get_cpu_usage()
    gpu_temp, gpu_usage = get_gpu_stats()

    return f"""
    <html>
    <head>
      <meta http-equiv="refresh" content="5">
      <style>
        body {{
            background: transparent;
            color: #eee;
            font-family: system-ui, sans-serif;
            margin: 0;
            padding: 10px;
        }}

        .grid {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            text-align: center;
        }}

        .title {{
            font-size: 14px;
            opacity: 0.7;
        }}

        .temp {{
            font-size: 42px;
            font-weight: bold;
            margin-top: 4px;
        }}

        .usage {{
            font-size: 13px;
            opacity: 0.6;
        }}
      </style>
    </head>
    <body>
      <div class="grid">
        <div>
          <div class="title">CPU</div>
          <div class="temp">{cpu_temp}°C</div>
          <div class="usage">{cpu_usage}% use</div>
        </div>

        <div>
          <div class="title">GPU</div>
          <div class="temp">{gpu_temp}°C</div>
          <div class="usage">{gpu_usage}% use</div>
        </div>
      </div>
    </body>
    </html>
    """


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=2013)
