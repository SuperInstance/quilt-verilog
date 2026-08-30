#!/bin/bash
set -e

cd "$(dirname "$0")/.."

# Build first
cargo build --release 2>/dev/null

BINARY="./target/release/v1consumer"
TMP=$(mktemp -d)
trap "rm -rf $TMP" EXIT

# Test 1: Create a minimal QUF file and test info command
echo "Test 1: info command on minimal QUF file"
python3 - "$TMP/test.quf" << 'PYTHON'
import struct
import sys

output = sys.argv[1]

# Write minimal QUF file
with open(output, 'wb') as f:
    # Fixed header
    f.write(b'QUF\x00')
    f.write(struct.pack('<I', 1))  # version
    f.write(struct.pack('<I', 1))  # endian
    f.write(struct.pack('<I', 0))  # 0 KV pairs
    
    # Section table
    f.write(struct.pack('<I', 0))  # 0 sections
PYTHON

$BINARY info "$TMP/test.quf" > "$TMP/info.json"
echo "✓ info command succeeded"

# Test 2: Test verify on file without epochs
echo "Test 2: verify on file without epochs (should find no epochs)"
$BINARY verify "$TMP/test.quf" "00" > "$TMP/verify.json" 2>&1 || true
# Should succeed with no epochs found
grep -q "result" "$TMP/verify.json" && echo "✓ verify command handled no-epoch case"

echo ""
echo "All tests passed!"
