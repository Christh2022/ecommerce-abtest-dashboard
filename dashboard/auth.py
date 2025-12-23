"""
Authentication Module for E-Commerce Dashboard
Provides Flask-Login based authentication with session management
"""

import os
from flask import Flask, session, redirect, url_for
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user
from werkzeug.security import check_password_hash, generate_password_hash
import json
from datetime import timedelta
from functools import wraps


class User(UserMixin):
    """User model for Flask-Login"""
    
    def __init__(self, id, username, email=None, role='user', force_password_change=False):
        self.id = id
        self.username = username
        self.email = email
        self.role = role
        self.force_password_change = force_password_change
    
    def __repr__(self):
        return f'<User {self.username}>'


class AuthManager:
    """Manages authentication for the Dash application"""
    
    def __init__(self, app_server):
        """
        Initialize authentication manager
        
        Args:
            app_server: Flask server instance from Dash app
        """
        self.server = app_server
        self.login_manager = LoginManager()
        self.login_manager.init_app(app_server)
        self.login_manager.login_view = '/login'
        
        # Configure session
        self.server.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-change-in-production')
        self.server.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=24)
        
        # User database (in production, use a real database)
        self.users_db = self._load_users()
        
        # Set up user loader
        @self.login_manager.user_loader
        def load_user(user_id):
            return self.get_user_by_id(user_id)
    
    def _load_users(self):
        """Load users from config file or environment"""
        users_file = os.path.join(os.path.dirname(__file__), 'users.json')
        
        # Default users if file doesn't exist
        default_users = {
            'admin': {
                'id': '1',
                'username': 'admin',
                'password': generate_password_hash('admin123'),
                'email': 'admin@example.com',
                'role': 'admin',
                'force_password_change': True
            },
            'user': {
                'id': '2',
                'username': 'user',
                'password': generate_password_hash('user123'),
                'email': 'user@example.com',
                'role': 'user',
                'force_password_change': True
            }
        }
        
        if os.path.exists(users_file):
            try:
                with open(users_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        
        # Save default users
        try:
            with open(users_file, 'w') as f:
                json.dump(default_users, f, indent=2)
        except:
            pass
        
        return default_users
    
    def get_user_by_username(self, username):
        """Get user by username"""
        user_data = self.users_db.get(username)
        if user_data:
            return User(
                id=user_data['id'],
                username=user_data['username'],
                email=user_data.get('email'),
                role=user_data.get('role', 'user'),
                force_password_change=user_data.get('force_password_change', False)
            )
        return None
    
    def get_user_by_id(self, user_id):
        """Get user by ID"""
        for user_data in self.users_db.values():
            if user_data['id'] == user_id:
                return User(
                    id=user_data['id'],
                    username=user_data['username'],
                    email=user_data.get('email'),
                    role=user_data.get('role', 'user'),
                    force_password_change=user_data.get('force_password_change', False)
                )
        return None
    
    def verify_password(self, username, password):
        """Verify username and password"""
        user_data = self.users_db.get(username)
        if user_data and check_password_hash(user_data['password'], password):
            return True
        return False
    
    def authenticate_user(self, username, password, remember=False):
        """
        Authenticate user and create session
        
        Returns:
            User object if successful, None otherwise
        """
        if self.verify_password(username, password):
            user = self.get_user_by_username(username)
            if user:
                login_user(user, remember=remember)
                return user
        return None
    
    def logout_current_user(self):
        """Logout current user"""
        logout_user()
    
    def change_password(self, username, new_password):
        """
        Change user password and remove force_password_change flag
        
        Returns:
            True if successful, False otherwise
        """
        if username not in self.users_db:
            return False
        
        self.users_db[username]['password'] = generate_password_hash(new_password)
        self.users_db[username]['force_password_change'] = False
        
        # Save to file
        try:
            users_file = os.path.join(os.path.dirname(__file__), 'users.json')
            with open(users_file, 'w') as f:
                json.dump(self.users_db, f, indent=2)
            return True
        except:
            return False
    
    def add_user(self, username, password, email=None, role='user'):
        """
        Add a new user (admin only)
        
        Returns:
            True if successful, False otherwise
        """
        if username in self.users_db:
            return False
        
        new_id = str(len(self.users_db) + 1)
        self.users_db[username] = {
            'id': new_id,
            'username': username,
            'password': generate_password_hash(password),
            'email': email,
            'role': role,
            'force_password_change': False
        }
        
        # Save to file
        try:
            users_file = os.path.join(os.path.dirname(__file__), 'users.json')
            with open(users_file, 'w') as f:
                json.dump(self.users_db, f, indent=2)
            return True
        except:
            return False


def require_login(func):
    """Decorator to require login for Dash callbacks"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect('/login')
        return func(*args, **kwargs)
    return wrapper
