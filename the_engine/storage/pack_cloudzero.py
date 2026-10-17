"""Packages CloudZero Production Kit into a downloadable zip file"""
import zipfile
from pathlib import Path

source_dir = Path("nodes/node_dev_cheatsheet_vault/dist_pack")
dest_dir = Path("nodes/node_dev_cheatsheet_vault/public/downloads")
dest_dir.mkdir(parents=True, exist_ok=True)
dest_zip = dest_dir / "cloudzero-production-kit.zip"

with zipfile.ZipFile(dest_zip, "w", zipfile.ZIP_DEFLATED) as zip_file:
    for file in source_dir.rglob("*"):
        if file.is_file():
            arcname = file.relative_to(source_dir)
            zip_file.write(file, arcname)

print(f"✓ Created {dest_zip} ({dest_zip.stat().st_size} bytes)")
