#!/usr/bin/env python3
"""
extract_docx_images.py
----------------------
Extracts all images from a .docx file in the exact order they appear
in the document and saves them to an `img/` folder named:
    image1.<ext>, image2.<ext>, image3.<ext>, ...

Usage:
    python extract_docx_images.py <path_to_file.docx> [--out <output_dir>]

Examples:
    python extract_docx_images.py report.docx
    python extract_docx_images.py report.docx --out ./my_images
"""

import argparse
import os
import shutil
import sys
import zipfile
from xml.etree import ElementTree as ET

# ── XML namespaces used inside a .docx ──────────────────────────────────────
NS = {
    "a":   "http://schemas.openxmlformats.org/drawingml/2006/main",
    "pic": "http://schemas.openxmlformats.org/drawingml/2006/picture",
    "r":   "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
    "v":   "urn:schemas-microsoft-com:vml",
    "w":   "http://schemas.openxmlformats.org/wordprocessingml/2006/main",
    "wp":  "http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing",
}


def get_rel_target(rels_xml: bytes, r_id: str) -> str | None:
    """Return the Target path for a given relationship Id."""
    root = ET.fromstring(rels_xml)
    for rel in root:
        if rel.get("Id") == r_id:
            return rel.get("Target")
    return None


def collect_image_rids_in_order(document_xml: bytes) -> list[str]:
    """
    Walk document.xml and return relationship IDs (rId…) for every
    image reference, in the order they appear in the document.
    Covers both modern <w:drawing> blocks and legacy <v:imagedata> elements.
    """
    root = ET.fromstring(document_xml)
    rids: list[str] = []

    for elem in root.iter():
        tag = elem.tag

        # Modern inline / floating images  →  <a:blip r:embed="rIdN"/>
        if tag == f"{{{NS['a']}}}blip":
            rid = elem.get(f"{{{NS['r']}}}embed")
            if rid:
                rids.append(rid)

        # Legacy VML images  →  <v:imagedata r:id="rIdN"/>
        elif tag == f"{{{NS['v']}}}imagedata":
            rid = elem.get(f"{{{NS['r']}}}id")
            if rid:
                rids.append(rid)

    return rids


def extract_images(docx_path: str, output_dir: str) -> None:
    if not os.path.isfile(docx_path):
        sys.exit(f"[ERROR] File not found: {docx_path}")

    if not zipfile.is_zipfile(docx_path):
        sys.exit(f"[ERROR] Not a valid .docx (ZIP) file: {docx_path}")

    img_dir = os.path.join(output_dir, "img")
    os.makedirs(img_dir, exist_ok=True)

    with zipfile.ZipFile(docx_path, "r") as zf:
        names = zf.namelist()

        # ── Load document.xml ────────────────────────────────────────────────
        if "word/document.xml" not in names:
            sys.exit("[ERROR] word/document.xml not found — is this a valid .docx?")
        document_xml = zf.read("word/document.xml")

        # ── Load the relationships file ──────────────────────────────────────
        rels_path = "word/_rels/document.xml.rels"
        if rels_path not in names:
            sys.exit(f"[ERROR] {rels_path} not found.")
        rels_xml = zf.read(rels_path)

        # ── Get image rIds in document order ─────────────────────────────────
        rids_in_order = collect_image_rids_in_order(document_xml)

        if not rids_in_order:
            print("[INFO] No images found in the document.")
            return

        # ── Resolve each rId → media path ────────────────────────────────────
        saved = 0
        for rid in rids_in_order:
            target = get_rel_target(rels_xml, rid)
            if target is None:
                print(f"[WARN] No relationship found for rId: {rid} — skipping.")
                continue

            # Relationships use paths relative to word/
            if not target.startswith("/"):
                media_path = "word/" + target.lstrip("./")
            else:
                media_path = target.lstrip("/")

            if media_path not in names:
                print(f"[WARN] Media file not found in archive: {media_path} — skipping.")
                continue

            # Derive extension from the original filename
            _, ext = os.path.splitext(media_path)
            ext = ext.lower() if ext else ".bin"

            # Skip non-image entries (e.g. embedded EMF/WMF chart images)
            image_exts = {".png", ".jpg", ".jpeg", ".gif", ".bmp", ".tiff",
                          ".tif", ".webp", ".emf", ".wmf", ".svg"}
            if ext not in image_exts:
                print(f"[SKIP] Non-image media skipped: {media_path}")
                continue

            saved += 1
            out_name = f"image{saved}{ext}"
            out_path = os.path.join(img_dir, out_name)

            with zf.open(media_path) as src, open(out_path, "wb") as dst:
                shutil.copyfileobj(src, dst)

            print(f"  [{saved}] {media_path}  →  img/{out_name}")

    if saved:
        print(f"\n✅  {saved} image(s) saved to: {os.path.abspath(img_dir)}/")
    else:
        print("[INFO] No supported image formats were extracted.")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Extract images from a .docx file in document order."
    )
    parser.add_argument("docx", help="Path to the .docx file")
    parser.add_argument(
        "--out",
        default=".",
        metavar="DIR",
        help="Directory where the img/ folder will be created (default: current directory)",
    )
    args = parser.parse_args()
    extract_images(args.docx, args.out)


if __name__ == "__main__":
    main()