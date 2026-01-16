# Build stage
FROM rust:1.75-slim-bookworm as builder

WORKDIR /usr/src/app
COPY . .

RUN cargo build --release

# Runtime stage
FROM debian:bookworm-slim

WORKDIR /app
COPY --from=builder /usr/src/app/target/release/rust-backend /usr/local/bin/rust-backend

EXPOSE 8000

CMD ["rust-backend"]
