import pandas as pd
import io
import re
from typing import List
from .schemas import ValidationError, ValidationResponse

REQUIRED_COLUMNS = ["id", "email", "age"]

def validate_csv(file_content: bytes) -> ValidationResponse:
    try:
        df = pd.read_csv(io.BytesIO(file_content))
    except Exception as e:
        return ValidationResponse(
            status="fail",
            errors=[ValidationError(error_message=f"Failed to parse CSV: {str(e)}")]
        )

    errors: List[ValidationError] = []

    # Check for missing columns
    missing_cols = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing_cols:
        return ValidationResponse(
            status="fail",
            errors=[ValidationError(error_message=f"Missing required columns: {', '.join(missing_cols)}")]
        )

    # Check for minimum row count
    if len(df) <= 10:
        return ValidationResponse(
            status="fail",
            errors=[ValidationError(row_index=None, id=None, column=None, error_message="File contains 10 or fewer data rows.")]
        )

    # --- Vectorized Validation ---
    
    # 1. Email validation (empty or null)
    email_invalid_mask = df['email'].isna() | (df['email'].astype(str).str.strip() == "")
    email_errors_df = df[email_invalid_mask]
    for idx, row in email_errors_df.iterrows():
        errors.append(ValidationError(
            row_index=int(idx) + 1,
            id=row.get("id"),
            column="email",
            error_message="Email column must not be empty or null."
        ))

    # 2. Age validation
    # Convert 'age' to numeric, invalid entries become NaN
    numeric_age = pd.to_numeric(df['age'], errors='coerce')
    
    # 2a. Identify rows with invalid number format (wasn't NaN but became NaN)
    format_errors_mask = numeric_age.isna()
    format_errors_df = df[format_errors_mask]
    for idx, row in format_errors_df.iterrows():
        errors.append(ValidationError(
            row_index=int(idx) + 1,
            id=row.get("id"),
            column="age",
            error_message=f"Invalid number format: '{row.get('age')}'"
        ))
        
    # 2b. Range errors (only for valid numeric entries)
    range_errors_mask = ~numeric_age.isna() & ((numeric_age < 18) | (numeric_age > 100))
    range_errors_df = df[range_errors_mask]
    for idx, row in range_errors_df.iterrows():
        # Using .loc to get the numeric age for the current index
        age_val = int(numeric_age.loc[idx])
        errors.append(ValidationError(
            row_index=int(idx) + 1,
            id=row.get("id"),
            column="age",
            error_message=f"Age {age_val} is outside the allowed range of 18-100."
        ))

    status = "pass" if not errors else "fail"
    return ValidationResponse(status=status, errors=errors)
