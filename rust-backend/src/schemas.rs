use serde::{Deserialize, Serialize};

#[derive(Debug, Serialize, Deserialize, Clone)]
pub struct ValidationError {
    #[serde(skip_serializing_if = "Option::is_none")]
    pub row_index: Option<usize>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub id: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub column: Option<String>,
    pub error_message: String,
}

#[derive(Debug, Serialize, Deserialize)]
pub struct ValidationResponse {
    pub status: String,
    pub errors: Vec<ValidationError>,
}
