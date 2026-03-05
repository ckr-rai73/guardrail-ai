const { Client } = require('ssh2');

const config = {
    host: '72.61.241.106',
    username: 'root',
    password: 'Muskan21072709@'
};

const nginxConfig = `
server {
    listen 80;
    server_name guardrailai.in www.guardrailai.in;
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl http2;
    server_name guardrailai.in www.guardrailai.in;

    ssl_certificate /etc/letsencrypt/live/guardrailai.in/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/guardrailai.in/privkey.pem;

    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
`;

const conn = new Client();
conn.on('ready', () => {
    console.log('SSH Ready');
    const cmd = `echo '${nginxConfig}' > /etc/nginx/sites-available/guardrail && ln -sf /etc/nginx/sites-available/guardrail /etc/nginx/sites-enabled/ && rm -f /etc/nginx/sites-enabled/default && nginx -t && systemctl reload nginx`;
    conn.exec(cmd, (err, stream) => {
        if (err) throw err;
        stream.on('close', (code) => {
            console.log('Nginx update finished with code ' + code);
            conn.end();
            process.exit(code);
        }).on('data', data => process.stdout.write(data)).stderr.on('data', data => process.stderr.write(data));
    });
}).connect(config);
