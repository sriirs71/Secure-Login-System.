# Secure Login System

A robust and secure user authentication web application built with Python, Flask, and SQLite. This project demonstrates modern security practices, including password hashing, session management, and optional Two-Factor Authentication (2FA), wrapped in a premium "glassmorphism" user interface.

## 🚀 Features

* **Secure Password Hashing:** Uses `bcrypt` with salt to securely store user passwords.
* **SQL Injection Protection:** Utilizes parameterized database queries to prevent SQL injection attacks.
* **Robust Session Management:** Implements server-side filesystem sessions via `Flask-Session` to securely track logged-in users and prevent session hijacking.
* **Two-Factor Authentication (2FA):** Optional Time-Based One-Time Password (TOTP) integration using `pyotp` and dynamically generated SVG QR codes for authenticator apps (Google Authenticator, Authy, etc.).
* **Premium UI/UX:** Responsive, modern design featuring vibrant gradients, glassmorphism card effects, and dynamic background animations built with pure CSS.
* **Flash Messaging:** User-friendly error and success notifications.

## 🛠️ Technology Stack

* **Backend:** Python 3, Flask
* **Database:** SQLite3
* **Authentication/Security:** bcrypt, pyotp, Flask-Session
* **Frontend:** HTML5, CSS3 (Vanilla, Glassmorphism design), Jinja2 Templates

## 📂 Project Structure

```text
├── app.py                  # Main Flask application and route definitions
├── db.py                   # Database connection and initialization logic
├── requirements.txt        # Python dependencies
├── .gitignore              # Files to ignore in version control
├── static/
│   └── style.css           # Premium CSS styling and animations
└── templates/
    ├── base.html           # Base Jinja2 layout
    ├── index.html          # Secure dashboard
    ├── login.html          # Login form
    ├── register.html       # Registration form
    ├── setup_2fa.html      # QR code generation and 2FA setup
    └── verify_2fa.html     # 2FA token verification during login
```

## ⚙️ Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone <your-github-repo-url>
   cd secure-login-system
   ```

2. **(Optional but Recommended) Create a virtual environment:**
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application:**
   ```bash
   python app.py
   ```
   *Note: The database (`secure_login.db`) and the necessary tables will be created automatically the first time you run the app.*

5. **Access the application:**
   Open your web browser and navigate to `http://127.0.0.1:5000`

## 🔒 Security Highlights

* **No Plaintext Passwords:** Even in the event of a database breach, user passwords remain secure due to `bcrypt` hashing.
* **Protected Routes:** Dashboard and 2FA setup pages cannot be accessed without an active, validated session.
* **TOTP Verification:** Enforces a secondary authentication layer that changes every 30 seconds, heavily mitigating credential stuffing and phishing attacks.

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the [issues page](issues-url).



