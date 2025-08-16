#!/usr/bin/python3

import telebot
import re
import pytesseract
from PIL import Image
import os

bot = telebot.TeleBot("8279142566:AAE7719-93KPDHFXc0q8Y1eMCKJ_FUOpk0E")  # đổi token của bạn vào đây

@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    try:
        file_info = bot.get_file(message.photo[-1].file_id)
        downloaded_file = bot.download_file(file_info.file_path)

        with open("temp.jpg", "wb") as f:
            f.write(downloaded_file)

        img = Image.open("temp.jpg")
        text = pytesseract.image_to_string(img)

        matches = re.findall(r'(\d{1,3}(?:\.\d{1,3}){3})[: ](\d+)', text)

        if not matches:
            bot.reply_to(message, "❌ Không tìm thấy IP:PORT trong ảnh.")
            return

        valid = [(ip, int(port)) for ip, port in matches if 10011 <= int(port) <= 10020]

        if valid:
            result = "🎯 IP:PORT nhận diện được (10011-10020):\n"
            for ip, port in valid:
                result += f"{ip}:{port}\n"
            bot.reply_to(message, result)
        else:
            bot.reply_to(message, "❌ Không có IP nào trong khoảng 10011-10020.")

        os.remove("temp.jpg")
    except Exception as e:
        bot.reply_to(message, f"Lỗi OCR: {e}")

bot.polling()
