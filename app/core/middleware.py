from fastapi import Request, HTTPException, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from typing import Dict, List, Tuple
import time
from collections import defaultdict
from app.core.config import settings
import hashlib

class RateLimitMiddleware(BaseHTTPMiddleware):
    """Advanced Rate Limiting Middleware"""
    
    def __init__(self, app):
        super().__init__(app)
        self.requests: Dict[str, List[float]] = defaultdict(list)
        self.blocked_ips: Dict[str, float] = {}
        self.whitelist = ["127.0.0.1", "localhost"]
    
    async def dispatch(self, request: Request, call_next):
        if not settings.RATE_LIMIT_ENABLED:
            return await call_next(request)
        
        # Get client IP
        client_ip = self._get_client_ip(request)
        
        # Skip whitelisted IPs
        if client_ip in self.whitelist:
            return await call_next(request)
        
        # Check if IP is blocked
        if client_ip in self.blocked_ips:
            block_time = self.blocked_ips[client_ip]
            if time.time() - block_time < 3600:  # Block for 1 hour
                return JSONResponse(
                    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                    content={
                        "error": "Too many requests",
                        "message": "Your IP has been temporarily blocked due to excessive requests",
                        "retry_after": int(3600 - (time.time() - block_time))
                    }
                )
            else:
                del self.blocked_ips[client_ip]
        
        # Clean old requests
        current_time = time.time()
        self.requests[client_ip] = [
            req_time for req_time in self.requests[client_ip]
            if current_time - req_time < settings.RATE_LIMIT_PERIOD
        ]
        
        # Check rate limit
        if len(self.requests[client_ip]) >= settings.RATE_LIMIT_REQUESTS:
            # Block IP if too many requests
            if len(self.requests[client_ip]) >= settings.RATE_LIMIT_REQUESTS * 2:
                self.blocked_ips[client_ip] = current_time
            
            return JSONResponse(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                content={
                    "error": "Rate limit exceeded",
                    "message": f"Maximum {settings.RATE_LIMIT_REQUESTS} requests per {settings.RATE_LIMIT_PERIOD} seconds",
                    "retry_after": settings.RATE_LIMIT_PERIOD
                }
            )
        
        # Add current request
        self.requests[client_ip].append(current_time)
        
        # Process request
        response = await call_next(request)
        
        # Add rate limit headers
        response.headers["X-RateLimit-Limit"] = str(settings.RATE_LIMIT_REQUESTS)
        response.headers["X-RateLimit-Remaining"] = str(
            settings.RATE_LIMIT_REQUESTS - len(self.requests[client_ip])
        )
        response.headers["X-RateLimit-Reset"] = str(
            int(current_time + settings.RATE_LIMIT_PERIOD)
        )
        
        return response
    
    def _get_client_ip(self, request: Request) -> str:
        """Get client IP from request"""
        forwarded = request.headers.get("X-Forwarded-For")
        if forwarded:
            return forwarded.split(",")[0].strip()
        return request.client.host if request.client else "unknown"

class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """Request Logging Middleware"""
    
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        
        # Log request
        print(f"📥 {request.method} {request.url.path}")
        
        # Process request
        response = await call_next(request)
        
        # Calculate processing time
        process_time = time.time() - start_time
        
        # Log response
        print(f"📤 {request.method} {request.url.path} - Status: {response.status_code} - Time: {process_time:.3f}s")
        
        # Add custom headers
        response.headers["X-Process-Time"] = str(process_time)
        response.headers["X-Application"] = settings.PROJECT_NAME
        
        return response

class IslamicHeadersMiddleware(BaseHTTPMiddleware):
    """Add Islamic headers and metadata"""
    
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        
        # Add Bismillah to response headers
        response.headers["X-Bismillah"] = "Bismillah-ir-Rahman-ir-Rahim"
        response.headers["X-Application-Name"] = settings.PROJECT_NAME
        response.headers["X-Application-Version"] = settings.VERSION
        
        return response

class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """Add security headers"""
    
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        
        # Security headers
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        response.headers["Content-Security-Policy"] = "default-src 'self'"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        
        return response

class ErrorHandlerMiddleware(BaseHTTPMiddleware):
    """Global Error Handler Middleware"""
    
    async def dispatch(self, request: Request, call_next):
        try:
            response = await call_next(request)
            return response
        except HTTPException as exc:
            return JSONResponse(
                status_code=exc.status_code,
                content={
                    "error": exc.detail,
                    "status_code": exc.status_code,
                    "path": request.url.path
                }
            )
        except Exception as exc:
            print(f"❌ Unhandled error: {str(exc)}")
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={
                    "error": "Internal server error",
                    "message": "An unexpected error occurred. Please try again later.",
                    "path": request.url.path
                }
            )
