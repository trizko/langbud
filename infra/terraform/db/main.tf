terraform {
  required_providers {
    digitalocean = {
      source  = "digitalocean/digitalocean"
      version = "~> 2.0"
    }
  }
  backend "s3" {
    endpoint                    = "sfo3.digitaloceanspaces.com"
    key                         = "langbud-db.tfstate"
    bucket                      = "langbud-terraform-state"
    region                      = "us-east-1"
    skip_credentials_validation = true
    skip_metadata_api_check     = true
  }
}

provider "digitalocean" {
  token = var.do_token
}

resource "digitalocean_database_cluster" "db_cluster" {
  name       = "langbud-db"
  engine     = "pg"
  version    = "15"
  size       = "db-s-1vcpu-2gb"
  region     = "sfo3"
  node_count = 1
}
