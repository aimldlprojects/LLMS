server {
    listen 80;
    server_name gmgp-theia-dev.pfizer.com;

    # Redirect HTTP to HTTPS
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl;
    server_name gmgp-theia-dev.pfizer.com;

    ssl_certificate /etc/nginx/ssl/gmgp-theia-dev.pfizer.pem;
    ssl_certificate_key /etc/nginx/ssl/gmgp-theia-dev.pfizer.com_key.pem;

    # Serve React frontend from /usr/share/nginx/html
    location / {
        root /usr/share/nginx/html;  # React build directory
        index index.html index.htm;
        try_files $uri $uri/ /index.html;
        add_header 'Access-Control-Allow-Origin' '*';
        add_header 'Access-Control-Allow-Credentials' 'true';
        add_header 'Access-Control-Allow-Methods' 'GET, POST, OPTIONS';
        add_header 'Access-Control-Allow-Headers' 'Accept, Content-Type';
        client_max_body_size 200M;
    }

    # API Requests - Proxy to the backend
    location /api/ {
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_pass http://backend:8010;  # Update backend container name and port
    }

    # Favicon request handling
    location = /favicon.ico {
        access_log off;
        log_not_found off;
    }

    # Static files
    location /staticfiles/ {
        root /usr/share/nginx/etl-dashboard;
    }

    # Media files
    location /media/ {
        root /usr/share/nginx/etl-dashboard;
    }

    # Handle 50x errors
    error_page 500 502 503 504 /50x.html;
    location = /50x.html {
        root /usr/share/nginx/html;
    }
}
