class TrieNode:
    def __init__(self):
        self.children = {}
        self.ip_address = None

class CompressedTrie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, domain, ip_address):
        node = self.root
        parts = domain.split(".")[::-1]

        for part in parts:
            if part not in node.children:
                node.children[part] = TrieNode()
            node = node.children[part]

        node.ip_address = ip_address
        print("inserted in ct")

    def lookup(self, domain):
        node = self.root
        parts = domain.split(".")[::-1]

        for part in parts:
            if part in node.children:
                node = node.children[part]
            else:
                return "Not Found"

        return node.ip_address if node.ip_address else "Not Found"


# trie = CompressedTrie()
# trie.insert("google.com", "8.8.8.8")
# trie.insert("go.com", "1.1.1.1")



# print(trie.lookup("google.com"))  # Output: "8.8.8.8"
# print(trie.lookup("go.com"))      # Output: "1.1.1.1"
# print(trie.lookup("bing.com"))    # Output: "Not Found"
