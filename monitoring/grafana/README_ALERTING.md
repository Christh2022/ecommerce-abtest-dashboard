# Grafana Alerting Configuration

This directory contains Grafana alerting configurations that are automatically provisioned on startup.

## Files

### alerts.yml
Defines alert rules for security and application monitoring:

**Security Alerts:**
- `suspicious_connections` - Detects suspicious network connections in Falco logs
- `shell_in_container` - Alerts when a shell is spawned inside a container
- `file_modifications` - Detects modifications to critical system files

**Application Alerts:**
- `high_error_rate` - Monitors Dash application error rate
- `database_failures` - Detects PostgreSQL connection failures
- `container_restart_loop` - Alerts on container restart loops

### notification-policies.yml
Configures notification routing and contact points:

**Contact Points:**
- `default-contact-point` - Email notifications for general alerts
- `security-team` - Email + Slack for security-critical alerts

**Routing Policies:**
- Security alerts (category=security) → security-team (1min interval)
- Warning/Critical alerts → default-contact-point (5min interval)

## Alert Severity Levels

- **Critical** - Immediate action required (security breaches, data loss)
- **High** - Urgent attention needed (shells in containers, file modifications)
- **Warning** - Investigation needed (high error rates, connection issues)

## Configuration

### Email Notifications
Update contact point email addresses in `notification-policies.yml`:
```yaml
settings:
  addresses: your-email@example.com
```

### Slack Notifications
1. Create a Slack webhook: https://api.slack.com/messaging/webhooks
2. Update the webhook URL in `notification-policies.yml`:
```yaml
settings:
  url: https://hooks.slack.com/services/YOUR/SLACK/WEBHOOK
  recipient: '#security-alerts'
```

### Custom Alert Rules

Add new rules to `alerts.yml`:
```yaml
- uid: your_alert_id
  title: Your Alert Title
  condition: A
  data:
    - refId: A
      datasourceUid: P8E80F9AEF21F6940
      model:
        expr: 'your_logql_query'
  for: 2m
  annotations:
    description: 'Alert description'
  labels:
    severity: high
    category: security
```

## LogQL Query Examples

### Detect failed login attempts
```logql
sum(count_over_time({container="ecommerce-dashboard"} |~ "(?i)(failed|unauthorized).*login" [5m])) > 3
```

### Monitor container resource usage
```logql
sum(count_over_time({container=~"ecommerce-.*"} |~ "(?i)(out of memory|oom)" [5m])) > 0
```

### Track configuration changes
```logql
sum(count_over_time({container="ecommerce-grafana"} |~ "(?i)(config|settings).*changed" [5m])) > 0
```

## Testing Alerts

### Trigger test alerts manually:

1. **Shell in Container:**
```bash
docker exec -it ecommerce-dashboard /bin/bash
```

2. **Database Connection Failure:**
```bash
docker exec ecommerce-postgres psql -U wronguser
```

3. **Generate Application Errors:**
```bash
curl http://localhost:8050/nonexistent-page
```

## Monitoring

View active alerts in Grafana:
- **Alerts Page:** http://localhost:3000/alerting/list
- **Alert Rules:** http://localhost:3000/alerting/rules
- **Notification History:** http://localhost:3000/alerting/notifications

## Troubleshooting

### Alerts not firing
1. Check Loki data source connection: http://localhost:3000/datasources
2. Verify logs are being collected: Check Loki metrics at http://localhost:3100/metrics
3. Test LogQL queries in Explore: http://localhost:3000/explore

### Notifications not sent
1. Verify contact point configuration in Grafana UI
2. Check SMTP settings if using email
3. Test webhook URLs manually with curl

### False positives
Adjust alert thresholds in `alerts.yml`:
- Increase `for` duration (evaluation time)
- Adjust query threshold values
- Add more specific log filters

## Best Practices

1. **Start with high thresholds** - Reduce false positives
2. **Test in staging** - Verify alerts before production
3. **Document runbooks** - Include resolution steps in annotations
4. **Regular reviews** - Adjust based on operational experience
5. **Keep queries simple** - Complex queries can miss events

## Related Documentation

- [Issue #56: Alerting Configuration](../docs/ISSUE56_COMPLETED.md)
- [Issue #55: Security Logs Dashboard](../docs/ISSUE55_COMPLETED.md)
- [Issue #52: Falco Security Monitoring](../docs/ISSUE52_COMPLETED.md)
- [Issue #53: Loki Log Aggregation](../docs/ISSUE53_COMPLETED.md)
