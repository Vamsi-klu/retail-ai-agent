#!/bin/bash

# Retail AI Pro - Complete Startup Script
# This script sets up and runs the entire application stack

set -e

echo "🚀 Starting Retail AI Pro - Enterprise Edition"
echo "=============================================="

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check prerequisites
echo -e "${BLUE}📋 Checking prerequisites...${NC}"

MISSING_DEPS=0

if ! command_exists docker; then
    echo -e "${RED}❌ Docker not found. Please install Docker.${NC}"
    MISSING_DEPS=1
fi

if ! command_exists docker-compose; then
    echo -e "${RED}❌ Docker Compose not found. Please install Docker Compose.${NC}"
    MISSING_DEPS=1
fi

if [ $MISSING_DEPS -eq 1 ]; then
    echo -e "${RED}Please install missing dependencies before running.${NC}"
    exit 1
fi

echo -e "${GREEN}✅ All prerequisites found${NC}\n"

# Stop any running containers
echo -e "${BLUE}🛑 Stopping any existing containers...${NC}"
docker-compose down 2>/dev/null || true

# Clean up old data (optional - comment out to preserve data)
# echo -e "${BLUE}🧹 Cleaning up old data...${NC}"
# docker volume rm retail-ai-pro_postgres_data 2>/dev/null || true

# Build images
echo -e "${BLUE}🔨 Building Docker images...${NC}"
docker-compose build --no-cache

# Start services
echo -e "${BLUE}🚀 Starting services...${NC}"
docker-compose up -d

# Wait for services to be healthy
echo -e "${BLUE}⏳ Waiting for services to be healthy...${NC}"

# Function to check service health
check_service() {
    local service=$1
    local max_attempts=30
    local attempt=0
    
    while [ $attempt -lt $max_attempts ]; do
        if docker-compose ps | grep $service | grep -q "healthy\|Up"; then
            echo -e "${GREEN}✅ $service is ready${NC}"
            return 0
        fi
        echo -n "."
        sleep 2
        ((attempt++))
    done
    
    echo -e "${RED}❌ $service failed to start${NC}"
    return 1
}

# Check each service
check_service "postgres" || exit 1
check_service "redis" || exit 1
check_service "backend" || exit 1
check_service "frontend" || exit 1

echo -e "\n${GREEN}✅ All services are running!${NC}\n"

# Initialize demo data
echo -e "${BLUE}📊 Initializing demo data...${NC}"
docker-compose exec -T backend python -m app.scripts.init_demo_data

# Run database migrations
echo -e "${BLUE}🗄️ Running database migrations...${NC}"
docker-compose exec -T backend alembic upgrade head

# Display access information
echo -e "\n${GREEN}🎉 Retail AI Pro is ready!${NC}"
echo -e "${GREEN}================================${NC}"
echo -e "${BLUE}🌐 Web Application:${NC} http://localhost:3000"
echo -e "${BLUE}📡 API Documentation:${NC} http://localhost:8000/docs"
echo -e "${BLUE}🗄️ Database:${NC} postgresql://localhost:5432/retailai"
echo -e "${BLUE}📊 Redis:${NC} redis://localhost:6379"
echo -e "${GREEN}================================${NC}\n"

# Show logs
echo -e "${YELLOW}📜 Showing application logs (Ctrl+C to stop)...${NC}\n"
docker-compose logs -f --tail=100

# Cleanup function
cleanup() {
    echo -e "\n${BLUE}🛑 Stopping services...${NC}"
    docker-compose down
    echo -e "${GREEN}✅ Services stopped successfully${NC}"
    exit 0
}

# Register cleanup function
trap cleanup SIGINT SIGTERM

# Keep script running
wait