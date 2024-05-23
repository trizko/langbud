output "server_ip" {
  value = digitalocean_droplet.langbud-server.ipv4_address
}

output "db_host" {
  value = digitalocean_database_cluster.db-cluster.host
}

output "db_port" {
  value = digitalocean_database_cluster.db-cluster.port
}

output "db_username" {
  value = digitalocean_database_cluster.db-cluster.user
}

output "db_password" {
  value = digitalocean_database_cluster.db-cluster.password
  sensitive = true
}