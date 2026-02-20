# SecretPixel

Hide secret messages *inside* ordinary image files.

This is a Python steganography tool that modifies the Least Significant Bit (LSB) of each pixel to store your data invisibly. The resulting image looks identical to the naked eye.

## Installation

**Prerequisites:** Python 3+

1.  **Clone the repo:**
    ```bash
    git clone https://github.com/onlyascend01-ai/SecretPixel.git
    cd SecretPixel
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## Usage

### 1. Hide a Message
To hide text inside `cat.png`:

```bash
python secretpixel.py hide cat.png "The eagle lands at midnight." -o secret_cat.png
```

This creates `secret_cat.png`. It looks exactly like `cat.png`, but it contains your secret message.

### 2. Reveal a Message
To extract the hidden text from `secret_cat.png`:

```bash
python secretpixel.py reveal secret_cat.png
```

### Note
- Use **PNG** images for best results (lossless).
- JPEG/JPG images compress data, which destroys the hidden message.
- The larger the image resolution, the more text you can hide!

## License
MIT License. Created by **Lux**.
