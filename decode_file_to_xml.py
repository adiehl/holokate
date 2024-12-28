#!/usr/bin/env python3
import os
import sys
import xml.etree.ElementTree as ET

def decode_jfif_to_xml(jfif_file):
    with open(jfif_file, 'rb') as f:
        data = f.read()

    # Locate the JFIF marker (APP0) and its length
    app0_marker = data.find(b'\xFF\xE0')
    if app0_marker == -1:
        raise ValueError("No JFIF (APP0) marker found.")

    segment_length = int.from_bytes(data[app0_marker+2:app0_marker+4], byteorder='big')
    jfif_segment = data[app0_marker+4 : app0_marker+4+segment_length-2]
    # The segment_length includes the 2 bytes for the length field,
    # so the payload is (segment_length - 2).

    # JFIF segment structure (minimally):
    #   "JFIF\x00" (5 bytes + null terminator => 6 bytes)
    #   version_major (1 byte)
    #   version_minor (1 byte)
    #   density_units (1 byte)
    #   Xdensity (2 bytes)
    #   Ydensity (2 bytes)
    #   Xthumbnail (1 byte)
    #   Ythumbnail (1 byte)
    #   <thumbnail data, if any>
    #
    # Here we extract the first 14 bytes after the "JFIF\x00" signature
    # ignoring any thumbnail data for simplicity.

    # First 6 bytes must be "JFIF\x00"
    if not jfif_segment.startswith(b'JFIF\x00'):
        raise ValueError("Invalid JFIF header signature.")

    version_major = jfif_segment[6]
    version_minor = jfif_segment[7]
    density_units = jfif_segment[8]
    x_density = int.from_bytes(jfif_segment[9:11], byteorder='big')
    y_density = int.from_bytes(jfif_segment[11:13], byteorder='big')
    x_thumb = jfif_segment[13]
    y_thumb = jfif_segment[14] if len(jfif_segment) > 14 else 0  # in case no byte is present

    # Build XML
    root = ET.Element("jfif")
    ET.SubElement(root, "version_major").text = str(version_major)
    ET.SubElement(root, "version_minor").text = str(version_minor)
    ET.SubElement(root, "density_units").text = str(density_units)
    ET.SubElement(root, "x_density").text = str(x_density)
    ET.SubElement(root, "y_density").text = str(y_density)
    ET.SubElement(root, "x_thumbnail").text = str(x_thumb)
    ET.SubElement(root, "y_thumbnail").text = str(y_thumb)

    # Write XML
    tree = ET.ElementTree(root)
    base_name = os.path.splitext(jfif_file)[0]
    xml_output = f"{base_name}.xml"
    tree.write(xml_output, encoding='utf-8', xml_declaration=True)
    print(f"JFIF metadata saved to {xml_output}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python decode_jfif_to_xml.py <file.jfif>")
        sys.exit(1)
    decode_jfif_to_xml(sys.argv[1])

