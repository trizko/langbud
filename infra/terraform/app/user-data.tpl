#!/bin/bash
set -euxo pipefail

########################
### SCRIPT VARIABLES ###
########################

# Name of the user to create and grant sudo privileges
USERNAME=langbud-server

# Whether to copy over the root user's `authorized_keys` file to the new sudo
# user.
COPY_AUTHORIZED_KEYS_FROM_ROOT=true

OTHER_PUBLIC_KEYS_TO_ADD=(
    "${CI_CD_SSH_PUBLIC_KEY}"
)

####################
### SCRIPT LOGIC ###
####################

# Add sudo user and grant privileges
useradd --create-home --shell "/bin/bash" --groups sudo "$USERNAME"
echo "$USERNAME ALL=(ALL) NOPASSWD: ALL" | EDITOR='tee -a' visudo

# Create SSH directory for sudo user
home_directory="$(eval echo ~$USERNAME)"
mkdir --parents "$home_directory/.ssh"

# Copy `authorized_keys` file from root if requested
if [ "$COPY_AUTHORIZED_KEYS_FROM_ROOT" = true ]; then
    cp /root/.ssh/authorized_keys "$home_directory/.ssh"
fi

# Add additional provided public keys
for pub_key in "$OTHER_PUBLIC_KEYS_TO_ADD[@]"; do
    echo "$pub_key" >> "$home_directory/.ssh/authorized_keys"
done

# Adjust SSH configuration ownership and permissions
chmod 0700 "$home_directory/.ssh"
chmod 0600 "$home_directory/.ssh/authorized_keys"
chown --recursive "$USERNAME":"$USERNAME" "$home_directory/.ssh"

# Disable root SSH login with password
sed --in-place 's/^PermitRootLogin.*/PermitRootLogin no/g' /etc/ssh/sshd_config
if sshd -t -q; then
    systemctl restart sshd
fi

# Install UFW firewall
apt update
apt install ufw

# Add exception for SSH and then enable UFW firewall
ufw allow OpenSSH
ufw allow 8000
ufw --force enable

# Install docker and login to digitalocean image registry
wget -O install_docker.sh get.docker.com
sh ./install_docker.sh
docker login -u ${DO_TOKEN} -p ${DO_TOKEN} registry.digitalocean.com

# Create systemd files for managing langbud-server docker container
cat <<EOF > /etc/systemd/system/langbud-server.service
[Unit]
Description=langbud-server

[Service]
ExecStartPre=docker pull registry.digitalocean.com/ai-stuff-registry/langbud-server:${ENVIRONMENT}
ExecStart=docker run --init --rm -p 0.0.0.0:8000:8000 --name=langbud-server registry.digitalocean.com/ai-stuff-registry/langbud-server:${ENVIRONMENT}
ExecStop=docker stop langbud-server
User=root

Restart=always
RestartSec=30

[Install]
WantedBy=multi-user.target
EOF