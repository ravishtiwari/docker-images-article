

# ===============================
# 1. Build stage
# ===============================
FROM golang:1.22-alpine AS builder

WORKDIR /app
RUN apk add --no-cache gcc musl-dev

COPY go.mod go.sum ./
RUN go mod download

COPY . .
RUN CGO_ENABLED=1 GOOS=linux go build -o todo-app main.go

# ===============================
# 2. Final stage (Distroless)
# ===============================
FROM gcr.io/distroless/base-debian12

WORKDIR /app
COPY --from=builder /app/todos.db ./todos.db
COPY --from=builder /app/todo-app .

EXPOSE 8000
USER nonroot:nonroot
CMD ["./todo-app"]
