# Dx Sprite Font Helper
is a Python application that converts TrueType Font (TTF) files into bitmap PNG images compatible with the DirectX Tool Kit's MakeSpriteFont tool.

## Dependencies:
*freetype-py<br>
*Pillow

You can install the required dependencies using pip:

`pip install freetype-py Pillow`


## Usage:
Run the script with the following command:

`python BitMapMaker.py --size <size> --output <output_file> <input_file>`<br><br>

`<size>` - The font size to render.<br>
`<output_file>` - The filename for the output PNG bitmap.<br>
`<input_file>` - The path to the input TTF font file.<br>

##Example:
`python BitMapMaker.py --size 32 --output font_bitmap.png Arial.ttf`

