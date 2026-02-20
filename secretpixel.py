import argparse
import os
import sys
from PIL import Image

def text_to_binary(text):
    """Converts a string to a binary string."""
    binary_data = ''.join(format(ord(char), '08b') for char in text)
    return binary_data

def binary_to_text(binary_data):
    """Converts a binary string back to text."""
    all_bytes = [binary_data[i:i+8] for i in range(0, len(binary_data), 8)]
    return "".join([chr(int(byte, 2)) for byte in all_bytes])

def hide_message(image_path, secret_message, output_path):
    """Hides the secret message inside the image."""
    try:
        img = Image.open(image_path)
        img = img.convert("RGB") # Ensure RGB mode
        
        # Using list(img.getdata()) is standard, ignoring deprecation for now
        pixels = list(img.getdata())

        # Add delimiter to know where message ends
        secret_message += "#####" 
        binary_secret = text_to_binary(secret_message)
        data_len = len(binary_secret)

        if data_len > len(pixels) * 3:
            print("[-] Error: Image is too small to hold this message!")
            return

        print(f"[*] Encrypting...")

        new_pixels = []
        data_index = 0

        for pixel in pixels:
            r, g, b = pixel
            
            if data_index < data_len:
                r = (r & ~1) | int(binary_secret[data_index])
                data_index += 1
            if data_index < data_len:
                g = (g & ~1) | int(binary_secret[data_index])
                data_index += 1
            if data_index < data_len:
                b = (b & ~1) | int(binary_secret[data_index])
                data_index += 1

            new_pixels.append((r, g, b))

        img.putdata(new_pixels)
        img.save(output_path, "PNG")
        
        print("\n" + "="*50)
        print(f"[+] SUCCESS! Secret saved to:\n   -> {output_path}")
        print("="*50)
        print("[!] IMPORTANT: To reveal the message later, select THIS new file!")
        print("="*50 + "\n")

    except Exception as e:
        print(f"[-] Error: {e}")

def reveal_message(image_path):
    """Reveals the hidden message from the image."""
    try:
        print(f"[*] Analyzing...")
        img = Image.open(image_path)
        img = img.convert("RGB")
        pixels = list(img.getdata())

        binary_data = ""
        for pixel in pixels:
            r, g, b = pixel
            binary_data += str(r & 1)
            binary_data += str(g & 1)
            binary_data += str(b & 1)

        all_bytes = [binary_data[i:i+8] for i in range(0, len(binary_data), 8)]
        
        decoded_msg = ""
        for byte in all_bytes:
            decoded_msg += chr(int(byte, 2))
            if decoded_msg.endswith("#####"):
                print("\n" + "="*50)
                print(f"[*] HIDDEN MESSAGE FOUND:\n\n   {decoded_msg[:-5]}")
                print("="*50 + "\n")
                return

        print("\n[-] No hidden message found.")
        print("    (Did you select the original image instead of the secret one?)")

    except Exception as e:
        print(f"[-] Error: {e}")

def interactive_mode():
    """Runs the interactive CLI wizard."""
    while True:
        print("\n=== SecretPixel ===")
        print("--------------------------------")
        print("1. Hide a Message")
        print("2. Reveal a Message")
        print("3. Exit")
        
        choice = input("\n-> Choose an option (1/2/3): ").strip()

        if choice == "1":
            raw_path = input("-> Enter image path (drag & drop file here): ").strip()
            # Handle quotes added by drag-and-drop
            if raw_path.startswith('"') and raw_path.endswith('"'):
                image_path = raw_path[1:-1]
            elif raw_path.startswith("'") and raw_path.endswith("'"):
                image_path = raw_path[1:-1]
            else:
                image_path = raw_path

            if not os.path.exists(image_path):
                print(f"[-] Error: File not found: {image_path}")
                continue
                
            message = input("-> Enter your secret message: ").strip()
            if not message:
                print("[-] Message cannot be empty.")
                continue

            # Auto-generate output filename
            folder = os.path.dirname(image_path)
            filename = os.path.splitext(os.path.basename(image_path))[0]
            output_path = os.path.join(folder, f"{filename}_secret.png")
            
            hide_message(image_path, message, output_path)
            
        elif choice == "2":
            raw_path = input("-> Enter image path to reveal (drag & drop file here): ").strip()
            if raw_path.startswith('"') and raw_path.endswith('"'):
                image_path = raw_path[1:-1]
            elif raw_path.startswith("'") and raw_path.endswith("'"):
                image_path = raw_path[1:-1]
            else:
                image_path = raw_path

            if not os.path.exists(image_path):
                print(f"[-] Error: File not found: {image_path}")
                continue
                
            reveal_message(image_path)
            
        elif choice == "3":
            print("Goodbye!")
            sys.exit()
        else:
            print("[-] Invalid choice!")

def main():
    parser = argparse.ArgumentParser(description="SecretPixel - Hide messages in images using Steganography.")
    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # Hide Command
    hide_parser = subparsers.add_parser("hide", help="Hide a secret message inside an image")
    hide_parser.add_argument("image", help="Path to the original image")
    hide_parser.add_argument("message", help="The secret message to hide")
    hide_parser.add_argument("-o", "--output", help="Output filename (optional)")

    # Reveal Command
    reveal_parser = subparsers.add_parser("reveal", help="Reveal a secret message from an image")
    reveal_parser.add_argument("image", help="Path to the image with hidden message")

    args = parser.parse_args()

    if args.command == "hide":
        if args.output:
            output = args.output
        else:
            folder = os.path.dirname(args.image)
            filename = os.path.splitext(os.path.basename(args.image))[0]
            output = os.path.join(folder, f"{filename}_secret.png")
            
        hide_message(args.image, args.message, output)
    elif args.command == "reveal":
        reveal_message(args.image)
    else:
        interactive_mode()

if __name__ == "__main__":
    main()
