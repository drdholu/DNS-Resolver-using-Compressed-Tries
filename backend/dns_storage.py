import json
import os

class DNSStorage:
    def __init__(self, filename="dns_records.json"):
        self.filename = filename
        self.records = {}
        self.load_records()  # Load data when initialized

    def load_records(self):
        """Load stored DNS records from file into memory."""
        if os.path.exists(self.filename):  # Check if file exists
            try:
                with open(self.filename, "r") as file:
                    self.records = json.load(file)  # Load JSON data
                print("DNS records loaded successfully.")
            except json.JSONDecodeError:
                print("Error reading DNS records. Starting with an empty database.")
                self.records = {}  # If corrupted, start fresh
        else:
            print("No existing DNS records found. Starting fresh.")

    def save_records(self):
        """Save current DNS records to file."""
        with open(self.filename, "w") as file:
            json.dump(self.records, file, indent=4)  # Save as formatted JSON
        print("DNS records saved successfully.")

    def add_record(self, domain, ip):
        """Add a new DNS record and save to file."""
        self.records[domain] = ip
        self.save_records()  # Save changes immediately

    def get_record(self, domain):
        """Retrieve an IP address for a domain."""
        return self.records.get(domain, "Not Found")

    def delete_record(self, domain):
        """Delete a DNS record and update storage."""
        if domain in self.records:
            del self.records[domain]
            self.save_records()
            return True
        return False
    
    def import_records(self, import_file):
        """Import multiple DNS records from a JSON file."""
        if os.path.exists(import_file):
            try:
                with open(import_file, "r") as file:
                    new_records = json.load(file)
                self.records.update(new_records)  # Merge with existing records
                self.save_records()  # Save updated data
                print(f"Successfully imported {len(new_records)} DNS records.")
            except json.JSONDecodeError:
                print("Error reading import file.")
        else:
            print("Import file not found.")

    def export_records(self, export_file):
        """Export current DNS records to a JSON file."""
        with open(export_file, "w") as file:
            json.dump(self.records, file, indent=4)
        print(f"Successfully exported {len(self.records)} DNS records.")
