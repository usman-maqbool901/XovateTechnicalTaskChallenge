export interface ValidationError {
  row_index: number | null;
  id: number | null;
  column: string | null;
  error_message: string;
}

export interface ValidationResponse {
  status: "pass" | "fail";
  errors: ValidationError[];
}
