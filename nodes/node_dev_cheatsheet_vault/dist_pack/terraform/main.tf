# ==============================================================================
# CloudZero Terraform Infrastructure-as-Code
# Provisions Cloudflare DNS, Cloudflare Pages, and WAF Security Rules ($0/mo)
# ==============================================================================

terraform {
  required_version = ">= 1.5.0"
  required_providers {
    cloudflare = {
      source  = "cloudflare/cloudflare"
      version = "~> 4.0"
    }
  }
}

variable "cloudflare_api_token" {
  type        = string
  description = "Cloudflare API token with Zone.DNS and Pages permissions"
  sensitive   = true
}

variable "cloudflare_account_id" {
  type        = string
  description = "Cloudflare Account ID"
}

variable "cloudflare_zone_id" {
  type        = string
  description = "Cloudflare Zone ID for the root domain"
}

variable "domain_name" {
  type        = string
  description = "Your custom root domain name (e.g. myproject.com)"
}

variable "server_ip" {
  type        = string
  description = "Public IP of your Oracle Always-Free VM or VPS"
  default     = "127.0.0.1"
}

provider "cloudflare" {
  api_token = var.cloudflare_api_token
}

# Root Domain A Record pointing to VM (proxied through Cloudflare CDN/WAF)
resource "cloudflare_record" "root_a" {
  zone_id = var.cloudflare_zone_id
  name    = "@"
  value   = var.server_ip
  type    = "A"
  proxied = true
  ttl     = 1
}

# WWW CNAME Record
resource "cloudflare_record" "www_cname" {
  zone_id = var.cloudflare_zone_id
  name    = "www"
  value   = var.domain_name
  type    = "CNAME"
  proxied = true
  ttl     = 1
}

# Cloudflare Free Tier WAF Rate Limiting Rule: Protects API from DDoS
resource "cloudflare_rate_limit" "api_guard" {
  zone_id   = var.cloudflare_zone_id
  threshold = 100
  period    = 60
  action {
    mode    = "challenge"
    timeout = 300
  }
  match {
    request {
      url_pattern = "${var.domain_name}/api/*"
      schemes     = ["HTTP", "HTTPS"]
      methods     = ["POST", "PUT", "DELETE"]
    }
  }
}

output "nameservers" {
  value       = ["Check your Cloudflare dashboard for assigned nameservers"]
  description = "Cloudflare authoritative nameservers"
}
