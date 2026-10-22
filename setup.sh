#!/bin/bash

# AI Interview Evaluation System Setup Script
# This script helps you set up the entire system for development

set -e

echo "🚀 AI Interview Evaluation System Setup"
echo "======================================"

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

echo "✅ Docker and Docker Compose are installed"

# Create .env files if they don't exist
if [ ! -f "backend/.env" ]; then
    echo "📝 Creating backend .env file..."
    cp backend/.env.example backend/.env
    echo "⚠️  Please edit backend/.env and add your OpenAI API key"
fi

if [ ! -f "frontend/.env" ]; then
    echo "📝 Creating frontend .env file..."
    cat > frontend/.env << EOF
REACT_APP_API_URL=http://localhost:8000/api
REACT_APP_UPLOAD_URL=http://localhost:8000/uploads
EOF
fi

# Create necessary directories
echo "📁 Creating necessary directories..."
mkdir -p backend/uploads/resumes
mkdir -p backend/uploads/audio
mkdir -p backend/uploads/proctoring

# Set proper permissions
chmod 755 backend/uploads
chmod 755 backend/uploads/resumes
chmod 755 backend/uploads/audio
chmod 755 backend/uploads/proctoring

echo "✅ Directories created and permissions set"

# Build and start services
echo "🐳 Building and starting Docker containers..."
docker-compose up --build -d

# Wait for services to be ready
echo "⏳ Waiting for services to start..."
sleep 30

# Check if services are running
echo "🔍 Checking service status..."

# Check PostgreSQL
if docker-compose exec -T postgres pg_isready -U postgres > /dev/null 2>&1; then
    echo "✅ PostgreSQL is ready"
else
    echo "❌ PostgreSQL is not ready"
fi

# Check Backend
if curl -f http://localhost:8000/health > /dev/null 2>&1; then
    echo "✅ Backend API is ready"
else
    echo "❌ Backend API is not ready"
fi

# Check Frontend
if curl -f http://localhost:3000 > /dev/null 2>&1; then
    echo "✅ Frontend is ready"
else
    echo "❌ Frontend is not ready"
fi

# Run database migrations
echo "🗄️ Running database migrations..."
docker-compose exec backend alembic upgrade head

# Create admin user
echo "👤 Creating admin user..."
docker-compose exec backend python -c "
from app.database import SessionLocal, engine
from app.models import Candidate, Base
from app.auth import get_password_hash

Base.metadata.create_all(bind=engine)
db = SessionLocal()

# Check if admin user exists
admin = db.query(Candidate).filter(Candidate.email == 'admin@interview.com').first()
if not admin:
    admin = Candidate(
        name='Admin User',
        email='admin@interview.com',
        password_hash=get_password_hash('admin123'),
        experience_level='senior'
    )
    db.add(admin)
    db.commit()
    print('✅ Admin user created: admin@interview.com / admin123')
else:
    print('ℹ️ Admin user already exists')

db.close()
"

# Populate question bank
echo "📚 Populating question bank..."
docker-compose exec backend python -c "
import requests
import time

# Wait a bit for the API to be fully ready
time.sleep(5)

try:
    response = requests.post('http://localhost:8000/api/admin/questions/populate')
    if response.status_code == 200:
        print('✅ Question bank populated successfully')
    else:
        print('⚠️ Question bank population may have failed')
except Exception as e:
    print(f'❌ Error populating question bank: {e}')
"

echo ""
echo "🎉 Setup Complete!"
echo "=================="
echo ""
echo "🌐 Access Points:"
echo "   Frontend:        http://localhost:3000"
echo "   Backend API:     http://localhost:8000"
echo "   API Docs:        http://localhost:8000/docs"
echo "   Admin Dashboard:  http://localhost:3000/admin"
echo ""
echo "👤 Default Admin Login:"
echo "   Email:    admin@interview.com"
echo "   Password: admin123"
echo ""
echo "📝 Next Steps:"
echo "   1. Edit backend/.env and add your OpenAI API key"
echo "   2. Restart the backend: docker-compose restart backend"
echo "   3. Visit the frontend and start using the system"
echo ""
echo "🔧 Useful Commands:"
echo "   View logs:       docker-compose logs -f"
echo "   Stop services:   docker-compose down"
echo "   Restart backend: docker-compose restart backend"
echo "   Access backend:  docker-compose exec backend bash"
echo ""
echo "📚 Documentation:"
echo "   Read README.md for detailed information"
echo ""
