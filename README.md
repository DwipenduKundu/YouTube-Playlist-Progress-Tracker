# YouTube Playlist Progress Tracker

A Django-based web application that helps users organize YouTube playlists, watch videos, and track their learning progress in one place.

## 🚀 Features

- **User Authentication** – Register, log in, and securely manage your account.
- **Import YouTube Playlists** – Add YouTube playlists using their playlist URLs.
- **Automatic Playlist Fetching** – Retrieve playlist information and videos using the YouTube Data API.
- **Video Player** – Watch playlist videos directly inside the application.
- **Progress Tracking** – Track video-watching progress and completion status.
- **Playlist Management** – View and manage your saved playlists.
- **Django Admin Panel** – Manage application data through Django's administration interface.
- **Responsive Interface** – Access the application across different screen sizes.

## 🛠️ Technologies Used

| Technology                | Purpose                            |
| ------------------------- | ---------------------------------- |
| Python                    | Backend programming                |
| Django                    | Web framework                      |
| HTML5                     | Page structure                     |
| CSS3                      | Styling and responsive design      |
| JavaScript                | Frontend interactions              |
| PostgreSQL                | Production database                |
| SQLite                    | Local development database         |
| YouTube Data API v3       | Fetch YouTube playlist information |
| YouTube IFrame Player API | Embedded video playback            |
| Render                    | Deployment and hosting             |
| Git & GitHub              | Version control                    |

## 📁 Project Structure

```text
YouTubeProgressTracker/
│
├── config/
│   ├── settings.py
│   ├── urls.py
│   ├── __init__.py
│   ├── asgi.py
│   └── wsgi.py
│
├── tracker/
│   ├── migrations/
│   ├── templates/
│   │   └── tracker
│   │       ├── register.html
│   │       ├── login.html
│   │       ├── dashboard.html 
│   │       ├── playlist_detail.html
│   │       ├── password_reset.html
│   │       ├── password_reset_done.html
│   │       ├── password_reset_confirm.html
│   │       ├── password_reset_complete.html
│   │       ├── password_reset_email.html
│   │       └── password_reset_subject.txt
│   │
│   ├── static/
│   │   └── tracker
│   │       ├── css
│   │       │   ├── register.css
│   │       │   ├── login.css
│   │       │   ├── dashboard.css 
│   │       │   ├── playlist_detail.css
│   │       │   └── password_reset.css
│   │       │
│   │       └── js
│   │           ├── dashboard.js
│   │           └── playlist_detail.js
│   │
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── forms.py
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   └── services/
│
├── manage.py
├── requirements.txt
├── build.sh
├── .gitignore
└── db.sqlite3
```

## ⚙️ Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/DwipenduKundu/YouTube-Playlist-Progress-Tracker
```

### 2. Navigate to the project directory

```bash
cd YouTubeProgressTracker
```

### 3. Create a virtual environment

```bash
python -m venv venv
```

Activate it:

**Linux / macOS**

```bash
source venv/bin/activate
```

**Windows**

```bash
venv\Scripts\activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure environment variables

Create a `.env` file in the project root.

```bash
touch .env
code .env
```

Configure the following variables in your local environment:

```env
SECRET_KEY=your_django_secret_key
DEBUG=True
YOUTUBE_API_KEY=your_youtube_api_key
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_gmail_app_password
```

For production, configure the database and other required environment variables securely through your hosting provider.

**Note:** Never upload your actual secret keys, passwords, or API credentials to GitHub.

### 6. Apply database migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 7. Create an Admin Account

```bash
python manage.py createsuperuser
```

### 8. Start the development server

```bash
python manage.py runserver
```

Open the application:

```text
http://127.0.0.1:8000/
```

Django Admin:

```text
http://127.0.0.1:8000/admin/
```

## 🌐 Deployment

The application is deployed using **Render**.

### 🔗 Project Links

- 🌐 **Live Application:** [Open Todo Application](https://youtube-playlist-progress-tracker.onrender.com)
- 💻 **GitHub Repository:** [View Source Code](https://github.com/DwipenduKundu/YouTube-Playlist-Progress-Tracker)
- 🔐 **Admin Panel:** [Django Admin](https://youtube-playlist-progress-tracker.onrender.com/admin)


Production deployment uses:

- Render Web Service
- Render PostgreSQL database
- Environment variables for sensitive configuration
- Django database migrations
- Static file collection

## Future Improvements

- Dashboard with task statistics
- Task reminders and notifications

## 🔐 Security

- Django authentication system.
- Passwords managed using Django's built-in password hashing.
- Sensitive configuration stored in environment variables.
- Production database credentials are not committed to GitHub.

## 🎯 Project Objective

The main objective of this project is to make online learning more organized by allowing users to save YouTube playlists, watch educational videos, and monitor their learning progress.

## 👨‍💻 Author

**Dwipendu Kundu**

Computer Science and Engineering Graduate

GitHub: [Dwipendu Kundu](https://github.com/DwipenduKundu)
---

⭐ If you find this project useful, consider giving the repository a star!
