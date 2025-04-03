class TrieNode:
    def __init__(self, label="", is_end=False):
        self.label = label
        self.children = {}
        self.is_end = is_end
        self.ip_address = None


class CompressedTrie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, domain, ip_address):
        parts = domain.split('.')[::-1]  # Reverse for TLD-first storage
        node = self.root
        
        for part in parts:
            if part in node.children:
                node = node.children[part]
            else:
                # Check for common prefixes
                to_split = None
                for key in list(node.children.keys()):
                    common_prefix = self._longest_common_prefix(key, part)
                    
                    if common_prefix and (common_prefix == key or common_prefix == part):
                        # Exact match with existing key or new part
                        if common_prefix == key:
                            # The new part contains the existing key as prefix
                            node = node.children[key]
                            remaining = part[len(common_prefix):]
                            if remaining:
                                node.children[remaining] = TrieNode(label=remaining)
                                node = node.children[remaining]
                        else:
                            # The existing key contains the new part as prefix
                            remaining = key[len(common_prefix):]
                            # Create a new node for the existing part
                            new_node = TrieNode(label=part)
                            node.children[part] = new_node
                            # Move existing node under the new one with the remaining suffix
                            if remaining:
                                new_node.children[remaining] = node.children[key]
                                node.children.pop(key)
                            node = new_node
                        to_split = True
                        break
                    elif common_prefix:
                        to_split = key
                        break

                if to_split and to_split is not True:
                    # Split the existing node
                    existing_suffix = to_split[len(common_prefix):]
                    new_suffix = part[len(common_prefix):]
                    
                    # Create a new node for the common prefix
                    prefix_node = TrieNode(label=common_prefix)
                    
                    # Create a new node for the existing suffix
                    existing_node = node.children[to_split]
                    existing_suffix_node = TrieNode(label=existing_suffix, 
                                                   is_end=existing_node.is_end)
                    existing_suffix_node.children = existing_node.children
                    existing_suffix_node.ip_address = existing_node.ip_address
                    
                    # Remove old node and add new prefix node
                    node.children.pop(to_split)
                    node.children[common_prefix] = prefix_node
                    
                    # Add both suffixes under the prefix node
                    prefix_node.children[existing_suffix] = existing_suffix_node
                    
                    # Insert new suffix if it exists
                    if new_suffix:
                        prefix_node.children[new_suffix] = TrieNode(label=new_suffix)
                        node = prefix_node.children[new_suffix]
                    else:
                        node = prefix_node
                        # If no new suffix, this is the end of a domain
                        node.is_end = True
                elif not to_split:
                    # No common prefix found, create a new node
                    node.children[part] = TrieNode(label=part)
                    node = node.children[part]

        # Mark the final node as the end of a domain
        node.is_end = True
        node.ip_address = ip_address

    def _longest_common_prefix(self, str1, str2):
        """Finds the longest common prefix between two strings."""
        min_length = min(len(str1), len(str2))
        for i in range(min_length):
            if str1[i] != str2[i]:
                return str1[:i]
        return str1[:min_length]
    
    def lookup(self, domain):
        parts = domain.split('.')[::-1]  # Reverse for TLD-first storage
        return self._lookup_recursive(self.root, parts, 0)
    
    def _lookup_recursive(self, node, parts, index):
        if index == len(parts):
            # We've reached the end of the domain parts
            return node.ip_address if node.is_end else "Not Found"
        
        current_part = parts[index]
        
        # Try to find an exact match first
        if current_part in node.children:
            return self._lookup_recursive(node.children[current_part], parts, index + 1)
        
        # Check for compressed nodes (partial matches)
        for key in node.children:
            if key.startswith(current_part) or current_part.startswith(key):
                # If key is a prefix of current_part or vice versa
                if current_part.startswith(key):
                    # The trie key is a prefix of our current part
                    remaining = current_part[len(key):]
                    if remaining in node.children[key].children:
                        return self._lookup_recursive(node.children[key].children[remaining], 
                                                    parts, index + 1)
                elif key.startswith(current_part):
                    # Our current part is a prefix of the trie key
                    if index == len(parts) - 1 and node.children[key].is_end:
                        # If this is the last part and the node is an end
                        return node.children[key].ip_address
        
        return "Not Found"

    def print_trie(self):
        self._print_trie(self.root, "", "")

    def _print_trie(self, node, prefix, branch):
        if node.label:
            ip_info = f" → {node.ip_address}" if node.ip_address else ""
            end_marker = " (end)" if node.is_end else ""
            print(f"{prefix}{branch}{node.label}{ip_info}{end_marker}")
            prefix += "│   " if len(node.children) > 0 else "    "
        
        children = sorted(node.children.keys())
        for i, key in enumerate(children):
            is_last = (i == len(children) - 1)
            branch = '└── ' if is_last else '├── '
            self._print_trie(node.children[key], prefix, branch)


# # Test the implementation
# if __name__ == "__main__":
#     trie = CompressedTrie()
    
#     # Insert test domains
#     trie.insert("go.com", "1.1.1.1")
#     trie.insert("google.com", "8.8.8.8")
#     trie.insert("golang.com", "2.2.2.2")

#     print("\nTrie structure:")
#     trie.print_trie()
    
#     print("\nLookup tests:")
#     print(f"go.com → {trie.lookup('go.com')}")
#     print(f"google.com → {trie.lookup('google.com')}")
#     print(f"golang.com → {trie.lookup('golang.com')}")
#     print(f"unknown.com → {trie.lookup('unknown.com')}")