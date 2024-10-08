import os
from PIL import Image, ImageDraw, ImageFont

def get_default_font():
    """Return a default font path based on the OS or use the built-in PIL font."""
    if os.name == 'nt':  # Windows
        return "C:\\Windows\\Fonts\\Consolas.ttf"  # Common Windows monospace font
    else:
        return "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"  # Common on Linux

def take_screenshot(filepath, screenshot_dir, line_number, search_word):

    with open(filepath, "r", encoding="utf-8", errors="replace") as file:
        # Ensure the screenshot directory exists
        if not os.path.exists(screenshot_dir):
            os.makedirs(screenshot_dir)

        lines = file.readlines()
        start_line = max(0, line_number - 5)
        end_line = min(len(lines), line_number + 5)

        relevant_line = lines[start_line:end_line]
        relevant_content = ''.join(relevant_line)

        # Clean up the search word for the filename
        secret_word = search_word.replace('android', '').replace('=', '_').replace('"', '_')

        # Create the filename and path for the screenshot
        filename = f'{secret_word}_{os.path.basename(filepath)}_{line_number}.png'
        screenshot_path = os.path.join(screenshot_dir, filename)

        # Define font path or use a fallback if not found
        font_path = get_default_font()

        try:
            font = ImageFont.truetype(font_path, 20)
        except IOError:
            font = ImageFont.load_default()  # Fallback to default font

        # Create the image and draw the text
        image = Image.new('RGB', (3000, 600), color='white')
        draw = ImageDraw.Draw(image)
        
        # Draw the relevant content and the file location
        draw.text((5, 100), relevant_content, fill=(0, 0, 0), font=font)
        draw.text((5, 50), f'File location: {filepath}', fill=(0, 0, 0), font=ImageFont.truetype(font_path, 30))

        # Save the image
        image.save(screenshot_path)
