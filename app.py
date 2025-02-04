from flask import Flask, render_template, request, send_file
from PIL import Image
import os
from io import BytesIO

app = Flask(__name__, static_folder="static", template_folder="templates")

@app.route("/")
def index():
    return render_template("index.html")

def compress_image_to_size(image, target_size_kb):
    """Compresses the image while maintaining the target size"""
    buffer = BytesIO()
    quality = 95  # Start with high quality

    for quality in range(95, 5, -5):  # Reduce quality stepwise
        buffer.seek(0)
        buffer.truncate()
        image.save(buffer, format="JPEG", quality=quality, optimize=True)
        size_kb = len(buffer.getvalue()) / 1024

        if size_kb <= target_size_kb:
            break

    buffer.seek(0)
    return buffer

@app.route("/compress", methods=["POST"])
def compress_image():
    if "image" not in request.files:
        return "No file uploaded", 400

    file = request.files["image"]
    if file.filename == "":
        return "No file selected", 400

    target_size = float(request.form.get("size", 500))  # Default 500 KB
    size_unit = request.form.get("unit", "KB")  # Default KB

    # Convert MB to KB if needed
    if size_unit.upper() == "MB":
        target_size *= 1024

    try:
        img = Image.open(file)
        img_format = img.format

        # Convert PNG/WebP to JPEG to allow compression
        if img_format in ["PNG", "WEBP"]:
            img = img.convert("RGB")
            img_format = "JPEG"

        # Get original filename and generate new name
        original_filename = file.filename
        new_filename = f"compressed_{original_filename}"

        # Compress image to target size
        buffer = compress_image_to_size(img, target_size)

        return send_file(buffer, mimetype="image/jpeg", as_attachment=True, download_name=new_filename)

    except Exception as e:
        return f"Error processing image: {str(e)}", 500

if __name__ == "__main__":
    app.run(debug=True)
