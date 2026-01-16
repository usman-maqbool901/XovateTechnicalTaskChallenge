use axum::{
    extract::{Multipart, DefaultBodyLimit},
    routing::post,
    Router,
    Json,
};
use tower_http::cors::CorsLayer;
use std::net::SocketAddr;
use crate::validator::validate_csv;

mod validator;
mod schemas;

#[tokio::main]
async fn main() {
    let cors = CorsLayer::new()
        .allow_origin(tower_http::cors::Any)
        .allow_methods(tower_http::cors::Any)
        .allow_headers(tower_http::cors::Any);

    let app = Router::new()
        .route("/validate", post(validate_endpoint))
        .layer(cors)
        .layer(DefaultBodyLimit::max(1000 * 1024 * 1024)); // 10MB limit

    let addr = SocketAddr::from(([0, 0, 0, 0], 8000));
    println!("Server listening on {}", addr);
    let listener = tokio::net::TcpListener::bind(addr).await.unwrap();
    axum::serve(listener, app).await.unwrap();
}

async fn validate_endpoint(mut multipart: Multipart) -> Json<schemas::ValidationResponse> {
    let mut content = bytes::Bytes::new();
    let mut file_found = false;

    while let Some(field) = multipart.next_field().await.unwrap_or(None) {
        // We take the first field or check name "file"
        // Python: file: UploadFile = File(...)
        // if field.name() == Some("file") {
            match field.bytes().await {
                Ok(c) => {
                    content = c;
                    file_found = true;
                    // We only need one file, break after finding it? 
                    // Or keep going? Usually just one.
                }
                Err(e) => {
                     return Json(schemas::ValidationResponse {
                        status: "fail".to_string(),
                        errors: vec![schemas::ValidationError {
                            row_index: None,
                            id: None,
                            column: None,
                            error_message: format!("Failed to read file part: {}", e),
                        }],
                    });
                }
            }
            if file_found { break; }
        // }
    }
    
    if !file_found || content.is_empty() {
         return Json(schemas::ValidationResponse {
            status: "fail".to_string(),
            errors: vec![schemas::ValidationError {
                row_index: None,
                id: None,
                column: None,
                error_message: "No file uploaded or empty file".to_string(),
            }],
        });
    }

    let response = validate_csv(content);
    Json(response)
}
