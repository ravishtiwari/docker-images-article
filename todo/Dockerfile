# ===============================
# 1. Build stage
# ===============================
FROM golang:1.22-alpine AS builder

WORKDIR /app
RUN apk add --no-cache gcc musl-dev

COPY go.mod go.sum ./
RUN go mod download

COPY . .
# Build fully static binary
RUN CGO_ENABLED=1 GOOS=linux go build \
    -ldflags '-linkmode external -extldflags "-static"' \
    -o /app/todo-app main.go

# ===============================
# 2. Final stage (Distroless Static)
# ===============================
FROM gcr.io/distroless/static-debian12

WORKDIR /app
COPY --from=builder /app/todo-app /app/todo-app
COPY --from=builder /app/todos.db /app/todos.db

EXPOSE 8000
USER nonroot:nonroot
CMD ["/app/todo-app"]
