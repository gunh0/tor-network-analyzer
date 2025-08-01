# Tor Anonymous Network Analysis - Makefile
.PHONY: help build run test clean logs stop viewer analyze

help: ## Show available commands
	@echo "Tor Anonymous Network Analysis Commands:"
	@echo "========================================"
	@echo "build       - Build Docker image"
	@echo "analyze     - Run analysis only"
	@echo "viewer      - Start results viewer on :8080"
	@echo "run         - Run analysis + start viewer"
	@echo "test        - Quick test with 2 URLs only"
	@echo "demo        - Run demo without Tor"
	@echo "logs        - Show container logs"
	@echo "stop        - Stop all containers"
	@echo "clean       - Clean up everything"
	@echo "cleanup     - Remove orphan containers"
	@echo "status      - Show system status"

build: ## Build the Docker image
	@echo "🔨 Building Docker image..."
	docker build -t tor-network-analyzer:latest .

analyze: ## Run analysis only
	@echo "🚀 Starting analysis..."
	@echo "Cleaning up any orphan containers..."
	docker compose down --remove-orphans 2>/dev/null || true
	docker compose --profile analyzer up --build

viewer: ## Start results viewer only
	@echo "📊 Starting results viewer..."
	docker compose --profile viewer up -d
	@echo "Results viewer available at http://localhost:8080"

run: ## Run analysis + start viewer
	@echo "🚀 Starting analysis and viewer..."
	docker compose down --remove-orphans 2>/dev/null || true
	docker compose --profile analyzer up --build &
	sleep 5
	docker compose --profile viewer up -d
	@echo "Results viewer available at http://localhost:8080"

test: ## Quick test
	@echo "🧪 Running quick test..."
	@cp src/assets/collect_target_address.txt src/assets/backup.txt
	@echo "https://duckduckgogg42xjoc72x3sjasowoarfbgcmvfimaftt6twagswzczad.onion/" > src/assets/collect_target_address.txt
	docker compose --profile analyzer up --build
	@mv src/assets/backup.txt src/assets/collect_target_address.txt

demo: ## Run demo mode
demo: ## Run demo mode
	@echo "🎭 Running demo..."
	python test_demo.py

logs: ## Show logs (analyzer by default, use 'make logs SERVICE=viewer' for viewer)
	@if [ "$(SERVICE)" = "viewer" ]; then \
		docker compose logs -f results-viewer; \
	else \
		docker compose logs -f tor-analyzer; \
	fi

stop: ## Stop containers
	@echo "🛑 Stopping containers..."
	docker compose --profile analyzer --profile viewer down

clean: ## Clean everything
	@echo "🧹 Cleaning up..."
	docker compose down --volumes
	docker image rm tor-network-analyzer:latest 2>/dev/null || true
	rm -rf results/*

install: ## Install dependencies locally
	pip install -r src/requirements.txt

local: ## Run locally
	@echo "🏠 Running locally (requires Tor)..."
	python main.py

cleanup: ## Remove orphan containers
	@echo "🧹 Removing orphan containers..."
	docker compose down --remove-orphans
	@echo "✅ Cleanup completed!"

status: ## Show status
	@echo "📊 Status:"
	@docker compose ps
	@ls -la results/
