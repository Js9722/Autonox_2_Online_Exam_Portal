# Quick Start Guide

## 🚀 Get Running in 5 Minutes

### Prerequisites
- Docker and Docker Compose installed
- OpenAI API key (for AI features)

### 1. Clone and Setup
```bash
git clone <repository-url>
cd ai-interview-system
chmod +x setup.sh
./setup.sh
```

### 2. Configure OpenAI API
```bash
# Edit backend/.env
nano backend/.env
# Add: OPENAI_API_KEY=your-key-here
```

### 3. Restart Services
```bash
docker-compose restart backend
```

### 4. Access System
- **Frontend**: http://localhost:3000
- **Admin**: http://localhost:3000/admin
- **API Docs**: http://localhost:8000/docs

### 5. Test Admin Login
- Email: `admin@interview.com`
- Password: `admin123`

## 🎯 Testing the System

### 1. Create Test Candidate
1. Go to http://localhost:3000
2. Click "Register"
3. Fill candidate details
4. Upload a resume (PDF/DOC)

### 2. Start Assessment
1. Login as candidate
2. Click "Start Assessment"
3. Grant camera/microphone permissions
4. Complete questions

### 3. View Results
1. Go to Admin Dashboard
2. Click "Candidates"
3. View assessment results

## 🔧 Troubleshooting

### Common Issues

**Backend not starting**
```bash
# Check logs
docker-compose logs backend

# Restart backend
docker-compose restart backend
```

**Frontend not accessible**
```bash
# Check if port 3000 is free
lsof -i :3000

# Restart frontend
docker-compose restart frontend
```

**Database connection error**
```bash
# Check PostgreSQL
docker-compose exec postgres pg_isready -U postgres

# Recreate database
docker-compose down -v
docker-compose up -d postgres
```

**OpenAI API errors**
1. Verify API key in backend/.env
2. Check OpenAI account credits
3. Restart backend service

### Reset System
```bash
# Complete reset
docker-compose down -v
docker system prune -f
./setup.sh
```

## 📱 Mobile Access

For mobile testing:
1. Find your local IP: `ipconfig getifaddr en0` (Mac) or `hostname -I` (Linux)
2. Access: `http://YOUR_IP:3000`
3. Note: WebRTC may require HTTPS on mobile

## 🔒 Security Notes

- Change default admin password
- Use HTTPS in production
- Secure your OpenAI API key
- Enable firewall rules
- Regular updates recommended

## 📊 System Features

### Candidate Flow
1. **Registration** → Create account
2. **Resume Upload** → AI analysis
3. **Assessment** → 65 questions total
4. **Results** → Instant scoring

### Admin Features
- Real-time monitoring
- Detailed reports
- Export capabilities
- Analytics dashboard

### Assessment Structure
- 30 Technical Questions (AI-generated)
- 30 Aptitude Questions (standardized)
- 5 Speaking Questions (voice recording)
- Proctoring enabled

## 🎯 Next Steps

1. **Customize**: Modify questions and scoring
2. **Integrate**: Connect with HR systems
3. **Scale**: Deploy to cloud
4. **Monitor**: Set up analytics

## 📞 Support

For issues:
1. Check logs: `docker-compose logs`
2. Review documentation: README.md
3. Create GitHub issue

---

**System Ready!** 🎉 You now have a fully functional AI Interview Evaluation System running locally.
