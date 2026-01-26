# Falco Runtime Security Monitoring

## Overview

Falco is configured to monitor the E-commerce Dashboard services for security threats and suspicious activities.

## Monitored Services

- **Dash Application** (ecommerce-dashboard)
- **Grafana** (ecommerce-grafana)
- **PostgreSQL** (ecommerce-postgres)

## Monitoring Rules

### Dash Application Monitoring

- **Unauthorized File Write**: Detects writes outside expected directories (/app/logs, /tmp, /var)
- **Database Connection Monitoring**: Tracks connections to PostgreSQL (INFO level)
- **Suspicious Process**: Alerts on unexpected process execution
- **Environment Variable Access**: Monitors access to .env files
- **Port Binding Change**: Detects attempts to bind to ports other than 8050

### Grafana Monitoring

- **Configuration Modification**: Detects changes to /etc/grafana/\*
- **Datasource Modification**: Monitors datasource configuration changes
- **Dashboard Export**: Tracks dashboard JSON file access
- **Plugin Installation**: Alerts on grafana-cli install commands
- **Database File Access**: Monitors grafana.db modifications

### PostgreSQL Monitoring

- **Data Directory Write**: Alerts on unauthorized writes to /var/lib/postgresql/data
- **Configuration Change**: Detects modifications to postgresql.conf, pg_hba.conf
- **Shell Access**: Alerts on shell spawning (bash, sh, zsh)
- **Backup Access**: Monitors access to backup/dump files
- **Table Drop**: Critical alert on DROP TABLE commands

### Cross-Service Monitoring

- **Suspicious Inter-Service Communication**: Detects unexpected network connections between services
- **Service Container File Execution**: Alerts on execution from /tmp directory

## Alert Priorities

- **CRITICAL**: Immediate action required (malware, intrusion)
- **ERROR**: Serious security violations (DROP TABLE, shell access, data exfiltration)
- **WARNING**: Suspicious activity requiring investigation
- **INFO**: Normal activity logging for audit trail
- **DEBUG**: Verbose logging for troubleshooting

## Configuration Files

- `falco/falco.yaml`: Main Falco configuration
- `falco/falco_rules.local.yaml`: Custom monitoring rules for Dash, Grafana, PostgreSQL

## Viewing Falco Logs

### Real-time monitoring

```bash
docker logs -f ecommerce-falco
```

### Filter by service

```bash
# Dash events
docker logs ecommerce-falco | grep "Dash"

# Grafana events
docker logs ecommerce-falco | grep "Grafana"

# PostgreSQL events
docker logs ecommerce-falco | grep "PostgreSQL"
```

### Filter by priority

```bash
# Critical and Error only
docker logs ecommerce-falco | grep -E "priority=ERROR|priority=CRITICAL"

# Warnings
docker logs ecommerce-falco | grep "priority=WARNING"
```

### Recent events

```bash
docker logs ecommerce-falco --since 1h
```

## Common Events

### Expected Events (INFO/DEBUG)

These are normal operations:

- Dash connecting to PostgreSQL database
- Grafana dashboard access
- PostgreSQL connection accepted

### Warning Events

Require investigation:

- Unexpected process execution
- Configuration file modifications
- Plugin installations
- Environment file access

### Critical/Error Events

Immediate action required:

- Shell access in containers
- DROP TABLE commands
- Unauthorized data directory writes
- Large outbound data transfers (possible exfiltration)

## Integration with Monitoring Stack

Falco events can be integrated with:

- **Prometheus**: Export metrics via Falco exporter
- **Grafana**: Visualize security events
- **Elasticsearch**: Store and search security logs
- **Slack/PagerDuty**: Real-time alerting

## Health Check

Falco exposes a health webserver on port 8765 (internal):

```bash
# From inside the container
wget -qO- http://localhost:8765/healthz
```

## Resource Usage

- **CPU Limit**: 0.5 cores
- **Memory Limit**: 256MB
- **CPU Reservation**: 0.1 cores
- **Memory Reservation**: 128MB

## Troubleshooting

### Falco not detecting events

1. Check if Falco is running: `docker ps | grep falco`
2. Check logs for errors: `docker logs ecommerce-falco | grep Error`
3. Verify rules loaded: `docker logs ecommerce-falco | grep "Loading rules"`
4. Test with a simple action (e.g., access Dash app)

### High resource usage

- Adjust log verbosity in falco.yaml
- Reduce monitored syscalls
- Filter events by priority

### False positives

- Adjust rules in falco_rules.local.yaml
- Add exceptions for known safe processes
- Change priority from WARNING to INFO

## Security Best Practices

1. **Review logs daily** for unusual activity
2. **Alert on ERROR/CRITICAL** events immediately
3. **Investigate WARNING** events within 24 hours
4. **Tune rules** based on your environment
5. **Rotate logs** to prevent disk space issues
6. **Backup rules** before modifications
7. **Test rule changes** in development first

## Maintenance

### Update Falco

```bash
docker-compose pull falco
docker-compose up -d falco
```

### Modify rules

1. Edit `falco/falco_rules.local.yaml`
2. Restart Falco: `docker-compose restart falco`
3. Verify: `docker logs ecommerce-falco | grep "Loading rules"`

### Disable custom rules temporarily

Edit `falco/falco.yaml` and comment out:

```yaml
# - /etc/falco/falco_rules.local.yaml
```

Then restart Falco.

## Support

- Falco Documentation: https://falco.org/docs/
- Falco Rules: https://github.com/falcosecurity/rules
- Issues: File a GitHub issue with logs attached
