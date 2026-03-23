#!/bin/bash
# Firewall initialization for secure automation pipeline execution
# This script restricts network access to only essential services

# Note: iptables requires root/CAP_NET_ADMIN, so firewall rules
# must be configured at container startup, not runtime.
# For Docker, use --cap-add=NET_ADMIN flag.

# Allow DNS (required for all network operations)
# iptables -A OUTPUT -p udp --dport 53 -j ACCEPT
# iptables -A OUTPUT -p tcp --dport 53 -j ACCEPT

# Allow AWS Bedrock (us-east-2)
# iptables -A OUTPUT -d bedrock-runtime.us-east-2.amazonaws.com -j ACCEPT
# iptables -A OUTPUT -d sts.us-east-2.amazonaws.com -j ACCEPT
# iptables -A OUTPUT -d sts.amazonaws.com -j ACCEPT

# Allow Telegram API
# iptables -A OUTPUT -d api.telegram.org -j ACCEPT

# Allow Facebook API (optional)
# iptables -A OUTPUT -d graph.facebook.com -j ACCEPT

# Block everything else
# iptables -A OUTPUT -j DROP

# Note: Firewall rules commented out by default because:
# 1. iptables requires NET_ADMIN capability (security risk for dev)
# 2. Most local dev environments don't need strict network isolation
# 3. Container orchestrators (Docker, K8s) provide network policies at higher level
#
# For production deployment, uncomment rules and run container with:
# docker run --cap-add=NET_ADMIN ...

# Run the pipeline
exec "$@"
