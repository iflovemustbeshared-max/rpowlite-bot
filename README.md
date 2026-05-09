# Rpowlite Telegram Bot

Bot Telegram interaktif untuk berinteraksi dengan API rpow.hopeware.ltd. Bot ini mendukung pengecekan info akun, melihat chat terbaru, dan melakukan minting token melalui Proof-of-Work (PoW).

## Fitur

- `/rpowlite_start` - Memulai bot dan melihat daftar perintah.
- `/rpowlite_me` - Melihat informasi akun (pubkey, balance, dll).
- `/rpowlite_chat` - Melihat pesan chat terbaru dari rpow.
- `/rpowlite_mint` - Melakukan minting token baru (memerlukan penyelesaian tantangan PoW).

## Cara Deploy ke Railway

1.  **Fork atau Clone Repositori ini.**
2.  **Buat Proyek Baru di Railway:**
    - Hubungkan dengan repositori GitHub Anda.
3.  **Konfigurasi Variabel Lingkungan (Environment Variables):**
    - `TELEGRAM_BOT_TOKEN`: Token bot Telegram Anda (dapatkan dari @BotFather).
    - `PRIVKEY`: Kunci pribadi (private key) Anda untuk autentikasi dengan API rpow.hopeware.ltd. (Opsional, hanya jika API memerlukan autentikasi dengan privkey).
4.  **Deploy:**
    - Railway akan secara otomatis mendeteksi `Dockerfile` dan melakukan build serta deploy.

## GitHub Actions CI/CD

Repositori ini menyertakan workflow GitHub Actions untuk deploy otomatis ke Railway setiap kali ada push ke branch `main`. Pastikan Anda telah menambahkan `RAILWAY_TOKEN` ke GitHub Secrets repositori Anda.

## Lisensi

MIT
