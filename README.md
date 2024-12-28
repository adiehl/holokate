# JFIF Utility Scripts

A small collection of scripts for handling JFIF metadata. This open-source project is licensed under the [GNU General Public License (GPL)](https://www.gnu.org/licenses/gpl-3.0.html).

## Overview

1. **`extract_jfif_jpeg.py`**  
   Splits a JFIF file into two parts:  
   - Extracted JFIF segment (`.jfif_data`)  
   - Full JPEG image (`.jpg`)

2. **`merge_jfif_jpeg.py`**  
   Reconstructs a valid JFIF file by merging a JFIF segment (`.jfif_data`) with a JPEG image (`.jpg`).

3. **`decode_jfif_to_xml.py`**  
   Reads the JFIF segment from a JFIF file, extracts metadata (version, densities, etc.) and saves it as XML.

4. **`merge_xml_jpeg.py`**  
   Combines JFIF metadata (from an XML file) with a JPEG image to produce a valid JFIF-encoded JPEG.

---

## Installation

1. Clone or download this repository.
2. Ensure Python 3 is installed on your system.

```bash
git clone https://github.com/<your-username>/jfif-utility-scripts.git
cd jfif-utility-scripts

