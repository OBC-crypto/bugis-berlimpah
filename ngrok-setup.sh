#!/bin/bash

set -e

# === Konfigurasi ===
#NGROK_TOKEN=""
NGROK_TOKEN=""
PORT_WEB=8080   # Ganti ke port yang kamu inginkan
NGROK_LOG="$HOME/ngrok.log"

echo "?? Menyiapkan ngrok..."
if ! command -v ngrok >/dev/null; then
  echo "?? Menginstal ngrok..."
  curl -s https://ngrok-agent.s3.amazonaws.com/ngrok.asc | sudo tee /etc/apt/trusted.gpg.d/ngrok.asc >/dev/null
  echo "deb https://ngrok-agent.s3.amazonaws.com buster main" | sudo tee /etc/apt/sources.list.d/ngrok.list
  sudo apt update && sudo apt install -y ngrok
else
  echo "? Ngrok sudah terpasang."
fi

# === Tambahkan Authtoken ===
echo "?? Menambahkan authtoken ngrok..."
ngrok config add-authtoken "${NGROK_TOKEN}"

# === Jalankan tunnel ===
echo "?? Menjalankan tunnel ke port ${PORT_WEB}..."
nohup ngrok http ${PORT_WEB} --log=stdout > "${NGROK_LOG}" 2>&1 &

# Tunggu ngrok aktif
sleep 8

# === Ambil URL publik ===
NGROK_URL=$(curl -s http://127.0.0.1:4040/api/tunnels \
  | grep -oE 'https://[a-z0-9\-]+\.ngrok-free\.app' \
  | head -n1)

if [[ -n "$NGROK_URL" ]]; then
  echo "? Tunnel aktif! Akses di: ${NGROK_URL}"
else
  echo "?? Tidak bisa mengambil URL ngrok. Periksa log di: ${NGROK_LOG}"
fi
