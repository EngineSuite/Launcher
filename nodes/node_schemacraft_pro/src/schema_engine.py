# SchemaCraft Pro - Backend Engine & Validator
import json
from typing import Dict, Any, List

class SchemaEngine:
    @staticmethod
    def generate_local_business(name: str, category: str, url: str, phone: str, 
                                address: Dict[str, str], price_range: str = "$$") -> Dict[str, Any]:
        return {
            "@context": "https://schema.org",
            "@type": category or "LocalBusiness",
            "name": name,
            "url": url,
            "telephone": phone,
            "priceRange": price_range,
            "address": {
                "@type": "PostalAddress",
                "streetAddress": address.get("street", ""),
                "addressLocality": address.get("city", ""),
                "addressRegion": address.get("region", ""),
                "postalCode": address.get("postal_code", ""),
                "addressCountry": address.get("country", "US")
            }
        }

    @staticmethod
    def generate_faq(faq_items: List[Dict[str, str]]) -> Dict[str, Any]:
        return {
            "@context": "https://schema.org",
            "@type": "FAQPage",
            "mainEntity": [
                {
                    "@type": "Question",
                    "name": item["question"],
                    "acceptedAnswer": {
                        "@type": "Answer",
                        "text": item["answer"]
                    }
                }
                for item in faq_items
            ]
        }

    @staticmethod
    def validate_schema(schema: Dict[str, Any]) -> Dict[str, Any]:
        errors = []
        if "@context" not in schema or schema["@context"] != "https://schema.org":
            errors.append("Missing or invalid '@context'. Must be 'https://schema.org'.")
        if "@type" not in schema:
            errors.append("Missing '@type' declaration.")
        
        return {
            "valid": len(errors) == 0,
            "errors": errors,
            "schema_type": schema.get("@type", "Unknown")
        }
