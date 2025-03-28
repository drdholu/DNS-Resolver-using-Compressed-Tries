# DNS Resolver with Compressed Trie

A fast and efficient DNS resolution system implemented using a Compressed Trie data structure. This project provides a RESTful API for domain name resolution with persistent storage capabilities.

## Features

- Fast domain name lookups using Compressed Trie (O(k) complexity)
- RESTful API endpoints for DNS resolution
- Persistent storage for domain-IP mappings
- Automatic random IP generation for new domains
- Simple and lightweight implementation

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/dns-resolver.git
cd dns-resolver
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Start the server:
```bash
python app.py
```

2. The API will be available at `http://localhost:5000`

### API Endpoints

#### Resolve Domain
```
GET /resolve?domain=example.com
```
Returns the IP address for the given domain.

#### Store Domain
```
POST /store
Content-Type: application/json
{
    "domain": "example.com"
}
```
Stores a new domain with a randomly generated IP.

## Example Response

```json
{
    "domain": "example.com",
    "ip": "192.168.1.1"
}
```