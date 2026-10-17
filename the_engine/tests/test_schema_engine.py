"""Direct Unit Tests for Schema Engine and Generation Logic"""
import unittest
import sys
from pathlib import Path

# Add node src to path
node_src = Path(__file__).resolve().parent.parent.parent / "nodes" / "node_schemacraft_pro" / "src"
sys.path.insert(0, str(node_src))

from schema_engine import SchemaEngine


class TestSchemaEngine(unittest.TestCase):
    def test_local_business_generation_and_validation(self):
        address = {
            "street": "100 South Congress Ave",
            "city": "Austin",
            "region": "TX",
            "postal_code": "78704",
            "country": "US"
        }
        schema = SchemaEngine.generate_local_business(
            name="Austin Tech Dental",
            category="Dentist",
            url="https://austintechdental.example",
            phone="+1-512-555-0199",
            address=address,
            price_range="$$"
        )
        self.assertEqual(schema["@context"], "https://schema.org")
        self.assertEqual(schema["@type"], "Dentist")
        self.assertEqual(schema["name"], "Austin Tech Dental")
        self.assertEqual(schema["address"]["addressLocality"], "Austin")

        validation = SchemaEngine.validate_schema(schema)
        self.assertTrue(validation["valid"])
        self.assertEqual(len(validation["errors"]), 0)

    def test_faq_generation(self):
        faqs = [
            {"question": "How much does it cost?", "answer": "Starter tier is 100% free forever."},
            {"question": "Is JSON-LD supported?", "answer": "Yes, standard Google JSON-LD schema."}
        ]
        schema = SchemaEngine.generate_faq(faqs)
        self.assertEqual(schema["@type"], "FAQPage")
        self.assertEqual(len(schema["mainEntity"]), 2)
        self.assertEqual(schema["mainEntity"][0]["name"], "How much does it cost?")

        validation = SchemaEngine.validate_schema(schema)
        self.assertTrue(validation["valid"])

    def test_validation_failure_on_invalid_schema(self):
        invalid_schema = {"type": "LocalBusiness", "name": "Broken Schema"}
        validation = SchemaEngine.validate_schema(invalid_schema)
        self.assertFalse(validation["valid"])
        self.assertGreater(len(validation["errors"]), 0)


if __name__ == "__main__":
    unittest.main()
