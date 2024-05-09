terraform {
  required_providers {
    digitalocean = {
      source  = "digitalocean/digitalocean"
      version = "~> 2.0"
    }
  }
}

provider "digitalocean" {
  token = var.do_token
}

resource "digitalocean_droplet" "web_server" {
  name   = "web-server"
  image  = "debian-10-x64"
  region = "sfo3"
  size   = "s-1vcpu-1gb"

  user_data = file("${path.module}/user-data.sh")

  ssh_keys = [
    var.ssh_fingerprint
  ]
}
