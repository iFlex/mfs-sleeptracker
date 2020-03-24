# mfs-fitness

Service that reports on fitness data and pulls it from various sources
First implemented source is FitBit - needs unit testing
Second source is a manual insert frontend - still under development

Requirements:
1. External Scheduling - AirFlow or Cron
2. External InfluxDB installation + credentials
3. FitBit Application credentials
4. Working_dir folder accessible to user running the application
