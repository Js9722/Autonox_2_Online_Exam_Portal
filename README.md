# AI Interview Evaluation System

A comprehensive full-stack web application for automated, structured, and intelligent candidate assessment powered by AI.

## Technology Stack

- **Backend**: Python (FastAPI)
- **Frontend**: React.js with TypeScript
- **Database**: PostgreSQL
- **Authentication**: JWT
- **AI Integration**: OpenAI API for resume analysis and question generation
- **Proctoring**: Webcam monitoring and violation detection
- **Containerization**: Docker & Docker Compose

## Features

### 1. Candidate Registration & Login
- Complete registration form with skills selection
- JWT-based authentication
- Profile management with resume upload
- Experience level and applied role tracking

### 2. Resume Analysis (AI-based)
- PDF/DOC file upload support
- AI-powered skill extraction
- Strength and weakness identification
- Dynamic question generation based on skills

### 3. Assessment Structure
- **30 Technical MCQs**: AI-generated based on resume skills
- **30 Aptitude MCQs**: Predefined question bank
- **5 Speaking Questions**: Audio recording and evaluation
- **Weighted scoring**: Easy (1.0x), Medium (1.5x), Hard (2.0x)

### 4. Proctoring System
- Webcam monitoring with periodic snapshots
- Tab switching detection
- Violation logging and auto-submission
- Real-time warning system

### 5. Scoring & Evaluation
- Technical score (50% weight)
- Aptitude score (30% weight)
- Speaking score (20% weight)
- AI-generated summary and recommendations
- Performance levels: Strong Hire (85+), Hire (70-84), Borderline (50-69), Reject (<50)

### 6. Admin Dashboard
- Complete candidate management
- Detailed assessment reports
- Audio playback for speaking responses
- Proctoring violation logs
- PDF/CSV report downloads

## Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- PostgreSQL 12+
- Docker & Docker Compose (optional)

### Option 1: Docker Deployment (Recommended)

1. Clone the repository:
```bash
git clone <repository-url>
cd ai-interview-system
```

2. Create environment file:
```bash
cp backend/.env.example backend/.env
# Edit backend/.env with your configuration
```

3. Start all services:
```bash
docker-compose up -d
```

4. Access the application:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/api/docs

### Option 2: Local Development

#### Backend Setup

1. Navigate to backend directory:
```bash
cd backend
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Setup database:
```bash
python setup.py
```

5. Start backend server:
```bash
python -m uvicorn app.main:app --reload
```

#### Frontend Setup

1. Navigate to frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start development server:
```bash
npm start
```

## Configuration

### Environment Variables

Create a `.env` file in the backend directory:

```env
# Database
DATABASE_URL=postgresql://postgres:password@localhost:5432/ai_interview_db

# JWT
JWT_SECRET_KEY=your-super-secret-jwt-key-change-this-in-production-256-bit
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30

# AI APIs
OPENAI_API_KEY=your_openai_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here

# File Upload
UPLOAD_DIR=./uploads
MAX_FILE_SIZE=10485760

# CORS
CORS_ORIGINS=["http://localhost:3000","http://127.0.0.1:3000"]

# Assessment Settings
ASSESSMENT_DURATION_MINUTES=30
TECHNICAL_QUESTIONS_COUNT=30
APTITUDE_QUESTIONS_COUNT=30
SPEAKING_QUESTIONS_COUNT=5
```

## Default Credentials

- **Admin Login**: admin@example.com / admin123
- **Demo Candidate**: demo@example.com / Password123@

## API Endpoints

### Authentication
- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login` - User login
- `GET /api/v1/auth/me` - Get current user

### Resume
- `POST /api/v1/resume/upload` - Upload resume
- `GET /api/v1/resume/my-resume` - Get user's resume

### Assessment
- `POST /api/v1/assessment/start` - Start assessment
- `GET /api/v1/assessment/{id}/questions` - Get assessment questions
- `POST /api/v1/assessment/{id}/submit` - Submit response
- `POST /api/v1/assessment/{id}/complete` - Complete assessment
- `GET /api/v1/assessment/{id}/results` - Get results

### Admin
- `GET /api/v1/admin/candidates` - Get all candidates
- `GET /api/v1/admin/assessments` - Get all assessments
- `GET /api/v1/admin/dashboard/stats` - Get dashboard statistics

## Database Schema

### Tables
- `users` - User authentication and roles
- `candidates` - Candidate profiles and information
- `resumes` - Resume files and analysis results
- `questions` - Assessment questions (technical, aptitude, speaking)
- `assessments` - Assessment sessions and scores
- `responses` - Question responses
- `proctoring_logs` - Proctoring violations
- `speaking_responses` - Audio responses and evaluations

## Project Structure

```
ai-interview-system/
|-- backend/
|   |-- app/
|   |   |-- api/v1/          # API endpoints
|   |   |-- core/            # Core configuration
|   |   |-- models/          # Database models
|   |   |-- schemas/         # Pydantic schemas
|   |   |-- services/        # Business logic
|   |-- alembic/             # Database migrations
|   |-- uploads/             # File uploads
|   |-- requirements.txt
|   |-- Dockerfile
|   |-- setup.py
|-- frontend/
|   |-- src/
|   |   |-- components/      # React components
|   |   |-- pages/           # Page components
|   |   |-- contexts/        # React contexts
|   |   |-- services/        # API services
|   |-- public/
|   |-- package.json
|   |-- Dockerfile
|-- docker-compose.yml
|-- README.md
```

## Development

### Running Tests
```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm test
```

### Code Formatting
```bash
# Backend
cd backend
black app/
isort app/

# Frontend
cd frontend
npm run lint
```

### Database Migrations
```bash
cd backend
alembic revision --autogenerate -m "migration description"
alembic upgrade head
```

## Deployment

### Production Deployment

1. Configure environment variables
2. Build Docker images:
```bash
docker-compose build
```

3. Deploy to production:
```bash
docker-compose -f docker-compose.prod.yml up -d
```

### Environment-Specific Configurations

- **Development**: Local database, debug mode
- **Staging**: Production database, staging APIs
- **Production**: Optimized build, SSL, monitoring

## Security Features

- JWT-based authentication
- Password hashing with bcrypt
- CORS protection
- File upload validation
- SQL injection prevention
- XSS protection

## Performance

- Fast API response (<2 seconds)
- Efficient database queries
- Image compression for screenshots
- Audio compression for speaking responses
- Caching with Redis

## Monitoring

- Application logs
- Database performance metrics
- API response time tracking
- Error reporting

## Contributing

1. Fork the repository
2. Create feature branch
3. Make changes
4. Add tests
5. Submit pull request

## License

This project is licensed under the MIT License.

## Support

For support and questions, please create an issue in the repository or contact the development team.

---

**Built with**: FastAPI, React, PostgreSQL, OpenAI, Docker
**Version**: 2.0.0
**Last Updated**: 2024
