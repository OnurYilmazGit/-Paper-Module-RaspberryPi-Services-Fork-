from flask import Flask, request
from PIL import Image, ImageDraw, ImageFont
import logging
import traceback
import os
from waveshare_epd import epd1in54_V2
import textwrap

app = Flask(__name__)

def init_epd():
    logging.basicConfig(level=logging.DEBUG)
    epd = epd1in54_V2.EPD()
    logging.info("init and Clear")
    epd.init(0)
    return epd

# Endpoint to clear screen
@app.route("/clearScreen", methods=["PUT"])
def clear_screen():
    try:
        epd = init_epd()
        epd.Clear(0xFF)
        return {"message": "Screen cleared successfully."}, 200
    except Exception as e:
        return {"error": str(e), "trace": traceback.format_exc()}, 400

# Endpoint to display Image
@app.route("/displayImage", methods=["POST"])
def display_image():
    try:
        epd = init_epd()
        image_file = request.files.get('image')
        if image_file:
            image = Image.open(image_file)
            bw_image = image.convert('1').resize((epd.width, epd.height))
            epd.display(epd.getbuffer(bw_image))
            return {"message": "Image displayed successfully."}, 200
        else:
            return {"error": "Image file not provided."}, 400
    except Exception as e:
        return {"error": str(e), "trace": traceback.format_exc()}, 400

# Endpoint to display Cross
@app.route("/displayCross", methods=["PUT"])  # Changed from GET to PUT
def display_cross():
    try:
        epd = init_epd()
        image = Image.new('1', (epd.width, epd.height), 255)  # 255: clear the frame
        draw = ImageDraw.Draw(image)
        draw.line((0, 0, epd.width, epd.height), fill=0, width=10)
        draw.line((epd.width, 0, 0, epd.height), fill=0, width=10)
        epd.display(epd.getbuffer(image))
        return {"message": "Cross displayed successfully."}, 200
    except Exception as e:
        return {"error": str(e), "trace": traceback.format_exc()}, 400

from textwrap import wrap

@app.route("/displayText", methods=["POST"])
def display_text():
    try:
        epd = init_epd()
        image = Image.new('1', (epd.width, epd.height), 255)  # 255: clear the frame
        draw = ImageDraw.Draw(image)
        text = request.form.get("text", "Default Text")

        max_width = epd.width
        max_height = epd.height
        font_size = 20  # starting font size
        font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', font_size)

        # Split the text into lines so that each line fits within the display width
        lines = wrap(text, width=12)  # This width might need adjusting

        # Check if the total height of the text exceeds the display height
        total_height = len(lines) * font.getsize(lines[0])[1]
        while font_size > 1 and total_height > max_height:
            font_size -= 1
            font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', font_size)
            total_height = len(lines) * font.getsize(lines[0])[1]

        current_height = 0
        for line in lines:
            draw.text((0, current_height), line, font=font, fill=0)
            current_height += font.getsize(line)[1]

        epd.display(epd.getbuffer(image))
        return {"message": "Text displayed successfully."}, 200
    except Exception as e:
        return {"error": str(e), "trace": traceback.format_exc()}, 400

if __name__ == "__main__":
    app.run(port=9920, debug=True)
