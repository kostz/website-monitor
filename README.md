# website-monitor: hassle free website availability monitoring toolset

website-monitor is a toolset containing of a front and back application interfering by Apache Kafka allowing to monitor websites content availability storing monitoring data in PostgreSQL backend database. 


## Configuration
``` yaml
check_every_seconds_default: 1
log_level: INFO
kafka_connect:
  uri: ''
  topic: 'website-monitor'
  cafile: config/ca.pem
  certfile: config/service.cert
  keyfile: config/service.key
websites:
  - url: https://www.website.com
    check_every_seconds: 5
    patterns:
      - '.*text.*'
target:
  postgres_uri: ''
```

parameter | details | possible values
--- | --- | ---
check_every_seconds_default | default polling interval applied for all websites | 
log_level | log level | INFO/DEBUG
kafka_connect | Apache Kafka connection parameters | 
kafka_connect.uri | Apache Kafka endpoint URI|
kafka_connect.topic | Apache Kafka topic, will be created automatically if absent|
kafka_connect.{cafile/ certfile/ keyfile} | Apache Kafka credential files location |
websites |list of monitored websites|
websites.url |URL of a website|
websites.check_every_seconds | optional polling interval |
websites.patterns | optional list of regexp patterns to verify website contents |
target | backend PostgreSQL database connection
target.postgres_uri | PostgreSQL database URI |



## Usage
### Monitoring
``` python
python run_monitoring.py --config=config/config.yml
```

### Data writing
``` python
python run_writer.py --config=config/config.yml
```

## Database schema
Monitoring data is written to PostgreSQL database containing of two tables automatically created in public schema
### website
column | details 
--- | --- 
id | internal website id, primary key | 
url | website url |
### website_mon
column | details 
--- | ---
request_time | probe time | 
website_id | website id, foreign key to website table |
elapsed | time taken for get request |
http_status_code | http get status code, 999 if request fails |
pattern_match | result of pattern match, null if no pattern defined for a website |
