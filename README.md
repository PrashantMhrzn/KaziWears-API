# KaziWears API Documentation

## Project Overview
KaziWears is an e-commerce backend API built with Django REST Framework. The system provides a complete online shopping platform with user authentication, product management, shopping cart functionality, and order processing.

## Technology Stack
- **Backend**: Django 5.2.8
- **API Framework**: Django REST Framework
- **Authentication**: Djoser (Token-based)
- **Database**: SQLite (Development) / PostgreSQL (Production)
- **API Documentation**: DRF Spectacular (OpenAPI/Swagger)
- **Payment Integration**: Stripe API

## API Endpoints

### Authentication (Djoser)
All authentication endpoints are prefixed with `/api/auth/`

**User Registration & Management**
- `POST /api/auth/users/` - Register new user
- `POST /api/auth/users/activation/` - Activate user account
- `POST /api/auth/users/resend_activation/` - Resend activation email
- `GET /api/auth/users/me/` - Get current user profile
- `PUT /api/auth/users/me/` - Update current user profile
- `PATCH /api/auth/users/me/` - Partial update current user profile
- `DELETE /api/auth/users/me/` - Delete current user account

**Token Management**
- `POST /api/auth/token/login/` - Login (get authentication token)
- `POST /api/auth/token/logout/` - Logout (invalidate token)

**Password Management**
- `POST /api/auth/users/set_password/` - Set new password
- `POST /api/auth/users/reset_password/` - Request password reset
- `POST /api/auth/users/reset_password_confirm/` - Confirm password reset

**Username Management**
- `POST /api/auth/users/set_username/` - Set new username
- `POST /api/auth/users/reset_username/` - Request username reset
- `POST /api/auth/users/reset_username_confirm/` - Confirm username reset

### Products
Endpoint: `/api/products/`

**Operations**
- `GET /api/products/` - List all products
- `POST /api/products/` - Create new product (Seller/Admin only)
- `GET /api/products/{id}/` - Retrieve specific product
- `PUT /api/products/{id}/` - Update product (Seller/Admin only)
- `PATCH /api/products/{id}/` - Partial update product (Seller/Admin only)
- `DELETE /api/products/{id}/` - Delete product (Seller/Admin only)

### Categories
Endpoint: `/api/category/`

**Operations**
- `GET /api/category/` - List all categories
- `POST /api/category/` - Create new category (Admin only)
- `GET /api/category/{id}/` - Retrieve specific category
- `PUT /api/category/{id}/` - Update category (Admin only)
- `PATCH /api/category/{id}/` - Partial update category (Admin only)
- `DELETE /api/category/{id}/` - Delete category (Admin only)

### Cart Management
Endpoint: `/api/cart/`

**Basic Cart Operations**
- `GET /api/cart/` - Get user's cart
- `POST /api/cart/` - Create cart (auto-created on first item add)
- `GET /api/cart/{id}/` - Get cart by ID (Admin only)
- `PUT /api/cart/{id}/` - Update cart (Admin only)
- `PATCH /api/cart/{id}/` - Partial update cart (Admin only)
- `DELETE /api/cart/{id}/` - Delete cart (Admin only)

**Cart Item Operations**
- `POST /api/cart/add-to-cart/` - Add product to cart
  - Request Body: `{"product_code": "ABC123", "quantity": 2}`
- `POST /api/cart/checkout/` - Checkout cart and create order

### Orders
Endpoint: `/api/orders/`

**Operations**
- `GET /api/orders/` - List user's orders
- `POST /api/orders/` - Create order (via checkout)
- `GET /api/orders/{id}/` - Get order details
- `PUT /api/orders/{id}/` - Update order (Admin/Seller only)
- `PATCH /api/orders/{id}/` - Partial update order (Admin/Seller only)
- `DELETE /api/orders/{id}/` - Delete order (Admin only)

### Payment
Endpoint: `/api/payment/`

**Operations**
- `GET /api/payment/` - List payments (Admin only)
- `POST /api/payment/` - Create payment
- `GET /api/payment/{id}/` - Get payment details
- `PUT /api/payment/{id}/` - Update payment (Admin only)
- `PATCH /api/payment/{id}/` - Partial update payment (Admin only)
- `DELETE /api/payment/{id}/` - Delete payment (Admin only)
- `POST /api/payment/{id}/confirm/` - Confirm payment

## Authentication
All protected endpoints require authentication. Include the token in request headers:
```
Authorization: Token <your_auth_token>
```

## API Documentation Access
- Swagger UI: `http://localhost:8000/api/docs/`
- ReDoc: `http://localhost:8000/api/redoc/`
