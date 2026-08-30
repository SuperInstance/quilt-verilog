// QUF-FORGETTING-V1 consumer implementation
// Based on QUF-SPEC.md and QUF-FORGETTING-V1.md

use crate::hmac::hmac_sha256;

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum ErrorCode {
    E1, // bad epoch magic
    E2, // truncated
    E3, // seal mismatch / no key
    E4, // malformed epoch name / epoch_no ≠ N / kind ≠ 0 / bad magic (file-level)
    E5, // custody violation
    E6, // multiple live epochs
}

impl ErrorCode {
    pub fn to_string(&self) -> String {
        match self {
            ErrorCode::E1 => "E1".to_string(),
            ErrorCode::E2 => "E2".to_string(),
            ErrorCode::E3 => "E3".to_string(),
            ErrorCode::E4 => "E4".to_string(),
            ErrorCode::E5 => "E5".to_string(),
            ErrorCode::E6 => "E6".to_string(),
        }
    }
}

pub struct Section {
    pub name: String,
    pub offset: u64,
    pub size: u64,
}

pub struct QufFile {
    pub sections: Vec<Section>,
    pub epochs: Vec<(u32, Vec<u8>)>, // (epoch_no, section_bytes)
}

impl QufFile {
    pub fn parse(file_bytes: &[u8]) -> Result<Self, ErrorCode> {
        let mut pos = 0;
        
        // Parse fixed header (16 bytes)
        if file_bytes.len() < 16 {
            return Err(ErrorCode::E2);
        }
        
        // Magic
        if file_bytes[0..4] != [0x51, 0x55, 0x46, 0x00] {
            return Err(ErrorCode::E4);
        }
        
        // Version
        let version = read_u32le(&file_bytes, 4);
        if version != 1 {
            return Err(ErrorCode::E4);
        }
        
        // Endian
        let endian = read_u32le(&file_bytes, 8);
        if endian != 1 {
            return Err(ErrorCode::E4);
        }
        
        // KV count
        let kv_count = read_u32le(&file_bytes, 12);
        pos = 16;
        
        // Skip KV pairs
        for _ in 0..kv_count {
            if pos + 4 > file_bytes.len() {
                return Err(ErrorCode::E2);
            }
            let name_len = read_u32le(&file_bytes, pos) as usize;
            pos += 4;
            
            if pos + name_len > file_bytes.len() {
                return Err(ErrorCode::E2);
            }
            pos += name_len;
            
            if pos + 4 > file_bytes.len() {
                return Err(ErrorCode::E2);
            }
            let value_type = read_u32le(&file_bytes, pos) as usize;
            pos += 4;
            
            // Parse value based on type
            let value_size = match value_type {
                0 | 1 => 1,              // u8, i8
                2 | 3 => 2,              // u16, i16
                4 | 5 | 6 => 4,          // u32, i32, f32
                7 => 1,                  // bool
                8 => {                   // string
                    if pos + 4 > file_bytes.len() {
                        return Err(ErrorCode::E2);
                    }
                    let len = read_u32le(&file_bytes, pos) as usize;
                    pos += 4;
                    if pos + len > file_bytes.len() {
                        return Err(ErrorCode::E2);
                    }
                    pos += len;
                    continue;
                }
                9 => {                   // array
                    if pos + 8 > file_bytes.len() {
                        return Err(ErrorCode::E2);
                    }
                    let elem_type = read_u32le(&file_bytes, pos) as usize;
                    pos += 4;
                    let count = read_u32le(&file_bytes, pos) as usize;
                    pos += 4;
                    
                    let elem_size = match elem_type {
                        0 | 1 => 1,
                        2 | 3 => 2,
                        4 | 5 | 6 => 4,
                        7 => 1,
                        10 | 11 | 12 => 8,
                        _ => return Err(ErrorCode::E4),
                    };
                    
                    if pos + elem_size * count > file_bytes.len() {
                        return Err(ErrorCode::E2);
                    }
                    pos += elem_size * count;
                    continue;
                }
                10 | 11 | 12 => 8,       // u64, i64, f64
                _ => return Err(ErrorCode::E4),
            };
            
            if pos + value_size > file_bytes.len() {
                return Err(ErrorCode::E2);
            }
            pos += value_size;
        }
        
        // Parse section table
        if pos + 4 > file_bytes.len() {
            return Err(ErrorCode::E2);
        }
        let section_count = read_u32le(&file_bytes, pos) as usize;
        pos += 4;
        
        let mut sections = Vec::new();
        let mut epochs = Vec::new();
        
        for _ in 0..section_count {
            if pos + 4 > file_bytes.len() {
                return Err(ErrorCode::E2);
            }
            let name_len = read_u32le(&file_bytes, pos) as usize;
            pos += 4;
            
            if pos + name_len > file_bytes.len() {
                return Err(ErrorCode::E2);
            }
            let name = String::from_utf8_lossy(&file_bytes[pos..pos+name_len]).to_string();
            pos += name_len;
            
            if pos + 4 > file_bytes.len() {
                return Err(ErrorCode::E2);
            }
            let kind = read_u32le(&file_bytes, pos);
            pos += 4;
            
            if pos + 16 > file_bytes.len() {
                return Err(ErrorCode::E2);
            }
            let offset = read_u64le(&file_bytes, pos);
            pos += 8;
            let size = read_u64le(&file_bytes, pos);
            pos += 8;
            
            let offset_usize = offset as usize;
            let size_usize = size as usize;
            
            if offset_usize + size_usize > file_bytes.len() {
                return Err(ErrorCode::E2);
            }
            
            // Handle epoch sections
            if name.starts_with("epoch.") && kind == 0 {
                let epoch_num_str = &name[6..];
                if !epoch_num_str.chars().all(|c| c.is_ascii_digit()) {
                    return Err(ErrorCode::E4);
                }
                match epoch_num_str.parse::<u32>() {
                    Ok(epoch_no) => {
                        let sec_bytes = file_bytes[offset_usize..offset_usize+size_usize].to_vec();
                        epochs.push((epoch_no, sec_bytes));
                    }
                    Err(_) => return Err(ErrorCode::E4),
                }
            }
            
            sections.push(Section {
                name,
                offset,
                size,
            });
        }
        
        Ok(QufFile { sections, epochs })
    }
    
    pub fn skip_mount(&self, archive_key: &[u8]) -> Result<Vec<String>, ErrorCode> {
        self.skip_mount_opt(archive_key, false)
    }

    /// allow_unverified: §4 fail-closed override — E3 epochs are restored
    /// (or skipped, if demoted) but every restored epoch is tagged
    /// "unverified" in the mount list. File-level codes still reject.
    pub fn skip_mount_opt(&self, archive_key: &[u8], allow_unverified: bool)
        -> Result<Vec<String>, ErrorCode> {
        let mut mounted = Vec::new();
        let mut live_epochs = 0;

        for section in &self.sections {
            if section.name.starts_with("epoch.") {
                // Find this epoch in our parsed epochs
                if let Some((epoch_no, sec_bytes)) = self.epochs.iter().find(|(no, _)| {
                    section.name == format!("epoch.{}", no)
                }) {
                    let verifier = EpochVerifier::new(sec_bytes, archive_key);
                    let verified = match verifier.verify(*epoch_no) {
                        Ok(_) => true,
                        Err(ErrorCode::E3) if allow_unverified => false,
                        Err(e) => return Err(e),
                    };
                    
                    // Check if demoted
                    if sec_bytes.len() < 9 {
                        return Err(ErrorCode::E2);
                    }
                    let status = sec_bytes[8];
                    if (status & 0x01) == 0 {
                        // Not demoted - it's live
                        live_epochs += 1;
                        if live_epochs > 1 {
                            return Err(ErrorCode::E6);
                        }
                        mounted.push(if verified {
                            section.name.clone()
                        } else {
                            format!("{} (unverified)", section.name)
                        });
                    }
                }
            } else if section.name == "custody" {
                mounted.push(section.name.clone());
            } else if section.name != "custody" {
                // Keep other sections (dials, edges, routing, ticks)
                mounted.push(section.name.clone());
            }
        }
        
        Ok(mounted)
    }
}

pub struct EpochVerifier<'a> {
    section_bytes: &'a [u8],
    archive_key: &'a [u8],
}

impl<'a> EpochVerifier<'a> {
    pub fn new(section_bytes: &'a [u8], archive_key: &'a [u8]) -> Self {
        EpochVerifier {
            section_bytes,
            archive_key,
        }
    }
    
    pub fn verify(&self, expected_epoch_no: u32) -> Result<(), ErrorCode> {
        let bytes = self.section_bytes;
        
        // Minimum size: 48 (header) + 32 (seal) = 80 bytes
        if bytes.len() < 80 {
            return Err(ErrorCode::E2);
        }
        
        // Check epoch magic "EPCH"
        if bytes[0..4] != [0x45, 0x50, 0x43, 0x48] {
            return Err(ErrorCode::E1);
        }
        
        let epoch_no = read_u32le(&bytes, 4);
        let status = bytes[8];
        let created_tick = read_u64le(&bytes, 12);
        let payload_kind = read_u32le(&bytes, 20);
        let payload_len = read_u32le(&bytes, 24) as usize;
        let primer_addr = read_u64le(&bytes, 32);
        
        // Cross-check epoch_no matches expected
        if epoch_no != expected_epoch_no {
            return Err(ErrorCode::E4);
        }
        
        // payload_kind must be 0
        if payload_kind != 0 {
            return Err(ErrorCode::E4);
        }
        
        // Check size: header(48) + payload + seal(32)
        let expected_size = 48 + payload_len + 32;
        if bytes.len() != expected_size {
            return Err(ErrorCode::E2);
        }
        
        // Extract payload and seal
        let payload = &bytes[48..48 + payload_len];
        let stored_seal = &bytes[48 + payload_len..48 + payload_len + 32];
        
        // Construct HMAC message per §3.3
        let mut msg = Vec::new();
        msg.extend_from_slice(b"QUF-EPOCH-V1\x00");
        msg.extend_from_slice(&epoch_no.to_le_bytes());
        msg.push(status);
        msg.extend_from_slice(&created_tick.to_le_bytes());
        msg.extend_from_slice(&payload_kind.to_le_bytes());
        msg.extend_from_slice(&primer_addr.to_le_bytes());
        msg.extend_from_slice(&(payload_len as u32).to_le_bytes());
        msg.extend_from_slice(payload);
        
        // Compute HMAC
        let computed_tag = hmac_sha256(self.archive_key, &msg);
        
        // Compare tags in constant time
        if constant_time_compare(&computed_tag, stored_seal) {
            Ok(())
        } else {
            Err(ErrorCode::E3)
        }
    }
}

fn read_u32le(bytes: &[u8], offset: usize) -> u32 {
    u32::from_le_bytes([bytes[offset], bytes[offset+1], bytes[offset+2], bytes[offset+3]])
}

fn read_u64le(bytes: &[u8], offset: usize) -> u64 {
    u64::from_le_bytes([
        bytes[offset], bytes[offset+1], bytes[offset+2], bytes[offset+3],
        bytes[offset+4], bytes[offset+5], bytes[offset+6], bytes[offset+7],
    ])
}

fn constant_time_compare(a: &[u8], b: &[u8]) -> bool {
    if a.len() != b.len() {
        return false;
    }
    let mut result = 0u8;
    for (x, y) in a.iter().zip(b.iter()) {
        result |= x ^ y;
    }
    result == 0
}

#[cfg(test)]
mod tests {
    use super::*;
    
    // Test helper: create a minimal epoch section with correct seal
    fn create_test_epoch(epoch_no: u32, payload: &[u8], key: &[u8]) -> Vec<u8> {
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
        
        // Compute seal
        let mut msg = Vec::new();
        msg.extend_from_slice(b"QUF-EPOCH-V1\x00");
        msg.extend_from_slice(&epoch_no.to_le_bytes());
        msg.push(0); // status
        msg.extend_from_slice(&0u64.to_le_bytes()); // created_tick
        msg.extend_from_slice(&0u32.to_le_bytes()); // payload_kind
        msg.extend_from_slice(&0u64.to_le_bytes()); // primer_addr
        msg.extend_from_slice(&(payload.len() as u32).to_le_bytes());
        msg.extend_from_slice(payload);
        
        let tag = hmac_sha256(key, &msg);
        section.extend_from_slice(&tag);
        
        section
    }
    
    #[test]
    fn test_verify_valid_epoch() {
        let key = b"test-key";
        let payload = b"test-payload";
        let section = create_test_epoch(0, payload, key);
        
        let verifier = EpochVerifier::new(&section, key);
        assert!(verifier.verify(0).is_ok());
    }
    
    #[test]
    fn test_verify_wrong_key() {
        let key = b"test-key";
        let payload = b"test-payload";
        let section = create_test_epoch(0, payload, key);
        
        let wrong_key = b"wrong-key";
        let verifier = EpochVerifier::new(&section, wrong_key);
        match verifier.verify(0) {
            Err(ErrorCode::E3) => {}
            _ => panic!("Expected E3 for wrong key"),
        }
    }
    
    #[test]
    fn test_verify_epoch_no_mismatch() {
        let key = b"test-key";
        let payload = b"test-payload";
        let section = create_test_epoch(0, payload, key);
        
        let verifier = EpochVerifier::new(&section, key);
        match verifier.verify(1) {
            Err(ErrorCode::E4) => {}
            _ => panic!("Expected E4 for epoch_no mismatch"),
        }
    }
    
    #[test]
    fn test_verify_truncated() {
        let key = b"test-key";
        let section = vec![0x45, 0x50, 0x43, 0x48]; // Just magic, truncated
        
        let verifier = EpochVerifier::new(&section, key);
        match verifier.verify(0) {
            Err(ErrorCode::E2) => {}
            _ => panic!("Expected E2 for truncated"),
        }
    }
    
    #[test]
    fn test_verify_bad_magic() {
        let key = b"test-key";
        let mut section = vec![0; 80];
        section[0..4].copy_from_slice(b"XXXX"); // bad magic
        
        let verifier = EpochVerifier::new(&section, key);
        match verifier.verify(0) {
            Err(ErrorCode::E1) => {}
            _ => panic!("Expected E1 for bad magic"),
        }
    }
}
