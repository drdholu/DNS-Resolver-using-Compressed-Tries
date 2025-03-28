from ct import CompressedTrie
from dns_storage import DNSStorage

class DNSResolver:
    def __init__(self):
        self.trie = CompressedTrie()
        self.storage = DNSStorage()  # Load stored data

        # Populate Trie with stored records
        for domain, ip in self.storage.records.items():
            self.trie.insert(domain, ip)

    def resolve(self, domain):
        """Resolve domain using trie or storage."""
        ip = self.trie.lookup(domain)
        if ip != "Not Found":
            return ip

        # Check storage if not in trie
        ip = self.storage.get_record(domain)
        if ip != "Not Found":
            self.trie.insert(domain, ip)  # Update trie for faster access
            return ip
        
        # At this point, domain is truly not found
        # We don't need to do anything here as the frontend will handle storing
        # the not found status through the /store endpoint
        return "Not Found"

