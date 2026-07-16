# Deliva: Event-Driven Ordering Platform

A mini ordering system built to demonstrate production-grade backend
architecture: event-driven microservices, resilience patterns, and
full observability, deployed on Kubernetes.

## Microservices
- **Auth Service** - registration, login, JWT issuing/validation
- **User Service** - customer profile management
- **Inventory Service** - product catalog and stock, source of truth (Postgres)
- **Order Service** - order lifecycle, orchestrates stock reservation
- **Search Service** - read-optimized product search (Elasticsearch)
- **Notification Service** - consumes events, sends customer notifications

## Architecture Patterns
- **Event-driven communication** - Kafka, domain-partitioned topics
  (`order`, `inventory`, `user`, `notification`)
- **Idempotency keys** - prevents duplicate order creation on client retries
- **Circuit breakers** - protects synchronous calls (Order → Inventory)
  from cascading failure
- **Retry with exponential backoff** - Tenacity, tuned differently for
  sync HTTP calls vs. async Kafka consumers
- **Dead Letter Queue** - captures events that exhaust retries instead
  of silently dropping them

## Observability
- **OpenTelemetry** - distributed tracing across services
- **GlitchTip** - error tracking / exception reporting
- **Langfuse** - LLM observability

## Infrastructure
- **PostgreSQL** - per-service transactional storage
- **Redis** - idempotency key store
- **Elasticsearch** - search index
- **Kubernetes** - deployment, StatefulSets for stateful workloads
- **Docker Compose** - local development
