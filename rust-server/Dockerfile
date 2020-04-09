FROM rust:1.41.0 as build-env
WORKDIR /app
ADD . /app
RUN cargo build --release

FROM gcr.io/distroless/cc
COPY --from=build-env /app/target/release/rust_http_server /
COPY . /
CMD ["./rust_http_server"]
