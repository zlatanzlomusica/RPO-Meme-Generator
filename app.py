import os
import io
import textwrap 
from flask import Flask, render_template, request
from PIL import Image, ImageDraw, ImageFont

app = Flask(__name__)

OUTPUT_FOLDER = 'static'
if not os.path.exists(OUTPUT_FOLDER):
    os.makedirs(OUTPUT_FOLDER)

FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" 


def create_meme(image_data, top_text, bottom_text, output_path):
    """Opens image, adds text with outline, and saves it."""
    
    img = Image.open(image_data).convert('RGB')
    width, height = img.size
    draw = ImageDraw.Draw(img)
    
    font_size = int(height * 0.1) 
    font = ImageFont.load_default()
    print("WARNING: Using default PIL font.") 
    
    try:
        font = ImageFont.truetype(FONT_PATH, font_size)
    except IOError:
        print("Warning: Failed to load DejaVuSans-Bold.ttf. Using default font.")
        font = ImageFont.load_default()
        
    text_color = "white"
    outline_color = "black"
    outline_width = 2
    
    wrapped_top = textwrap.fill(top_text.upper(), 30)
    wrapped_bottom = textwrap.fill(bottom_text.upper(), 30)

    def draw_text_with_outline(draw, x, y, text, font, text_color, outline_color, width):
        for dx in range(-width, width + 1):
            for dy in range(-width, width + 1):
                if dx != 0 or dy != 0:
                    draw.text((x + dx, y + dy), text, font=font, fill=outline_color, anchor="ms")
        draw.text((x, y), text, font=font, fill=text_color, anchor="ms")
    

    center_x = width / 1.75
    top_y = height * 0.15
    bottom_y = height * 0.90
    
    if wrapped_top:
        draw_text_with_outline(draw, center_x, top_y, wrapped_top, font, text_color, outline_color, outline_width)
        
    if wrapped_bottom:
        draw_text_with_outline(draw, center_x, bottom_y, wrapped_bottom, font, text_color, outline_color, outline_width)
    
    img.save(output_path, format="JPEG")


@app.route('/', methods=['GET', 'POST'])
def index():
    meme_generated = False
    
    if request.method == 'POST':
        image_file = request.files.get('image_file')
        top_text = request.form.get('top_text', '')
        bottom_text = request.form.get('bottom_text', '')

        if image_file and image_file.filename != '':
            img_bytes = io.BytesIO(image_file.read())
            output_path = os.path.join(OUTPUT_FOLDER, 'meme.jpg')
            
            try:
                create_meme(img_bytes, top_text, bottom_text, output_path)
                meme_generated = True
            except Exception as e:
                print(f"Error generating meme: {e}")
                
            cache_buster = os.urandom(8).hex()
            return render_template('index.html', 
                                   meme_image=meme_generated, 
                                   cache_buster=cache_buster)

    return render_template('index.html', meme_image=False)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)