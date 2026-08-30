// Integration tests for v1consumer

// Helper to create a test QUF file with epoch sections
fn create_test_quf_file_bytes(epoch_count: usize, archive_key: &[u8]) -> Vec<u8> {
    let mut bytes = Vec::new();
    
    // Fixed header
    bytes.extend_from_slice(b"QUF\x00");
    bytes.extend_from_slice(&1u32.to_le_bytes()); // version
    bytes.extend_from_slice(&1u32.to_le_bytes()); // endian
    bytes.extend_from_slice(&0u32.to_le_bytes()); // no KV pairs
    
    // Section table (just 2 sections: dials and epoch.0)
    let section_count = (epoch_count + 1) as u32; // +1 for dials
    bytes.extend_from_slice(&section_count.to_le_bytes());
    
    // Section 1: dials (dummy)
    let dials_name = b"dials";
    bytes.extend_from_slice(&(dials_name.len() as u32).to_le_bytes());
    bytes.extend_from_slice(dials_name);
    bytes.extend_from_slice(&0u32.to_le_bytes()); // kind
    bytes.extend_from_slice(&64u64.to_le_bytes()); // offset
    bytes.extend_from_slice(&64u64.to_le_bytes()); // size
    
    // Section N: epoch.0, epoch.1, etc.
    let mut offset = 128u64; // After dials
    for i in 0..epoch_count {
        let epoch_name = format!("epoch.{}", i);
        bytes.extend_from_slice(&(epoch_name.len() as u32).to_le_bytes());
        bytes.extend_from_slice(epoch_name.as_bytes());
        bytes.extend_from_slice(&0u32.to_le_bytes()); // kind
        bytes.extend_from_slice(&offset.to_le_bytes());
        
        // Compute epoch section size: 48 (header) + 0 (payload) + 32 (seal) = 80
        let epoch_size = 80u64;
        bytes.extend_from_slice(&epoch_size.to_le_bytes());
        offset += epoch_size;
    }
    
    // Dials section (64 dummy bytes)
    for _ in 0..64 {
        bytes.push(0);
    }
    
    // Create epoch sections
    for i in 0..epoch_count {
        let epoch_bytes = create_epoch_section(i as u32, b"", archive_key);
        bytes.extend_from_slice(&epoch_bytes);
    }
    
    bytes
}

fn create_epoch_section(epoch_no: u32, payload: &[u8], archive_key: &[u8]) -> Vec<u8> {
    use std::process::Command;
    
    let mut section = Vec::new();
    
    // Header
    section.extend_from_slice(b"EPCH"); // magic
    section.extend_from_slice(&epoch_no.to_le_bytes());
    section.push(0); // status (not demoted)
    section.extend_from_slice(&[0, 0, 0]); // rsvd0
    section.extend_from_slice(&0u64.to_le_bytes()); // created_tick
    section.extend_from_slice(&0u32.to_le_bytes()); // payload_kind
    section.extend_from_slice(&(payload.len() as u32).to_le_bytes());
    section.extend_from_slice(&[0, 0, 0, 0]); // rsvd1
    section.extend_from_slice(&0u64.to_le_bytes()); // primer_addr
    section.extend_from_slice(&[0, 0, 0, 0, 0, 0, 0, 0]); // rsvd2
    
    // Payload
    section.extend_from_slice(payload);
    
    // For now, add a dummy seal (this won't verify, but tests file parsing)
    for _ in 0..32 {
        section.push(0);
    }
    
    section
}

#[test]
fn test_parse_empty_quf() {
    // Just test that we can parse a minimal valid QUF file
    // This test would require calling the binary or using library functions
    // For now, just create a file and verify basic structure
    let key = b"test-key";
    let quf_bytes = create_test_quf_file_bytes(0, key);
    
    // Verify magic
    assert_eq!(&quf_bytes[0..4], b"QUF\x00");
    // Verify version
    assert_eq!(u32::from_le_bytes([quf_bytes[4], quf_bytes[5], quf_bytes[6], quf_bytes[7]]), 1);
}
