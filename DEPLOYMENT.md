# Deployment Guide

## Production Deployment

### Prerequisites
- Docker & Docker Compose
- PostgreSQL server
- Redis server
- SSL certificates (for HTTPS)
- Domain name (optional)

### Step 1: Environment Configuration

1. Create production environment file:
```bash
cp backend/.env.example backend/.env.production
```

2. Edit `.env.production` with production values:
```env
# Database
DATABASE_URL=postgresql://username:password@your-db-host:5432/ai_interview_db

# Security
JWT_SECRET_KEY=your-very-secure-256-bit-secret-key-here
CORS_ORIGINS=["https://yourdomain.com"]

# AI APIs
OPENAI_API_KEY=your-production-openai-key
ANTHROPIC_API_KEY=your-production-anthropic-key

# File Storage
UPLOAD_DIR=/app/uploads
MAX_FILE_SIZE=10485760
```

### Step 2: Docker Production Setup

1. Create production docker-compose file:
```bash
cp docker-compose.yml docker-compose.prod.yml
```

2. Modify `docker-compose.prod.yml` for production:
```yaml
version: '3.8'

services:
  postgres:
    image: postgres:15
    environment:
      POSTGRES_DB: ai_interview_db
      POSTGRES_USER: ${POSTGRES_USER}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    networks:
      - ai_interview_network
    restart: always

  redis:
    image: redis:7-alpine
    networks:
      - ai_interview_network
    restart: always

  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    environment:
      - DATABASE_URL=${DATABASE_URL}
      - REDIS_URL=${REDIS_URL}
      - JWT_SECRET_KEY=${JWT_SECRET_KEY}
      - OPENAI_API_KEY=${OPENAI_API_KEY}
    volumes:
      - ./uploads:/app/uploads
    depends_on:
      - postgres
      - redis
    networks:
      - ai_interview_network
    restart: always

  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    depends_on:
      - backend
    networks:
      - ai_interview_network
    restart: always

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/nginx.prod.conf:/etc/nginx/nginx.conf
      - ./nginx/ssl:/etc/nginx/ssl
      - ./uploads:/var/www/uploads
    depends_on:
      - frontend
      - backend
    networks:
      - ai_interview_network
    restart: always

volumes:
  postgres_data:

networks:
  ai_interview_network:
    driver: bridge
```

### Step 3: Nginx Configuration

Create `nginx/nginx.prod.conf`:
```nginx
events {
    worker_connections 1024;
}

http {
    include /etc/nginx/mime.types;
    default_type application/octet-stream;

    # Logging
    access_log /var/log/nginx/access.log;
    error_log /var/log/nginx/error.log;

    # Gzip compression
    gzip on;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_types text/plain text/css application/json application/javascript text/xml application/xml application/xml+rss text/javascript;

    # Rate limiting
    limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;

    upstream backend {
        server backend:8000;
    }

    # HTTP to HTTPS redirect
    server {
        listen 80;
        server_name yourdomain.com www.yourdomain.com;
        return 301 https://$server_name$request_uri;
    }

    # HTTPS server
    server {
        listen 443 ssl http2;
        server_name yourdomain.com www.yourdomain.com;

        # SSL configuration
        ssl_certificate /etc/nginx/ssl/cert.pem;
        ssl_certificate_key /etc/nginx/ssl/key.pem;
        ssl_protocols TLSv1.2 TLSv1.3;
        ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512:ECDHE-RSA-AES256-GCM-SHA384:DHE-RSA-AES256-GCM-SHA384;
        ssl_prefer_server_ciphers off;

        # Security headers
        add_header X-Frame-Options DENY;
        add_header X-Content-Type-Options nosniff;
        add_header X-XSS-Protection "1; mode=block";
        add_header Strict-Transport-Security "max-age=63072000; includeSubDomains; preload";

        # Frontend
        location / {
            root /usr/share/nginx/html;
            index index.html index.htm;
            try_files $uri $uri/ /index.html;
        }

        # API proxy
        location /api/ {
            limit_req zone=api burst=20 nodelay;
            proxy_pass http://backend;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
            
            # CORS headers
            add_header Access-Control-Allow-Origin $http_origin always;
            add_header Access-Control-Allow-Methods "GET, POST, PUT, DELETE, OPTIONS" always;
            add_header Access-Control-Allow-Headers "DNT,User-Agent,X-Requested-With,If-Modified-Since,Cache-Control,Content-Type,Range,Authorization" always;
            
            if ($request_method = 'OPTIONS') {
                add_header Access-Control-Allow-Origin $http_origin;
                add_header Access-Control-Allow-Methods "GET, POST, PUT, DELETE, OPTIONS";
                add_header Access-Control-Allow-Headers "DNT,User-Agent,X-Requested-With,If-Modified-Since,Cache-Control,Content-Type,Range,Authorization";
                add_header Access-Control-Max-Age 1728000;
                add_header Content-Type "text/plain; charset=utf-8";
                add_header Content-Length 0;
                return 204;
            }
        }

        # File uploads
        location /uploads/ {
            alias /var/www/uploads/;
            expires 1y;
            add_header Cache-Control "public, immutable";
        }

        # Static assets
        location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg)$ {
            expires 1y;
            add_header Cache-Control "public, immutable";
        }
    }
}
```

### Step 4: SSL Certificate Setup

1. Generate self-signed certificate (for testing):
```bash
mkdir -p nginx/ssl
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout nginx/ssl/key.pem \
  -out nginx/ssl/cert.pem
```

2. For production, use Let's Encrypt:
```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
```

### Step 5: Deploy

1. Build and start services:
```bash
docker-compose -f docker-compose.prod.yml up -d --build
```

2. Run database migrations:
```bash
docker-compose -f docker-compose.prod.yml exec backend alembic upgrade head
```

3. Seed initial data:
```bash
docker-compose -f docker-compose.prod.yml exec backend python seed_database.py
```

### Step 6: Verify Deployment

1. Check service status:
```bash
docker-compose -f docker-compose.prod.yml ps
```

2. Check logs:
```bash
docker-compose -f docker-compose.prod.yml logs -f backend
docker-compose -f docker-compose.prod.yml logs -f frontend
```

3. Test endpoints:
```bash
curl -k https://yourdomain.com/api/v1/health
```

## Monitoring and Maintenance

### Health Checks

Add health check endpoints to `docker-compose.prod.yml`:
```yaml
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
  interval: 30s
  timeout: 10s
  retries: 3
```

### Log Management

1. Configure log rotation:
```bash
sudo nano /etc/logrotate.d/ai-interview
```

2. Add log rotation config:
```
/var/log/ai-interview/*.log {
    daily
    missingok
    rotate 52
    compress
    delaycompress
    notifempty
    create 644 www-data www-data
    postrotate
        docker-compose -f /path/to/docker-compose.prod.yml restart nginx
    endscript
}
```

### Backup Strategy

1. Database backup script:
```bash
#!/bin/bash
BACKUP_DIR="/backups/ai-interview"
DATE=$(date +%Y%m%d_%H%M%S)
docker-compose -f docker-compose.prod.yml exec postgres pg_dump -U postgres ai_interview_db > $BACKUP_DIR/backup_$DATE.sql
```

2. File backup:
```bash
rsync -av /path/to/uploads/ /backups/uploads/
```

## Scaling

### Horizontal Scaling

1. Load balance multiple backend instances:
```yaml
backend:
  build: ./backend
  deploy:
    replicas: 3
```

2. Use external database and Redis services

### Performance Optimization

1. Enable Redis caching
2. Use CDN for static assets
3. Implement database connection pooling
4. Add application-level caching

## Security Checklist

- [ ] Change default passwords
- [ ] Use strong JWT secrets
- [ ] Enable HTTPS
- [ ] Configure firewall rules
- [ ] Set up intrusion detection
- [ ] Regular security updates
- [ ] Backup encryption
- [ ] Access control policies

## Troubleshooting

### Common Issues

1. **Database Connection Failed**
   - Check DATABASE_URL format
   - Verify PostgreSQL is running
   - Check network connectivity

2. **Frontend Not Loading**
   - Check nginx configuration
   - Verify build process completed
   - Check CORS settings

3. **File Upload Issues**
   - Check upload directory permissions
   - Verify file size limits
   - Check disk space

4. **AI API Errors**
   - Verify API keys
   - Check rate limits
   - Review API quotas

### Debug Commands

```bash
# Check container logs
docker-compose -f docker-compose.prod.yml logs [service_name]

# Enter container shell
docker-compose -f docker-compose.prod.yml exec [service_name] bash

# Restart services
docker-compose -f docker-compose.prod.yml restart [service_name]

# View resource usage
docker stats
```

## Rollback Plan

1. Keep previous version tagged:
```bash
docker tag ai-interview-backend:latest ai-interview-backend:previous
```

2. Rollback command:
```bash
docker-compose -f docker-compose.prod.yml down
docker tag ai-interview-backend:previous ai-interview-backend:latest
docker-compose -f docker-compose.prod.yml up -d
```

## Support

For deployment issues:
1. Check logs for error messages
2. Verify environment variables
3. Test individual components
4. Contact support with logs and configuration details
