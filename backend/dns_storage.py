import json
import os

class DNSStorage:
    def __init__(self, filename="dns_records.json"):
        self.filename = filename
        self.records = {}
        self.load_records()  # Load data when initialized

    def load_records(self):
        """
        Initialize in-memory storage.

        Persistent storage to disk has been disabled to ensure each user
        only sees their own DNS records (which are now stored in the browser's
        localStorage via the frontend).
        """
        self.records = {}
        # No file access – records start empty on every server start.

    def save_records(self):
        """Persistence disabled – records are kept only in memory."""
        # Intentionally do nothing
        pass

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
