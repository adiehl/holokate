#!/usr/bin/env python3
import os

def extract_jfif_jpeg(file_path):
    with open(file_path, 'rb') as f:
        data = f.read()

    # Locate the JFIF header (APP0 marker) and SOI marker
    start_jfif = data.find(b'\xFF\xE0')
    start_soi = data.find(b'\xFF\xD8')

    if start_jfif == -1 or start_soi == -1 or start_soi > start_jfif:
        raise ValueError("Invalid file: cannot find SOI before JFIF header.")

    # Extract the length of the JFIF segment
    length_jfif = int.from_bytes(data[start_jfif+2:start_jfif+4], byteorder='big')

    # Extract the JFIF segment (\xFF\xE0 + length)
    jfif_data = data[start_jfif : start_jfif + 2 + length_jfif]

    # Write extracted JFIF data
    base_name = os.path.splitext(file_path)[0]
    jfif_out = f"{base_name}.jfif_data"
    with open(jfif_out, 'wb') as f_jfif:
        f_jfif.write(jfif_data)

    # Write the full JPEG image starting from SOI
    jpeg_out = f"{base_name}.jpg"
    with open(jpeg_out, 'wb') as f_jpeg:
        f_jpeg.write(data[start_soi:])

    print(f"JFIF data saved to {jfif_out}")
    print(f"JPEG data saved to {jpeg_out}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python extract_jfif_jpeg.py <file.jfif>")
    else:
        extract_jfif_jpeg(sys.argv[1])
