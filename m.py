#!/usr/bin/python3

import telebot
import re
import pytesseract
from PIL import Image
import os

# === TOKEN BOT ===
bot = telebot.TeleBot("PUT-YOUR-TOKEN-HERE")  # đổi token của bạn vào đây

@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    try:
        # tải ảnh về
        file_info = bot.get_file(message.photo[-1].file_id)
        downloaded_file = bot.download_file(file_info.file_path)

        with open("temp.jpg", "wb") as f:
            f.write(downloaded_file)

        # OCR lấy text
        img = Image.open("temp.jpg")
        text = pytesseract.image_to_string(img)

        # Regex tìm IP:PORT
        matches = re.findall(r'(\d{1,3}(?:\.\d{1,3}){3})[: ](\d+)', text)

        if not matches:
            bot.reply_to(message, "❌ Không tìm thấy IP:PORT trong ảnh.")
            return

        # lọc port >= 10011
        valid = [(ip, int(port)) for ip, port in matches if int(port) >= 10011]

        if valid:
            result = "🎯 IP:PORT nhận diện được:\n"
            for ip, port in valid:
                result += f"{ip}:{port}\n"
            bot.reply_to(message, result)
        else:
            bot.reply_to(message, "❌ Không có IP nào hợp lệ (port >= 10011).")

        os.remove("temp.jpg")
    except Exception as e:
        bot.reply_to(message, f"Lỗi OCR: {e}")

bot.polling()