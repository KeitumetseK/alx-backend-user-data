# User Authentication Service

## Project Overview
This project is a simple user authentication service built using Flask, designed to handle tasks such as user registration, login, session management, password reset, and more. It provides a RESTful API for interacting with the service, utilizing HTTP methods for various endpoints.

## Requirements
- **Python Version:** 3.7
- **Flask Version:** 1.1.2
- **pycodestyle Version:** 2.5

## Features
- **User Registration**: Allows users to register with an email and password.
- **User Login**: Authenticates users and creates a session.
- **Session Management**: Manages user sessions via cookies.
- **User Profile**: Retrieves user profile information.
- **Password Reset**: Allows users to reset their password using a reset token.
- **Session Logout**: Handles session destruction upon logout.

## Endpoints
Here are the key endpoints provided by the service:

### 1. Register User
- **Method**: `POST`
- **URL**: `/users`
- **Payload**:
  ```json
  {
    "email": "user@example.com",
    "password": "password123"
  }

