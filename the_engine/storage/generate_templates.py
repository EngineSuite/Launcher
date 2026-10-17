"""Helper to generate 25 verified industry templates for SchemaCraft Agency Pro"""
import json
from pathlib import Path

TEMPLATES = {
    "dentist": {"@type": "Dentist", "name": "Precision Dental Care", "priceRange": "$$", "currenciesAccepted": "USD", "paymentAccepted": "Cash, Credit Card, Insurance"},
    "attorney": {"@type": "Attorney", "name": "Sterling Legal Counsel", "priceRange": "$$$", "currenciesAccepted": "USD"},
    "plumber": {"@type": "Plumber", "name": "Rapid Rooter Plumbing", "priceRange": "$$", "currenciesAccepted": "USD"},
    "restaurant": {"@type": "Restaurant", "name": "Bistro Bella Vita", "priceRange": "$$", "servesCuisine": ["Italian", "Mediterranean"], "acceptsReservations": "True"},
    "real_estate_agent": {"@type": "RealEstateAgent", "name": "Summit Realty Group", "priceRange": "$$$"},
    "medical_clinic": {"@type": "MedicalClinic", "name": "Beacon Urgent Care & Clinic", "medicalSpecialty": "PrimaryCare"},
    "auto_repair": {"@type": "AutoRepair", "name": "MasterTech Auto Repair", "priceRange": "$$"},
    "roofing_contractor": {"@type": "RoofingContractor", "name": "Pinnacle Roofing Solutions", "priceRange": "$$"},
    "hvac_contractor": {"@type": "HVACBusiness", "name": "Comfort Air HVAC Pros", "priceRange": "$$"},
    "veterinary_care": {"@type": "VeterinaryCare", "name": "Companion Animal Hospital", "priceRange": "$$"},
    "accountant": {"@type": "AccountingService", "name": "Vanguard Tax & Accounting", "priceRange": "$$"},
    "fitness_center": {"@type": "HealthClub", "name": "Apex Strength & Fitness", "priceRange": "$$"},
    "hair_salon": {"@type": "HairSalon", "name": "Lumiere Hair Studio", "priceRange": "$$"},
    "hotel": {"@type": "Hotel", "name": "The Grand Heritage Hotel", "priceRange": "$$$", "starRating": {"@type": "Rating", "ratingValue": "4.5"}},
    "electrician": {"@type": "Electrician", "name": "VoltCraft Electrical Services", "priceRange": "$$"},
    "locksmith": {"@type": "Locksmith", "name": "QuickKey 24/7 Locksmith", "priceRange": "$$"},
    "child_care": {"@type": "ChildCare", "name": "Bright Futures Early Learning", "priceRange": "$$"},
    "cleaning_service": {"@type": "HousePainter", "name": "SparkleClean Commercial Services", "priceRange": "$$"},
    "optician": {"@type": "Optician", "name": "ClearView Optometry & Eyewear", "priceRange": "$$"},
    "moving_company": {"@type": "MovingCompany", "name": "ReloPro Movers", "priceRange": "$$"},
    "insurance_agency": {"@type": "InsuranceAgency", "name": "Sentinel Shield Insurance", "priceRange": "$$"},
    "saas_company": {"@type": "SoftwareApplication", "name": "CloudMetric Analytics", "applicationCategory": "BusinessApplication", "operatingSystem": "Web"},
    "ecommerce_product": {"@type": "Product", "name": "ErgoPro Dynamic Desk", "brand": {"@type": "Brand", "name": "ErgoWorks"}, "offers": {"@type": "Offer", "price": "499.00", "priceCurrency": "USD"}},
    "event_venue": {"@type": "EventVenue", "name": "The Metropolitan Ballroom", "maximumAttendeeCapacity": 500},
    "course_education": {"@type": "Course", "name": "Zero-Cost Cloud Mastery", "description": "Master serverless architecture without cloud bills.", "provider": {"@type": "Organization", "name": "CloudZero Institute"}}
}

dest_dir = Path("nodes/node_schemacraft_pro/dist_pack/templates")
dest_dir.mkdir(parents=True, exist_ok=True)

for slug, data in TEMPLATES.items():
    base = {
        "@context": "https://schema.org",
        "url": f"https://{slug}.example.com",
        "telephone": "+1-555-010-0000",
        "address": {
            "@type": "PostalAddress",
            "streetAddress": "100 Main Street",
            "addressLocality": "Austin",
            "addressRegion": "TX",
            "postalCode": "78701",
            "addressCountry": "US"
        },
        "geo": {
            "@type": "GeoCoordinates",
            "latitude": 30.2672,
            "longitude": -97.7431
        },
        "openingHours": ["Mo-Fr 08:00-18:00"],
        "aggregateRating": {
            "@type": "AggregateRating",
            "ratingValue": 4.9,
            "reviewCount": 120
        }
    }
    base.update(data)
    with open(dest_dir / f"{slug}.json", "w", encoding="utf-8") as f:
        json.dump(base, f, indent=2)

print(f"Generated {len(TEMPLATES)} industry templates in {dest_dir}")
