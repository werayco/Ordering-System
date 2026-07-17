.PHONY: build-all build-auth-service build-inventory-service build-notification-service build-order-service build-search-service build-user-service

IMAGE_REPO ?= ordering-system

build-auth-service:
	docker build -t $(IMAGE_REPO)-auth-service:latest ./services/auth-service

build-inventory-service:
	docker build -t $(IMAGE_REPO)-inventory-service:latest ./services/inventory-service

build-notification-service:
	docker build -t $(IMAGE_REPO)-notification-service:latest ./services/notification-service

build-order-service:
	docker build -t $(IMAGE_REPO)-order-service:latest ./services/order-service

build-search-service:
	docker build -t $(IMAGE_REPO)-search-service:latest ./services/search-service

build-user-service:
	docker build -t $(IMAGE_REPO)-user-service:latest ./services/user-service

build-all: build-auth-service build-inventory-service build-notification-service build-order-service build-search-service build-user-service

create-topics:
	python -m shared.kafka.create_topics

git:
	git add .
	git commit -m "$(filter-out $@,$(MAKECMDGOALS))"
	git push
%:
	@: