# System Metrics Collector for Grafana

## Overview
This Python script collects system metrics such as CPU usage, memory usage, disk usage, and network I/O statistics. It logs the collected data into files and inserts it into a MariaDB database for visualization with Grafana.

## Features
- Collects CPU usage percentage.
- Retrieves virtual memory statistics.
- Monitors disk usage.
- Tracks network I/O statistics.
- Logs data into timestamped files.
- Inserts collected data into a MariaDB database.

## Requirements
### Dependencies
This script requires the following Python libraries:
- `psutil` (for system metrics collection)
- `mariadb` (for database interactions)
- `logging` (for error handling)

You can install the required dependencies using:
```bash
pip install -r requirements.txt
```

### Database Setup
Ensure that you have a MariaDB instance running with a database named `monitoring`. You should have tables for CPU, memory, disk, and network usage:

```sql
CREATE TABLE cpu_percent (
    id INT AUTO_INCREMENT PRIMARY KEY,
    percent FLOAT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE virtual_mem (
    id INT AUTO_INCREMENT PRIMARY KEY,
    total BIGINT,
    available BIGINT,
    percent FLOAT,
    used BIGINT,
    free BIGINT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE disk (
    id INT AUTO_INCREMENT PRIMARY KEY,
    total BIGINT,
    used BIGINT,
    free BIGINT,
    percent FLOAT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE net_usage (
    id INT AUTO_INCREMENT PRIMARY KEY,
    bytes_sent BIGINT,
    bytes_recv BIGINT,
    packets_sent BIGINT,
    packets_recv BIGINT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## Usage
### Running the Script
To start collecting metrics, simply run:
```bash
python collector.py
```
The script will collect data every 5 seconds and store it in log files and the database.

### Log Files
Each metric is stored in a daily log file with a naming convention like `DDMMYYYY-cpu_percent.log`.

### Stopping the Script
Press `CTRL+C` to stop execution.

## Integration with Grafana
1. Configure Grafana to connect to your MariaDB instance.
2. Add a new data source in Grafana:
   - Select `MySQL/MariaDB`.
   - Enter the database details.
3. Create dashboards using queries like:
   ```sql
   SELECT percent, timestamp FROM cpu_percent ORDER BY timestamp DESC;
   ```
4. Visualize the collected data in graphs.
