Hotel Booking API with Django REST Framework
https://via.placeholder.com/800x400?text=Hotel+Booking+API

A RESTful API for hotel room booking management with user authentication, hotel/room management, and booking reservation system.

Features
🏨 Hotel Management - Create, update, view and delete hotels

🛏️ Room Management - Manage room inventory

📅 Booking System - Reserve rooms with date conflict checking

👤 User Accounts - User registration and authentication

📊 Admin Dashboard - Django admin interface for management

API Endpoints
Endpoint	Methods	Description
/users/	POST, PATCH, GET	User registration and management
/hotel/	POST, PATCH, GET, DELETE	Hotel CRUD operations
/room/	POST, PATCH, GET, DELETE	Room CRUD operations
/booking/	GET, POST	Booking management with HTML view
Technology Stack
Backend: Django 3.2+, Django REST Framework

Database: SQLite (can be configured for PostgreSQL)

Authentication: Session-based (extendable to Token/JWT)

Templates: Django HTML templates for booking views
