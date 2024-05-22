output "host" {
  value = digitalocean_database_cluster.db_cluster.host
}

output "port" {
  value = digitalocean_database_cluster.db_cluster.port
}

output "username" {
  value = digitalocean_database_cluster.db_cluster.user
}

output "password" {
  value = digitalocean_database_cluster.db_cluster.password
  sensitive = true
}