terraform {
  required_providers {
    digitalocean = {
      source  = "digitalocean/digitalocean"
      version = "~> 2.0"
    }
  }
  backend "s3" {
    endpoint                    = "sfo3.digitaloceanspaces.com"
    key                         = "langbud-app.tfstate"
    bucket                      = "langbud-terraform-state"
    region                      = "us-east-1"
    skip_credentials_validation = true
    skip_metadata_api_check     = true
  }
}

provider "digitalocean" {
  token = var.do_token
}

locals {
  environment = terraform.workspace == "default" ? "dev" : terraform.workspace
}

resource "digitalocean_droplet" "langbud-server" {
  name   = "langbud-server-${local.environment}"
  image  = "debian-10-x64"
  region = "sfo3"
  size   = "s-1vcpu-1gb"

  user_data = templatefile("${path.module}/user-data.tpl", { DO_TOKEN = var.do_token })

  ssh_keys = [
    var.ssh_fingerprint
  ]
}

resource "digitalocean_database_cluster" "db-cluster" {
  name       = "langbud-db-cluster-${local.environment}"
  engine     = "pg"
  version    = "15"
  size       = "db-s-1vcpu-2gb"
  region     = "sfo3"
  node_count = 1
}

resource "digitalocean_database_db" "langbud-db" {
  cluster_id = digitalocean_database_cluster.db-cluster.id
  name       = "langbud-db"
}

resource "digitalocean_database_firewall" "db-firewall" {
  cluster_id = digitalocean_database_cluster.db-cluster.id

  rule {
    type  = "droplet"
    value = digitalocean_droplet.langbud-server.id
  }
}