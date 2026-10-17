#!/usr/bin/env python3
"""
SchemaCraft Agency Pro - Bulk JSON-LD Generator CLI
Transforms CSV/Spreadsheet multi-location data into 100% Google-compliant Schema.org JSON-LD.

Usage:
    python bulk_generator.py input_locations.csv --output-dir ./dist_schemas/
    python bulk_generator.py input_locations.csv --combined-feed ./all_locations_schema.json
"""

import csv
import json
import argparse
import sys
from pathlib import Path
from typing import Dict, Any, List


def generate_location_schema(row: Dict[str, str]) -> Dict[str, Any]:
    """Converts a single CSV row into a complete Schema.org LocalBusiness JSON-LD structure."""
    category = row.get("category", "").strip() or "LocalBusiness"
    name = row.get("name", "").strip()
    url = row.get("url", "").strip()
    phone = row.get("phone", "").strip()
    street = row.get("street", "").strip()
    city = row.get("city", "").strip()
    region = row.get("region", "").strip()
    postal_code = row.get("postal_code", "").strip()
    country = row.get("country", "").strip() or "US"
    price_range = row.get("price_range", "").strip() or "$$"
    rating = row.get("rating", "").strip()
    review_count = row.get("review_count", "").strip()
    latitude = row.get("latitude", "").strip()
    longitude = row.get("longitude", "").strip()
    opening_hours = row.get("opening_hours", "").strip()

    schema: Dict[str, Any] = {
        "@context": "https://schema.org",
        "@type": category,
        "name": name,
        "url": url,
        "telephone": phone,
        "priceRange": price_range,
        "address": {
            "@type": "PostalAddress",
            "streetAddress": street,
            "addressLocality": city,
            "addressRegion": region,
            "postalCode": postal_code,
            "addressCountry": country
        }
    }

    if latitude and longitude:
        schema["geo"] = {
            "@type": "GeoCoordinates",
            "latitude": float(latitude),
            "longitude": float(longitude)
        }

    if opening_hours:
        schema["openingHours"] = [h.strip() for h in opening_hours.split(";") if h.strip()]

    if rating and review_count:
        try:
            schema["aggregateRating"] = {
                "@type": "AggregateRating",
                "ratingValue": float(rating),
                "reviewCount": int(review_count)
            }
        except ValueError:
            pass

    return schema


def process_csv(csv_path: Path, output_dir: Path = None, combined_feed: Path = None) -> List[Dict[str, Any]]:
    if not csv_path.exists():
        print(f"Error: CSV file not found at {csv_path}", file=sys.stderr)
        sys.exit(1)

    schemas = []
    with open(csv_path, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader, 1):
            if not row.get("name"):
                continue
            schema = generate_location_schema(row)
            schemas.append(schema)

            if output_dir:
                output_dir.mkdir(parents=True, exist_ok=True)
                slug = "".join(c if c.isalnum() else "_" for c in row.get("name", f"location_{i}")).lower()
                dest_file = output_dir / f"{slug}_schema.json"
                with open(dest_file, "w", encoding="utf-8") as out_f:
                    json.dump(schema, out_f, indent=2)

    if combined_feed:
        combined_feed.parent.mkdir(parents=True, exist_ok=True)
        # Google accepts an array of objects or an @graph container
        feed_structure = {
            "@context": "https://schema.org",
            "@graph": schemas
        }
        with open(combined_feed, "w", encoding="utf-8") as out_f:
            json.dump(feed_structure, out_f, indent=2)

    return schemas


def main():
    parser = argparse.ArgumentParser(description="SchemaCraft Agency Pro: Bulk Schema.org JSON-LD Generator")
    parser.add_argument("csv_file", type=str, help="Path to input CSV file")
    parser.add_argument("--output-dir", type=str, default=None, help="Directory to save individual JSON files")
    parser.add_argument("--combined-feed", type=str, default=None, help="Output path for single combined @graph JSON feed")

    args = parser.parse_args()
    csv_file = Path(args.csv_file)
    output_dir = Path(args.output_dir) if args.output_dir else None
    combined_feed = Path(args.combined_feed) if args.combined_feed else None

    if not output_dir and not combined_feed:
        output_dir = Path("./generated_schemas")

    schemas = process_csv(csv_file, output_dir=output_dir, combined_feed=combined_feed)
    print(f"✓ Successfully processed {len(schemas)} location schemas from {csv_file.name}!")
    if output_dir:
        print(f"  • Individual schemas saved to: {output_dir}")
    if combined_feed:
        print(f"  • Combined @graph feed saved to: {combined_feed}")


if __name__ == "__main__":
    main()
