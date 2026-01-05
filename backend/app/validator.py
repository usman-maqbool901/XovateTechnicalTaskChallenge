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

    missing_cols = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing_cols:
        return ValidationResponse(
            status="fail",
            errors=[ValidationError(error_message=f"Missing required columns: {', '.join(missing_cols)}")]
        )

    if len(df) <= 10:
        return ValidationResponse(
            status="fail",
            errors=[ValidationError(row_index=None, id=None, column=None, error_message="File contains 10 or fewer data rows.")]
        )

    for idx, row in df.iterrows():
        row_index = int(idx) + 1
        row_id = row.get("id")
        
        email_val = row.get("email")
        if pd.isna(email_val) or str(email_val).strip() == "":
            errors.append(ValidationError(
                row_index=row_index,
                id=row_id,
                column="email",
                error_message="Email column must not be empty or null."
            ))

        age_val = row.get("age")
        
        is_valid_format = False
        parsed_age = None
        
        if not pd.isna(age_val):
            age_str = str(age_val).strip()
            if re.fullmatch(r"\d+", age_str):
                parsed_age = int(age_str)
                is_valid_format = True
            else:
                is_valid_format = False
        else:
            is_valid_format = False

        if not is_valid_format:
            errors.append(ValidationError(
                row_index=row_index,
                id=row_id,
                column="age",
                error_message=f"Invalid number format: '{age_val}'"
            ))
        else:
            if not (18 <= parsed_age <= 100):
                errors.append(ValidationError(
                    row_index=row_index,
                    id=row_id,
                    column="age",
                    error_message=f"Age {parsed_age} is outside the allowed range of 18-100."
                ))

    status = "pass" if not errors else "fail"
    return ValidationResponse(status=status, errors=errors)
