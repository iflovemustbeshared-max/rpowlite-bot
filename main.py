import os
import logging
import hashlib
import asyncio
from datetime import datetime, timedelta
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from api_client import RpowClient

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

# Environment variables
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
PRIVKEY = os.getenv("PRIVKEY") # New environment variable for private key

rpow_client = RpowClient(privkey=PRIVKEY)

# PoW Solver (simple brute-force for demonstration)
async def solve_pow(nonce_prefix, difficulty_bits):
    target = 2**(256 - difficulty_bits)
    for nonce in range(10000000):  # Limit nonce search for practical reasons
        message = f"{nonce_prefix}{nonce}"
        hashed = hashlib.sha256(message.encode()).hexdigest()
        if int(hashed, 16) < target:
            return nonce
    return None

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Halo! Saya adalah bot Rpowlite. Gunakan perintah berikut:\n"
        "/rpowlite_me - Dapatkan info akun Anda.\n"
        "/rpowlite_chat - Dapatkan pesan chat terbaru.\n"
        "/rpowlite_mint - Coba mint token baru (membutuhkan PoW).\n"
    )

async def get_me(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        me_info = rpow_client.get_my_info()
        response_text = (
            f"Info Akun:\n"
            f"Pubkey: {me_info.get("pubkey")}\n"
            f"Balance: {me_info.get("balance")}\n"
            f"Minted: {me_info.get("minted")}\n"
            f"Sent: {me_info.get("sent")}\n"
            f"Received: {me_info.get("received")}"
        )
    except Exception as e:
        response_text = f"Error mengambil info akun: {e}"
    await update.message.reply_text(response_text)

async def get_chat(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        # Get messages from the last 5 minutes
        since_time = (datetime.utcnow() - timedelta(minutes=5)).isoformat(timespec="milliseconds") + "Z"
        chat_messages = rpow_client.get_chat_messages(since=since_time)
        if chat_messages:
            response_text = "Pesan Chat Terbaru:\n"
            for msg in chat_messages:
                response_text += f"- [{msg.get("at").split("T")[-1][:-5]}] {msg.get("short_pub")}: {msg.get("text")}\n"
        else:
            response_text = "Tidak ada pesan chat terbaru."
    except Exception as e:
        response_text = f"Error mengambil pesan chat: {e}"
    await update.message.reply_text(response_text)

async def mint_token(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Mencoba mint token baru... Ini mungkin memakan waktu beberapa saat karena Proof-of-Work.")
    try:
        challenge = rpow_client.get_challenge()
        challenge_id = challenge["challenge_id"]
        nonce_prefix = challenge["nonce_prefix"]
        difficulty_bits = challenge["difficulty_bits"]

        await update.message.reply_text(f"Mendapatkan tantangan PoW. Mencari nonce untuk difficulty {difficulty_bits}...")
        
        solution_nonce = await solve_pow(nonce_prefix, difficulty_bits)

        if solution_nonce is not None:
            await update.message.reply_text(f"Nonce ditemukan: {solution_nonce}. Mengirim solusi...")
            mint_result = rpow_client.submit_mint(challenge_id, solution_nonce)
            response_text = (
                f"Token berhasil di-mint!\n"
                f"ID Token: {mint_result.get("token", {}).get("id")}\n"
                f"Value: {mint_result.get("token", {}).get("value")}\n"
                f"Issued At: {mint_result.get("token", {}).get("issued_at")}"
            )
        else:
            response_text = "Gagal menemukan nonce dalam batas waktu. Coba lagi."
    except Exception as e:
        response_text = f"Error saat mint token: {e}"
    await update.message.reply_text(response_text)

def main() -> None:
    """Start the bot."""
    if not TELEGRAM_BOT_TOKEN:
        logger.error("TELEGRAM_BOT_TOKEN environment variable not set.")
        return

    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    application.add_handler(CommandHandler("rpowlite_start", start))
    application.add_handler(CommandHandler("rpowlite_me", get_me))
    application.add_handler(CommandHandler("rpowlite_chat", get_chat))
    application.add_handler(CommandHandler("rpowlite_mint", mint_token))

    logger.info("Bot started polling...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
