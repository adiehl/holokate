#!/usr/bin/env python3
import os

def merge_jfif_jpeg(jfif_file, jpeg_file):
    # Read the extracted JFIF header data
    with open(jfif_file, 'rb') as f_jfif:
        jfif_data = f_jfif.read()

    # Read the full JPEG data
    with open(jpeg_file, 'rb') as f_jpeg:
        jpeg_data = f_jpeg.read()

    # Ensure we have a valid SOI marker in the JPEG data
    start_soi = jpeg_data.find(b'\xFF\xD8')
    if start_soi == -1:
        raise ValueError("Invalid JPEG file: SOI marker not found.")

    # Separate the JPEG into:
    #   - everything up to and including SOI
    #   - the remainder after SOI
    soi_part = jpeg_data[:start_soi + 2]
    remainder = jpeg_data[start_soi + 2:]

    # Merge into a proper JFIF: SOI first, then JFIF segment, then the rest of JPEG
    merged_data = soi_part + jfif_data + remainder

    base_name = os.path.splitext(jfif_file)[0]
    merged_path = f"{base_name}.jfif"
    with open(merged_path, 'wb') as f_out:
        f_out.write(merged_data)

    print(f"Merged JFIF saved to {merged_path}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print("Usage: python merge_jfif_jpeg.py <file.jfif_data> <file.jpg>")
    else:
        merge_jfif_jpeg(sys.argv[1], sys.argv[2])
