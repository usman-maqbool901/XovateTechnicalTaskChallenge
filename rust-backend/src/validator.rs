use csv::ReaderBuilder;
use crate::schemas::{ValidationError, ValidationResponse};
use std::io::Cursor;
use bytes::Bytes;

const REQUIRED_COLUMNS: &[&str] = &["id", "email", "age"];

pub fn validate_csv(content: Bytes) -> ValidationResponse {
    let cursor = Cursor::new(content);
    let mut rdr = ReaderBuilder::new()
        .has_headers(true)
        .from_reader(cursor);

    // 1. Check headers
    let headers = match rdr.headers() {
        Ok(h) => h.clone(),
        Err(e) => return fail(format!("Failed to parse CSV: {}", e)),
    };
    
    let header_names: Vec<&str> = headers.iter().collect();
    let mut missing_cols = Vec::new();
    for req in REQUIRED_COLUMNS {
        if !header_names.contains(req) {
            missing_cols.push(*req);
        }
    }
    
    if !missing_cols.is_empty() {
        return fail(format!("Missing required columns: {}", missing_cols.join(", ")));
    }
    
    let mut records = Vec::new();
    for result in rdr.records() {
        match result {
            Ok(rec) => records.push(rec),
            Err(e) => return fail(format!("Failed to read record: {}", e)),
        }
    }
    
    // 2. Check row count
    // Python code checks: if len(df) <= 10
    if records.len() <= 10 {
        return ValidationResponse {
            status: "fail".to_string(),
            errors: vec![ValidationError {
                row_index: None,
                id: None,
                column: None,
                error_message: "File contains 10 or fewer data rows.".to_string(),
            }],
        };
    }
    
    let mut errors = Vec::new();
    
    let id_idx = headers.iter().position(|h| h == "id").unwrap();
    let email_idx = headers.iter().position(|h| h == "email").unwrap();
    let age_idx = headers.iter().position(|h| h == "age").unwrap();
    
    for (i, record) in records.iter().enumerate() {
        // Python uses 1-based indexing for rows
        let row_index = i + 1;
        let id_val = record.get(id_idx).map(|s| s.to_string());
        
        // 1. Email validation
        let email = record.get(email_idx).unwrap_or("");
        if email.trim().is_empty() {
             errors.push(ValidationError {
                row_index: Some(row_index),
                id: id_val.clone(),
                column: Some("email".to_string()),
                error_message: "Email column must not be empty or null.".to_string(),
            });
        }
        
        // 2. Age validation
        let age_str = record.get(age_idx).unwrap_or("");
        
        // Try to parse as float first (to match Pandas numeric behavior usually handling floats)
        // If it can be parsed, we check range. If not, it's a format error.
        match age_str.parse::<f64>() {
             Ok(age_num) => {
                 // Check range 18-100
                 if age_num < 18.0 || age_num > 100.0 {
                     errors.push(ValidationError {
                        row_index: Some(row_index),
                        id: id_val.clone(),
                        column: Some("age".to_string()),
                        error_message: format!("Age {} is outside the allowed range of 18-100.", age_num as i64),
                    });
                 }
             }
             Err(_) => {
                 // Invalid number format
                 errors.push(ValidationError {
                    row_index: Some(row_index),
                    id: id_val.clone(),
                    column: Some("age".to_string()),
                    error_message: format!("Invalid number format: '{}'", age_str),
                });
             }
        }
    }
    
    let status = if errors.is_empty() { "pass" } else { "fail" };
    ValidationResponse {
        status: status.to_string(),
        errors,
    }
}

fn fail(msg: String) -> ValidationResponse {
    ValidationResponse {
        status: "fail".to_string(),
        errors: vec![ValidationError {
            row_index: None,
            id: None,
            column: None,
            error_message: msg,
        }],
    }
}
