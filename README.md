# MiniTube

A simple YouTube-like video sharing platform built with Django, featuring user authentication, video uploads via YouTube embed links, like/dislike system, comments, and popularity scoring.

## Features

- **User Authentication**: Register, login, and user profiles
- **Video Management**: Upload videos using YouTube embed links
- **Social Features**: Like/dislike videos, add comments
- **Popular Videos**: Algorithm-based popularity scoring system
- **Viewing History**: Track user video viewing history with pagination
- **Scalable Architecture**: Docker containerization with Nginx load balancing

## Popularity Scoring Algorithm

Videos are ranked based on:
- **Likes**: +10 points each
- **Dislikes**: -5 points each  
- **Comments**: +1 point each
- **Recency**: +100 points per day since creation

## Technology Stack

- **Backend**: Django 5.2.4
- **Database**: PostgreSQL
- **Frontend**: Django Templates with Tailwind CSS
- **Containerization**: Docker & Docker Compose
- **Web Server**: Nginx (load balancing)
- **WSGI Server**: Gunicorn

## Quick Start

### Prerequisites

- Docker
- Docker Compose

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd minitube
```

2. Build and start the containers:
```bash
docker-compose up --build
```

3. Create a superuser (in a new terminal):
```bash
docker-compose exec web python manage.py createsuperuser
```

4. Access the application:
- **Main Site**: http://localhost
- **Admin Panel**: http://localhost/admin

**Note**: Environment variables are configured directly in `docker-compose.yml`. For production, consider using environment files or secrets management.

## Project Structure

```
minitube/
├── accounts/          # User authentication and profiles
├── videos/           # Video management and display
├── interactions/     # Likes, comments, and views
├── templates/        # Django templates
├── static/          # Static files (CSS, JS)
├── docker-compose.yml
├── Dockerfile
├── nginx.conf
└── requirements.txt
```

## API Endpoints

- `/` - Home page with random videos
- `/video/<id>/` - Video detail page
- `/upload/` - Upload new video (authenticated)
- `/popular/` - Most popular videos
- `/history/` - User viewing history (authenticated)
- `/accounts/register/` - User registration
- `/accounts/profile/` - User profile (authenticated)
- `/login/` - Login page
- `/logout/` - Logout

## Docker Architecture

The application uses a scalable Docker setup:

1. **Nginx Container**: Load balancer and static file server
2. **Django Container**: Application server with Gunicorn
3. **PostgreSQL Container**: Database server

### Static Files

Static files (CSS, JavaScript, images) are automatically collected during container startup and served through Nginx. The setup includes:
- Automatic `collectstatic` command execution
- Shared volume between Django and Nginx containers
- Proper static file serving configuration

## Testing

Run tests for the popular videos and history features:
```bash
python manage.py test
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

This project is licensed under the MIT License. 