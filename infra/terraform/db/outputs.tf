output "host" {
  value = digitalocean_database_cluster.db-cluster.host
}

output "port" {
  value = digitalocean_database_cluster.db-cluster.port
}

output "username" {
  value = digitalocean_database_cluster.db-cluster.user
}

output "password" {
  value = digitalocean_database_cluster.db-cluster.password
  sensitive = true
}