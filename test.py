server {
    listen 80;
    server_name gmgp-theia-dev.pfizer.com;

    # Forward HTTP requests to HTTPS
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl;
    server_name gmgp-theia-dev.pfizer.com;

    ssl_certificate /etc/nginx/ssl/gmgp-theia-dev.pfizer.pem;
    ssl_certificate_key /etc/nginx/ssl/gmgp-theia-dev.pfizer.com_key.pem;

    # Serve React frontend
    location / {
        root /usr/share/nginx/html;  # React build output directory
        try_files $uri /index.html;
    }

    # Proxy backend API requests
    location /api/ {
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_pass http://backend:8010;  # Update backend port here
    }
}
