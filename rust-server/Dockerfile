FROM rust:1.41.0 as build-env
WORKDIR /app
ADD . /app
RUN rustup default nightly
RUN rustup override set nightly
RUN rustup update && cargo update
RUN cargo build --release

FROM gcr.io/distroless/cc
COPY --from=build-env /app/target/release/hello-world-distroless /
CMD ["./hello-world-distroless"]
