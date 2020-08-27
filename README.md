# website-monitor: hassle free website availability monitoring toolset

website-monitor is a toolkit containing of a front and back application interfering by Apache Kafka allowing to monitor websites content availability storing monitoring data in PostgreSQL database. 


## Usage

### Configuration
``` yaml
check_every_seconds_default: 1
log_level: { DEBUG / INFO }
kafka_connect:
     uri: '%kafka endpoint uri%'
     topic: 'website-monitor'
  cafile: config/ca.pem
  certfile: config/service.cert
  keyfile: config/service.key
websites:
  - url: https://www.website.com
    patterns:
      - '.*text.*'
target:
  postgres_uri: '%postgres full grade uri%'
```

### Monitoring
``` python
python run_monitoring.py --config=config/config.yml
```

### Data writing
``` python
python run_writer.py --config=config/config.yml
```