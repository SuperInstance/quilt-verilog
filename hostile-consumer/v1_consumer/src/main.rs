mod sha256;
mod hmac;
mod quf;

use std::env;
use std::fs;
use std::time::Instant;
use quf::QufFile;

fn main() {
    let args: Vec<String> = env::args().collect();
    
    if args.len() < 2 {
        eprintln!("Usage: v1consumer <command> [args...]");
        std::process::exit(2);
    }
    
    let command = &args[1];
    
    match command.as_str() {
        "verify" => cmd_verify(&args[2..]),
        "skip-mount" => cmd_skip_mount(&args[2..]),
        "bench" => cmd_bench(&args[2..]),
        "info" => cmd_info(&args[2..]),
        _ => {
            eprintln!("Unknown command: {}", command);
            std::process::exit(2);
        }
    }
}

fn cmd_verify(args: &[String]) {
    if args.len() < 2 {
        eprintln!("Usage: verify FILE KEYHEX [--epoch N]");
        std::process::exit(2);
    }
    
    let file_path = &args[0];
    let key_hex = &args[1];
    let mut epoch_filter: Option<u32> = None;
    let mut unverified_load = false;
    
    let mut i = 2;
    while i < args.len() {
        match args[i].as_str() {
            "--epoch" => {
                if i + 1 >= args.len() {
                    eprintln!("--epoch requires an argument");
                    std::process::exit(2);
                }
                epoch_filter = args[i + 1].parse().ok();
                i += 2;
            }
            "--unverified-load" => {
                unverified_load = true;
                i += 1;
            }
            _ => {
                eprintln!("Unknown argument: {}", args[i]);
                std::process::exit(2);
            }
        }
    }
    
    let file_bytes = match fs::read(file_path) {
        Ok(b) => b,
        Err(e) => {
            println!("{{\"result\":\"error\",\"detail\":\"Failed to read file: {}\"}}", e);
            std::process::exit(1);
        }
    };
    
    let key = match parse_hex_key(key_hex) {
        Ok(k) => k,
        Err(_) => {
            println!("{{\"result\":\"error\",\"detail\":\"Invalid key hex\"}}", );
            std::process::exit(1);
        }
    };
    
    let quf = match QufFile::parse(&file_bytes) {
        Ok(q) => q,
        Err(code) => {
            println!("{{\"result\":\"reject\",\"code\":\"{}\"}}", code.to_string());
            std::process::exit(1);
        }
    };
    
    let mut found_any = false;
    for (epoch_no, sec_bytes) in &quf.epochs {
        if let Some(filter) = epoch_filter {
            if *epoch_no != filter {
                continue;
            }
        }
        found_any = true;
        
        let verifier = quf::EpochVerifier::new(sec_bytes, &key);
        match verifier.verify(*epoch_no) {
            Ok(_) => {
                println!("{{\"result\":\"ok\",\"epoch\":{}}}", epoch_no);
            }
            Err(code) => {
                if unverified_load {
                    println!("{{\"result\":\"ok\",\"epoch\":{},\"unverified\":true}}", epoch_no);
                } else {
                    println!("{{\"result\":\"reject\",\"code\":\"{}\",\"epoch\":{}}}", code.to_string(), epoch_no);
                    std::process::exit(1);
                }
            }
        }
    }
    
    if !found_any && epoch_filter.is_some() {
        println!("{{\"result\":\"error\",\"detail\":\"Epoch not found\"}}", );
        std::process::exit(1);
    }
}

fn cmd_skip_mount(args: &[String]) {
    if args.len() < 2 {
        eprintln!("Usage: skip-mount FILE KEYHEX [--unverified-load]");
        std::process::exit(2);
    }
    let allow_unverified = args.iter().skip(2)
        .any(|a| a == "--unverified-load");
    let args: Vec<String> = args.iter().filter(|a| **a != "--unverified-load")
        .cloned().collect();
    let file_path = &args[0];
    let key_hex = &args[1];
    
    let file_bytes = match fs::read(file_path) {
        Ok(b) => b,
        Err(e) => {
            println!("{{\"result\":\"error\",\"detail\":\"Failed to read file: {}\"}}", e);
            std::process::exit(1);
        }
    };
    
    let key = match parse_hex_key(key_hex) {
        Ok(k) => k,
        Err(_) => {
            println!("{{\"result\":\"error\",\"detail\":\"Invalid key hex\"}}", );
            std::process::exit(1);
        }
    };
    
    let quf = match QufFile::parse(&file_bytes) {
        Ok(q) => q,
        Err(code) => {
            println!("{{\"result\":\"reject\",\"code\":\"{}\"}}", code.to_string());
            std::process::exit(1);
        }
    };
    
    match quf.skip_mount_opt(&key, allow_unverified) {
        Ok(sections) => {
            println!("{{\"result\":\"ok\",\"mounted_sections\":[");
            for (i, section) in sections.iter().enumerate() {
                if i > 0 {
                    println!(",");
                }
                print!("  {{\"name\":\"{}\"}}", section);
            }
            println!("\n]}}", );
        }
        Err(code) => {
            println!("{{\"result\":\"reject\",\"code\":\"{}\"}}", code.to_string());
            std::process::exit(1);
        }
    }
}

fn cmd_bench(args: &[String]) {
    if args.len() < 3 {
        eprintln!("Usage: bench FILE KEYHEX ITERS");
        std::process::exit(2);
    }
    
    let file_path = &args[0];
    let key_hex = &args[1];
    let iters: usize = match args[2].parse() {
        Ok(i) => i,
        Err(_) => {
            eprintln!("Invalid iteration count");
            std::process::exit(2);
        }
    };
    
    let file_bytes = match fs::read(file_path) {
        Ok(b) => b,
        Err(e) => {
            println!("{{\"result\":\"error\",\"detail\":\"Failed to read file: {}\"}}", e);
            std::process::exit(1);
        }
    };
    
    let key = match parse_hex_key(key_hex) {
        Ok(k) => k,
        Err(_) => {
            println!("{{\"result\":\"error\",\"detail\":\"Invalid key hex\"}}", );
            std::process::exit(1);
        }
    };
    
    let quf = match QufFile::parse(&file_bytes) {
        Ok(q) => q,
        Err(code) => {
            println!("{{\"result\":\"reject\",\"code\":\"{}\"}}", code.to_string());
            std::process::exit(1);
        }
    };
    
    // Bench per-epoch verification
    let mut epoch_times = Vec::new();
    for (epoch_no, sec_bytes) in &quf.epochs {
        let start = Instant::now();
        for _ in 0..iters {
            let verifier = quf::EpochVerifier::new(sec_bytes, &key);
            let _ = verifier.verify(*epoch_no);
        }
        let elapsed = start.elapsed();
        let micros = elapsed.as_micros() as f64 / iters as f64;
        epoch_times.push((*epoch_no, micros));
    }
    
    // Bench full skip-mount
    let start = Instant::now();
    for _ in 0..iters {
        let _ = quf.skip_mount(&key);
    }
    let elapsed = start.elapsed();
    let mount_ms = elapsed.as_secs_f64() * 1000.0 / iters as f64;
    
    println!("{{\"result\":\"ok\",\"per_epoch_verify_us\":[");
    for (i, (epoch_no, micros)) in epoch_times.iter().enumerate() {
        if i > 0 {
            println!(",");
        }
        print!("  {{\"epoch\":{},\"micros\":{:.2}}}", epoch_no, micros);
    }
    println!("\n],\"skip_mount_avg_ms\":{:.4}}}", mount_ms);
}

fn cmd_info(args: &[String]) {
    if args.is_empty() {
        eprintln!("Usage: info FILE");
        std::process::exit(2);
    }
    
    let file_path = &args[0];
    let file_bytes = match fs::read(file_path) {
        Ok(b) => b,
        Err(e) => {
            println!("{{\"result\":\"error\",\"detail\":\"Failed to read file: {}\"}}", e);
            std::process::exit(1);
        }
    };
    
    let quf = match QufFile::parse(&file_bytes) {
        Ok(q) => q,
        Err(code) => {
            println!("{{\"result\":\"reject\",\"code\":\"{}\"}}", code.to_string());
            std::process::exit(1);
        }
    };
    
    println!("{{\"result\":\"ok\",\"sections\":[");
    for (i, section) in quf.sections.iter().enumerate() {
        if i > 0 {
            println!(",");
        }
        print!("  {{\"name\":\"{}\",\"offset\":{},\"size\":{}}}", section.name, section.offset, section.size);
    }
    println!("\n]}}", );
}

fn parse_hex_key(hex_str: &str) -> Result<Vec<u8>, String> {
    if hex_str.len() % 2 != 0 {
        return Err("Hex string must have even length".to_string());
    }
    
    let mut result = Vec::new();
    for i in (0..hex_str.len()).step_by(2) {
        let hex_byte = &hex_str[i..i+2];
        match u8::from_str_radix(hex_byte, 16) {
            Ok(b) => result.push(b),
            Err(_) => return Err(format!("Invalid hex byte: {}", hex_byte)),
        }
    }
    Ok(result)
}
