#!/usr/bin/env bash
set -euo pipefail

APP_NAME="jtproject"
APP_DIR="/opt/apps/${APP_NAME}"
SERVICE_FILE="/etc/systemd/system/${APP_NAME}.service"
NGINX_SITE="/etc/nginx/sites-available/${APP_NAME}"
NGINX_ENABLED="/etc/nginx/sites-enabled/${APP_NAME}"
SUDOERS_FILE="/etc/sudoers.d/${APP_NAME}-deploy"

DEPLOY_USER=""
APP_RUN_USER="www-data"
DOMAIN=""
APP_PORT="8080"
ENABLE_CERTBOT="false"

usage() {
  cat <<EOF
Usage:
  sudo bash init-jtproject-server.sh \\
    --deploy-user <deploy-user> \\
    --domain <your-domain.com> \\
    [--app-run-user www-data] \\
    [--app-port 8080] \\
    [--enable-certbot]

Notes:
- This script initializes directories, systemd service, nginx reverse proxy, and sudoers whitelist.
- Run on Ubuntu/Debian server with internet access.
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --deploy-user)
      DEPLOY_USER="$2"; shift 2;;
    --app-run-user)
      APP_RUN_USER="$2"; shift 2;;
    --domain)
      DOMAIN="$2"; shift 2;;
    --app-port)
      APP_PORT="$2"; shift 2;;
    --enable-certbot)
      ENABLE_CERTBOT="true"; shift 1;;
    -h|--help)
      usage; exit 0;;
    *)
      echo "Unknown arg: $1"; usage; exit 1;;
  esac
done

if [[ -z "$DEPLOY_USER" || -z "$DOMAIN" ]]; then
  echo "Missing required args: --deploy-user and --domain"
  usage
  exit 1
fi

if ! id "$DEPLOY_USER" >/dev/null 2>&1; then
  echo "User not found: $DEPLOY_USER"
  exit 1
fi

echo "[1/7] Install runtime packages"
apt-get update
apt-get install -y nginx openjdk-17-jre-headless curl
if [[ "$ENABLE_CERTBOT" == "true" ]]; then
  apt-get install -y certbot python3-certbot-nginx
fi

echo "[2/7] Prepare app directories"
mkdir -p "$APP_DIR/releases" "$APP_DIR/backups"
touch "$APP_DIR/app.jar"
chown -R "$APP_RUN_USER":"$APP_RUN_USER" "$APP_DIR"

echo "[3/7] Create systemd service"
cat > "$SERVICE_FILE" <<EOF
[Unit]
Description=JtProject Spring Boot Service
After=network.target

[Service]
Type=simple
User=${APP_RUN_USER}
WorkingDirectory=${APP_DIR}
ExecStart=/usr/bin/java -Xms256m -Xmx1024m -jar ${APP_DIR}/app.jar
SuccessExitStatus=143
Restart=always
RestartSec=5
Environment=SPRING_PROFILES_ACTIVE=prod
Environment=SERVER_PORT=${APP_PORT}

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable --now "${APP_NAME}"

echo "[4/7] Configure nginx reverse proxy"
cat > "$NGINX_SITE" <<EOF
server {
    listen 80;
    server_name ${DOMAIN};

    location / {
        proxy_pass http://127.0.0.1:${APP_PORT};
        proxy_http_version 1.1;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}
EOF

ln -sf "$NGINX_SITE" "$NGINX_ENABLED"
nginx -t
systemctl reload nginx

echo "[5/7] Configure sudoers whitelist for deploy user"
cat > "$SUDOERS_FILE" <<EOF
Defaults:${DEPLOY_USER} !requiretty

${DEPLOY_USER} ALL=(root) NOPASSWD: \\
  /bin/mkdir -p ${APP_DIR}, \\
  /bin/mkdir -p ${APP_DIR}/releases/*, \\
  /bin/mkdir -p ${APP_DIR}/backups, \\
  /bin/cp /tmp/app.jar ${APP_DIR}/releases/*/app.jar, \\
  /bin/cp ${APP_DIR}/releases/*/app.jar ${APP_DIR}/app.jar, \\
  /bin/cp ${APP_DIR}/app.jar ${APP_DIR}/backups/app-*.jar, \\
  /bin/mv ${APP_DIR}/java-projects/JtProject/target/app.jar ${APP_DIR}/app.jar, \\
  /bin/rm -rf ${APP_DIR}/java-projects, \\
  /bin/chown -R ${APP_RUN_USER}:${APP_RUN_USER} ${APP_DIR}, \\
  /bin/systemctl daemon-reload, \\
  /bin/systemctl restart ${APP_NAME}, \\
  /bin/systemctl status ${APP_NAME} --no-pager
EOF

chmod 440 "$SUDOERS_FILE"
visudo -cf "$SUDOERS_FILE"

echo "[6/7] Optional certbot setup"
if [[ "$ENABLE_CERTBOT" == "true" ]]; then
  certbot --nginx -d "$DOMAIN" || true
fi

echo "[7/7] Final status"
systemctl status "${APP_NAME}" --no-pager || true
systemctl status nginx --no-pager || true

echo "Done."
echo "Health check examples:"
echo "  curl -I http://127.0.0.1:${APP_PORT}"
echo "  curl -I http://${DOMAIN}"
