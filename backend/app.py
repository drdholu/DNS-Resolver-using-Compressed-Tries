from flask import Flask, request, jsonify
from flask_cors import CORS
from dns_resolver import DNSResolver
import random
import socket

app = Flask(__name__)
CORS(app)
resolver = DNSResolver()

def generate_random_ip():
    """Generate a random IP address."""
    return f"{random.randint(1, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}"

@app.route('/resolve', methods=['GET'])
def resolve_domain():
    """API endpoint to resolve a domain name."""
    domain = request.args.get('domain')
    if not domain:
        return jsonify({"error": "Domain parameter is required"}), 400

    ip_address = resolver.resolve(domain)
    if ip_address == "Not Found":
        try:
            # Fetch actual IP address
            ip_address = socket.gethostbyname(domain)
            resolver.storage.add_record(domain, ip_address)
            resolver.trie.insert(domain, ip_address)
            return jsonify({"domain": domain, "ip": ip_address, "note": "Fetched IP address"})
        except socket.gaierror:
            return jsonify({"error": "Domain not found"}), 404
    
    return jsonify({"domain": domain, "ip": ip_address})

@app.route('/store', methods=['POST'])
def store_domain():
    """Store a domain resolution result."""
    data = request.json
    if not data or 'domain' not in data:
        return jsonify({"error": "Domain is required"}), 400

    domain = data['domain']
    random_ip = generate_random_ip()
    resolver.storage.add_record(domain, random_ip)
    resolver.trie.insert(domain, random_ip)
    return jsonify({"message": f"Stored random IP {random_ip} for {domain}"}), 200

@app.route('/trie', methods=['GET'])
def get_trie_structure():
    """Return the trie structure for visualization."""
    trie_data = serialize_trie(resolver.trie.root)
    return jsonify(trie_data)

def serialize_trie(node, label="root"):
    """Convert trie node to a serializable format for visualization."""
    result = {
        "name": label,
        "attributes": {}
    }
    
    if node.is_end:
        result["attributes"]["ip"] = node.ip_address
        result["attributes"]["isEnd"] = True
    
    if node.children:
        result["children"] = []
        for key, child in node.children.items():
            result["children"].append(serialize_trie(child, key))
    
    return result

if __name__ == '__main__':
    app.run(debug=True)

"""
1. User types "google.com"
2. Frontend calls GET /resolve?domain=google.com
3. Backend checks Trie and Storage
4. If found: returns existing IP
5. If not found: fetches actual IP, stores it, updates Trie
6. Frontend displays result and updates visualization
"""