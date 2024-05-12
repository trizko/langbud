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
  name   = "langbud-server"
  image  = "debian-10-x64"
  region = "sfo3"
  size   = "s-1vcpu-1gb"

  user_data = templatefile("${path.module}/user-data.tpl", { DO_TOKEN = var.do_token })

  ssh_keys = [
    var.ssh_fingerprint
  ]
}
