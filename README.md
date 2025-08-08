# Dx Sprite Font Helper
is a Python application that converts TrueType Font (TTF) files into bitmap PNG images compatible with the DirectX Tool Kit's MakeSpriteFont tool.

Dependencies:

freetype-py

Pillow

You can install the required dependencies using pip:
```
pip install freetype-py Pillow
```

Usage:
Run the script with the following command:
```
python BitMapMaker.py --size <size> --output <output_file> <input_file>
```
<size> - The font size to render.
<output_file> - The filename for the output PNG bitmap.
<input_file> - The path to the input TTF font file.

Example:
```
python BitMapMaker.py --size 32 --output font_bitmap.png Arial.ttf
```
