#!/usr/bin/env python3
import os
import sys
import xml.etree.ElementTree as ET

def merge_xml_jpeg(xml_file, jpeg_file):
    # Load XML metadata
    tree = ET.parse(xml_file)
    root = tree.getroot()

    # Extract fields
    version_major = int(root.find("version_major").text)
    version_minor = int(root.find("version_minor").text)
    density_units = int(root.find("density_units").text)
    x_density = int(root.find("x_density").text)
    y_density = int(root.find("y_density").text)
    x_thumb = int(root.find("x_thumbnail").text)
    y_thumb = int(root.find("y_thumbnail").text)

    # Construct minimal JFIF segment (APP0)
    # JFIF segment length is (16) if ignoring thumbnails:
    #   2 bytes for segment length itself
    #   14 bytes for "JFIF\x00" + version + units + densities + thumbnails
    #
    #   Marker: 0xFFE0
    #   Length: 16 (0x0010)
    #   "JFIF\x00"
    #   version_major (1 byte)
    #   version_minor (1 byte)
    #   density_units (1 byte)
    #   x_density (2 bytes)
    #   y_density (2 bytes)
    #   x_thumb (1 byte)
    #   y_thumb (1 byte)

    segment_marker = b'\xFF\xE0'
    segment_length = (16).to_bytes(2, 'big')  # 0x0010

    jfif_id = b'JFIF\x00'
    v_major = version_major.to_bytes(1, 'big')
    v_minor = version_minor.to_bytes(1, 'big')
    dens_unit = density_units.to_bytes(1, 'big')
    x_dens = x_density.to_bytes(2, 'big')
    y_dens = y_density.to_bytes(2, 'big')
    x_t = x_thumb.to_bytes(1, 'big')
    y_t = y_thumb.to_bytes(1, 'big')

    # Combine to build the JFIF segment
    jfif_segment = (
        segment_marker +
        segment_length +
        jfif_id +
        v_major +
        v_minor +
        dens_unit +
        x_dens +
        y_dens +
        x_t +
        y_t
    )

    # Read the JPEG file
    with open(jpeg_file, 'rb') as f_jpeg:
        jpeg_data = f_jpeg.read()

    # Find SOI marker to insert after
    start_soi = jpeg_data.find(b'\xFF\xD8')
    if start_soi == -1:
        raise ValueError("Invalid JPEG file: SOI marker not found.")

    # The segment goes immediately after the 2-byte SOI marker
    soi_part = jpeg_data[:start_soi + 2]
    remainder = jpeg_data[start_soi + 2:]

    # Merge
    merged_data = soi_part + jfif_segment + remainder

    # Save the output
    base_name = os.path.splitext(xml_file)[0]
    merged_filename = f"{base_name}_merged.jpg"
    with open(merged_filename, 'wb') as f_out:
        f_out.write(merged_data)

    print(f"Merged JFIF-encoded JPEG saved to {merged_filename}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python merge_xml_jpeg.py <file.xml> <file.jpg>")
        sys.exit(1)
    merge_xml_jpeg(sys.argv[1], sys.argv[2])

