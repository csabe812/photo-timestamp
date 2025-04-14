import os
from PIL import Image, ImageDraw, ImageFont
import piexif
from datetime import datetime


def add_timestamp(image_path, output_folder, font_file):
    try:
        img = Image.open(image_path)
        exif_data = img.info.get('exif')

        if not exif_data:
            print(f"No EXIF data found in: {image_path}")
            return

        exif_dict = piexif.load(exif_data)
        datetime_original = exif_dict["0th"].get(piexif.ImageIFD.DateTime)

        if not datetime_original:
            print(f"No timestamp found in: {image_path}")
            return

        # timestamp = datetime_original.decode("utf-8")
        raw_timestamp = datetime_original.decode(
            "utf-8")  # e.g., '2024:04:14 18:45:12'
        parsed = datetime.strptime(raw_timestamp, "%Y:%m:%d %H:%M:%S")
        timestamp = parsed.strftime("%Y-%m-%d %H:%M:%S")

        # Draw timestamp
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype(font_file, 100)
        margin = 130
        bbox = draw.textbbox((0, 0), timestamp, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        x = img.width - text_width - margin
        y = img.height - text_height - margin

        # Outline for visibility
        for dx in [-2, 2]:
            for dy in [-2, 2]:
                draw.text((x+dx, y+dy), timestamp, font=font, fill="black")

        draw.text((x, y), timestamp, font=font, fill="red")

        # Save output
        filename = os.path.basename(image_path)
        output_path = os.path.join(output_folder, f"timestamped_{filename}")
        img.save(output_path, exif=exif_data)

        print(f"Processed: {filename}")

    except Exception as e:
        print(f"Error processing {image_path}: {e}")


def process_folder(input_folder, output_folder, font_file):
    os.makedirs(output_folder, exist_ok=True)
    supported_exts = ('.jpg', '.jpeg', '.png')

    for filename in os.listdir(input_folder):
        if filename.lower().endswith(supported_exts):
            image_path = os.path.join(input_folder, filename)
            add_timestamp(image_path, output_folder, font_file)


# Example usage
input_folder = "this-is-your-path"
output_folder = "this-is-your-output-path"
font_file = "this-is-your-font-file.ttf"
process_folder(input_folder, output_folder, font_file)
