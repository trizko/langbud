variable "do_token" {
  type        = string
  default     = ""
  description = "DigitalOcean API Token"
}

variable "ssh_fingerprint" {
  type        = string
  default     = ""
  description = "SSH Key Fingerprint"
}

variable "ci_cd_ssh_public_key" {
  type        = string
  default     = ""
  description = "CI/CD SSH Public Key"
}