# Secure Steganography

This Python script, `secure_steganography_chambal.py`, lets you **encrypt** (hide) and **decrypt** (extract) messages in image files without visible difference using simple steganography with a modified caesar cipher. The script runs in interactive mode.

---

## Requirements

- Python 3.6 or higher  
- [Pillow](https://pypi.org/project/Pillow/) (for image I/O)

Install Pillow via pip:

```bash
pip install Pillow
```

---

## Setup

1. **Download** the file `secure_steganography_chambal.py`.  
2. **Create** an `output/` directory in the same folder as the script:

   ```bash
   mkdir output
   ```

---

## Running the Script

Run the program with:

```bash
python3 secure_steganography_chambal.py
```

You will see:

```
Select program mode: (encrypt/decrypt/exit):
```

---

### Encrypt (hide) a message

1. Type `encrypt` and press Enter.  
2. When prompted, enter the **path** to an existing **.jpg** or **.jpeg** image:

   ```
   Enter image filename: myphoto.jpg
   ```

3. Enter a **secret key** (composed of only the letters `u` [upshift] and `d` [downshift], length between **3** and **20**):

   ```
   Enter Key: uduudd
   ```

4. Enter your **message** (printable ASCII only, length **10–1000**):

   ```
   Enter Message: Meet me at the old pier at midnight.
   ```

   The script will re‑prompt if:
   - The key contains other letters or has invalid length.  
   - The message has non‑printable characters or wrong length.  
   - The combined message+key data won’t fit in the image.

5. The resulting image is saved as:

   ```
   output/modified_<original_filename>.png
   ```

   _Example: `output/modified_myphoto.jpg.png`_

---

### Decrypt (extract) a message

1. Type `decrypt` and press Enter.  
2. Enter the path to your image with a hidden message (from `output/`):

   ```
   Enter image filename: output/modified_myphoto.jpg.png
   ```

3. The script reads the hidden bits, reconstructs the key and encrypted message, then **decrypts** it.

4. Your extracted message is written to:

   ```
   output/<basename>_decoded_message.txt
   ```

   _Example: `output/myphoto_decoded_message.txt`_

---

## Key & Message Rules

- **Key**:  
  - Only characters `u` (upshift) or `d` (downshift)  
  - 3 ≤ Length ≤ 20  
- **Message**:  
  - Printable ASCII codes 32–126  
  - 10 ≤ Length ≤ 1000  

---

## Notes

- Input images **must** be `.jpg` or `.jpeg`.  
- Output images are saved as **PNG** (lossless) to preserve hidden bits.  
- Always use images large enough to embed your message + key (script enforces this).  
- The `output/` directory must exist before running the script.

---

## Author

**Vivekjeet Singh Chambal**  
University of the Philippines Los Baños
