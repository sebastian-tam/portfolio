#!/usr/bin/env python3
"""
Export E-Commerce Hyper-Growth Blueprint PowerPoint to high-resolution JPEGs
"""

import subprocess
import os
from pathlib import Path
import tempfile
import shutil

def export_pptx_with_libreoffice(pptx_path, output_dir):
    """Convert PowerPoint to JPEGs using LibreOffice + PDF + pdfrw"""
    print(f"Converting PowerPoint to JPEGs...")

    temp_dir = tempfile.mkdtemp()
    try:
        # Convert PPTX to PDF using LibreOffice
        libreoffice_path = '/opt/homebrew/bin/soffice'

        if not os.path.exists(libreoffice_path):
            print("Error: LibreOffice not found")
            return 0

        print("Converting to PDF...")
        cmd = [
            libreoffice_path,
            '--headless',
            '--convert-to', 'pdf',
            '--outdir', temp_dir,
            pptx_path
        ]
        subprocess.run(cmd, check=True, capture_output=True, timeout=120)

        pdf_path = os.path.join(temp_dir, Path(pptx_path).stem + '.pdf')
        if not os.path.exists(pdf_path):
            print("Error: PDF conversion failed")
            return 0

        print(f"✓ PDF created: {pdf_path}")

        # Convert PDF to JPEGs using pdf2image
        print("Converting PDF to JPEGs...")
        from pdf2image import convert_from_path

        images = convert_from_path(pdf_path, dpi=150)

        for i, image in enumerate(images, 1):
            jpeg_path = os.path.join(output_dir, f"slide_{i:02d}.jpg")
            image.save(jpeg_path, 'JPEG', quality=85, optimize=True)
            width, height = image.size
            file_size = os.path.getsize(jpeg_path) / 1024
            print(f"✓ Slide {i}: {width}x{height}, {file_size:.1f}KB")

        return len(images)

    except Exception as e:
        print(f"Error: {e}")
        return 0
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)

def main():
    pptx_file = '/Users/sebastiantam/Desktop/E-Commerce_Hyper-Growth_Blueprint_(7).pptx'
    output_dir = '/Users/sebastiantam/portfolio/anymind-seo'

    if not os.path.exists(pptx_file):
        print(f"Error: PowerPoint file not found at {pptx_file}")
        return

    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    print(f"Output directory: {output_dir}\n")

    # Export slides
    num_slides = export_pptx_with_libreoffice(pptx_file, output_dir)

    if num_slides > 0:
        print(f"\n✓ Successfully exported {num_slides} slides to {output_dir}")
    else:
        print(f"\n✗ Failed to export slides")

if __name__ == '__main__':
    main()
