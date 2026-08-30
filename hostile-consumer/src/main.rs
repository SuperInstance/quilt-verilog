// hostile-consumer — independent QUF parser, written from docs/QUF-SPEC.md ONLY.
// No access to tools/quf.py, rtl/, or tb/ was used in writing this file.
// Language choice: Rust (memory-safety + explicit integer widths for a binary format).
use std::env;
use std::fs;
use std::process::exit;

#[derive(Debug)]
pub enum QufError {
    BadMagic,
    BadVersion(u32),
    BadEndian(u32),
    Trunc(&'static str),
    UnknownValueType(u32),
    BadArrayElem(u32),
    NameTooLong(usize),
    SectionOverlap(String),
    NotAscending(String),
    Misaligned(String, u64, u32),
    PastEof(String),
    DuplicateSection(String),
    BadAlign(u32),
    SectionSizeMismatch(String, String),
    BadEdgeK(u32),
    BadTickSize(u64, u64),
    NonZeroPadding,
    SpecGap(String), // behavior the spec does not define; we flag, not guess
}

#[derive(Debug, Clone, PartialEq)]
pub enum Value {
    U8(u8), I8(i8), U16(u16), I16(i16), U32(u32), I32(i32), F32(f32),
    Bool(bool), Str(String), Array(u32, Vec<Value>), U64(u64), I64(i64), F64(f64),
}

#[derive(Debug)]
pub struct Section {
    pub name: String,
    pub kind: u32,
    pub offset: u64,
    pub size: u64,
}

pub struct Quf {
    pub version: u32,
    pub kv: Vec<(String, Value)>,
    pub sections: Vec<Section>,
    pub file_len: u64,
    pub align: u32,
    pub edge_k: Option<u32>,
    pub cell_count: Option<u32>,
    pub edge_count: Option<u32>,
    pub route_count: Option<u32>,
}

struct Rd<'a> { b: &'a [u8], p: usize }
impl<'a> Rd<'a> {
    fn new(b: &'a [u8]) -> Self { Rd { b, p: 0 } }
    fn u8(&mut self) -> Result<u8, QufError> { if self.p >= self.b.len() { return Err(QufError::Trunc("u8")); } let v = self.b[self.p]; self.p += 1; Ok(v) }
    fn u16(&mut self) -> Result<u16, QufError> { Ok(u16::from_le_bytes([self.u8()?, self.u8()?])) }
    fn u32(&mut self) -> Result<u32, QufError> { Ok(u32::from_le_bytes([self.u8()?, self.u8()?, self.u8()?, self.u8()?])) }
    fn u64(&mut self) -> Result<u64, QufError> { let mut a = [0u8; 8]; for x in a.iter_mut() { *x = self.u8()?; } Ok(u64::from_le_bytes(a)) }
    fn bytes(&mut self, n: usize) -> Result<&'a [u8], QufError> { if self.p + n > self.b.len() { return Err(QufError::Trunc("bytes")); } let s = &self.b[self.p..self.p + n]; self.p += n; Ok(s) }
    fn name(&mut self) -> Result<String, QufError> {
        let l = self.u32()? as usize;
        if l > 255 { return Err(QufError::NameTooLong(l)); }
        let s = self.bytes(l)?;
        String::from_utf8(s.to_vec()).map_err(|_| QufError::SpecGap("section/KV name is not valid UTF-8 (spec says 'UTF-8 bytes' but does not define behavior on invalid UTF-8)".into()))
    }
}

fn value_size(t: u32, rd: &mut Rd) -> Result<usize, QufError> {
    // fixed sizes per spec §4 table
    Ok(match t {
        0 | 1 | 7 => 1,
        2 | 3 => 2,
        4 | 5 | 6 => 4,
        10 | 11 | 12 => 8,
        8 => return Err(QufError::SpecGap("string size is variable (caller handles)".into())), // handled specially
        9 => return Err(QufError::SpecGap("array size is variable (caller handles)".into())),
        _ => return Err(QufError::UnknownValueType(t)),
    })
}

fn read_value(rd: &mut Rd, t: u32) -> Result<Value, QufError> {
    match t {
        0 => Ok(Value::U8(rd.u8()?)),
        1 => Ok(Value::I8(rd.u8()? as i8)),
        2 => Ok(Value::U16(rd.u16()?)),
        3 => Ok(Value::I16(rd.u16()? as i16)),
        4 => Ok(Value::U32(rd.u32()?)),
        5 => Ok(Value::I32(rd.u32()? as i32)),
        6 => { let b = rd.bytes(4)?.to_vec(); Ok(Value::F32(f32::from_le_bytes([b[0], b[1], b[2], b[3]]))) }
        7 => Ok(Value::Bool(rd.u8()? != 0)),
        8 => { let l = rd.u32()? as usize; let s = rd.bytes(l)?; Ok(Value::Str(String::from_utf8_lossy(s).into())) }
        9 => {
            let et = rd.u32()?;
            let n = rd.u32()? as usize;
            // spec: element types must be fixed-size, no nested strings/arrays
            let sz = match et {
                0 | 1 | 7 => 1, 2 | 3 => 2, 4 | 5 | 6 => 4, 10 | 11 | 12 => 8,
                8 | 9 => return Err(QufError::BadArrayElem(et)),
                _ => return Err(QufError::UnknownValueType(et)),
            };
            let need = n.checked_mul(sz).ok_or(QufError::SpecGap("array byte length overflows usize (spec has no limit on array count)".into()))?;
            let _ = rd.bytes(need)?;
            Ok(Value::Array(et, Vec::new())) // we skip elements; content not needed for hostile parsing
        }
        10 => Ok(Value::U64(rd.u64()?)),
        11 => Ok(Value::I64(rd.u64()? as i64)),
        12 => { let mut a = [0u8; 8]; for x in a.iter_mut() { *x = rd.u8()?; } Ok(Value::F64(f64::from_le_bytes(a))) }
        _ => Err(QufError::UnknownValueType(t)),
    }
}

const _UNUSED: fn(u32, &mut Rd) -> Result<usize, QufError> = value_size; // silence dead code

pub fn parse(b: &[u8]) -> Result<Quf, QufError> {
    if b.len() < 16 { return Err(QufError::Trunc("fixed header")); }
    if &b[0..4] != b"QUF\0" { return Err(QufError::BadMagic); }
    let mut rd = Rd::new(b);
    let _ = rd.bytes(4)?;
    let version = rd.u32()?;
    if version != 1 { return Err(QufError::BadVersion(version)); }
    let endian = rd.u32()?;
    if endian != 1 { return Err(QufError::BadEndian(endian)); }
    let kv_count = rd.u32()?;

    let mut kv = Vec::new();
    for _ in 0..kv_count {
        let name = rd.name()?;
        let t = rd.u32()?;
        let v = read_value(&mut rd, t)?;
        kv.push((name, v));
    }

    let section_count = rd.u32()?;
    let mut sections = Vec::new();
    for _ in 0..section_count {
        let name = rd.name()?;
        let kind = rd.u32()?;
        let offset = rd.u64()?;
        let size = rd.u64()?;
        if offset > u32::MAX as u64 || size > u32::MAX as u64 {
            return Err(QufError::SpecGap("u64 offset/size with nonzero high word: spec §9 says files must be <4GiB for the RTL loader, but the spec body (§2/§5) imposes no such limit — two consumers with different limits".into()));
        }
        sections.push(Section { name, kind, offset, size });
    }

    let get = |k: &str| kv.iter().find(|(n, _)| n == k).map(|(_, v)| v.clone());
    let align = match get("align") { Some(Value::U32(a)) => a, _ => 32 };
    if align < 8 || (align & (align - 1)) != 0 {
        return Err(QufError::BadAlign(align));
    }

    let file_len = b.len() as u64;
    let mut prev_end = 0u64;
    let mut prev_name = String::new();
    for s in &sections {
        if s.offset % align as u64 != 0 { return Err(QufError::Misaligned(s.name.clone(), s.offset, align)); }
        if s.offset < prev_end { return Err(QufError::NotAscending(format!("{} after {}", s.name, prev_name))); }
        if s.offset + s.size > file_len { return Err(QufError::PastEof(s.name.clone())); }
        if sections.iter().filter(|x| x.name == s.name).count() > 1 {
            return Err(QufError::DuplicateSection(s.name.clone()));
        }
        prev_end = s.offset + s.size;
        prev_name = s.name.clone();
    }
    if file_len % align as u64 != 0 {
        return Err(QufError::SpecGap(format!("file length {} is not a multiple of align {} (§5 says the reference writer pads; whether an unpadded file is invalid is not stated)", file_len, align)));
    }
    // padding must be zero bytes
    let mut pos = rd.p as u64;
    for s in &sections {
        while pos < s.offset {
            if b[pos as usize] != 0 { return Err(QufError::NonZeroPadding); }
            pos += 1;
        }
        pos = s.offset + s.size;
    }
    while pos < file_len {
        if b[pos as usize] != 0 { return Err(QufError::NonZeroPadding); }
        pos += 1;
    }

    // cross-checks between KV counts and section sizes (§4/§6)
    let cell_count = match get("cell_count") { Some(Value::U32(c)) => Some(c), _ => None };
    let edge_count = match get("edge_count") { Some(Value::U32(c)) => Some(c), _ => None };
    let route_count = match get("route_count") { Some(Value::U32(c)) => Some(c), _ => None };
    let edge_k = match get("edge.k") { Some(Value::U32(c)) => Some(c), _ => None };
    if let Some(k) = edge_k { if !(1..=16).contains(&k) { return Err(QufError::BadEdgeK(k)); } }
    let k = edge_k.unwrap_or(8);
    let sec = |n: &str| sections.iter().find(|s| s.name == n);
    if let Some(d) = sec("dials") {
        if let Some(c) = cell_count {
            if d.size != c as u64 * 32 {
                return Err(QufError::SectionSizeMismatch("dials".into(), format!("size {} != cell_count {} * 32", d.size, c)));
            }
        }
    }
    if let Some(e) = sec("edges") {
        if let Some(c) = edge_count {
            if e.size != c as u64 * (12 + k as u64) {
                return Err(QufError::SectionSizeMismatch("edges".into(), format!("size {} != edge_count {} * (12+{})", e.size, c, k)));
            }
        }
    }
    if let Some(r) = sec("routing") {
        if let Some(c) = route_count {
            if r.size != c as u64 * 2 {
                return Err(QufError::SectionSizeMismatch("routing".into(), format!("size {} != route_count {} * 2", r.size, c)));
            }
        }
    }
    if let Some(t) = sec("ticks") {
        if let Some(c) = cell_count {
            if t.size != 4 + 4 * c as u64 {
                return Err(QufError::BadTickSize(t.size, c as u64));
            }
        }
    }

    Ok(Quf { version, kv, sections, file_len, align, edge_k, cell_count, edge_count, route_count })
}

fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() < 2 { eprintln!("usage: qufparse <file.quf> [--dump]"); exit(2); }
    let b = fs::read(&args[1]).unwrap_or_else(|e| { eprintln!("read error: {e}"); exit(2); });
    match parse(&b) {
        Ok(q) => {
            if args.iter().any(|a| a == "--dump") {
                println!("version={} kv={} sections={} align={} len={}", q.version, q.kv.len(), q.sections.len(), q.align, q.file_len);
                for (n, v) in &q.kv { println!("  kv {} = {:?}", n, v); }
                for s in &q.sections { println!("  sec {} kind={} @{} +{}", s.name, s.kind, s.offset, s.size); }
            } else {
                println!("OK");
            }
        }
        Err(e) => { println!("FAIL {:?}", e); exit(1); }
    }
}
