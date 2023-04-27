from pymerkle import MerkleTree, verify_inclusion, verify_consistency

tree = MerkleTree()

# Populate tree with some entries
for data in [b'foo', b'bar', b'baz', b'qux', b'quux']:
    tree.append_entry(data)
print(tree.root)
# Prove and verify inclusion of `bar`
proof = tree.prove_inclusion(b'baj')
print(proof)
print(verify_inclusion(b'baj', tree.root, proof))

# Save current state
sublength = tree.length
subroot = tree.root

# Append further entries
for data in [b'corge', b'grault', b'garlpy']:
    tree.append_entry(data)

# Prove and verify previous state
proof = tree.prove_consistency(sublength, subroot)
print(verify_consistency(subroot, tree.root, proof))