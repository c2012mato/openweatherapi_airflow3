# OpenWeather API ETL with Airflow 3

This project implements an ETL (Extract, Transform, Load) pipeline to fetch weather data from the [OpenWeatherMap API](https://openweathermap.org/api), store it in a PostgreSQL database, and visualize it using Metabase. The entire workflow is orchestrated by Apache Airflow 3.

## ✨ Features

- **Automated Data Extraction**: Regularly fetches weather data for specified locations.
- **Robust Orchestration**: Uses Apache Airflow for scheduling, monitoring, and managing the ETL pipeline.
- **Scalable Data Storage**: Leverages PostgreSQL for storing weather data.
- **Easy Database Management**: Includes pgAdmin for easy interaction with the PostgreSQL database.
- **Insightful Visualization**: Connects to Metabase for creating dashboards and visualizing the weather data.
- **Local Development**: Utilizes Airflow's `LocalExecutor` for easy setup and execution on a single machine.

## 🏗️ Architecture

The pipeline follows a simple, yet effective, data flow:

1.  **Airflow DAG**: A Directed Acyclic Graph (DAG) is scheduled to run at a regular interval.
2.  **Extract**: The DAG triggers a task that calls the OpenWeatherMap API to fetch the latest weather data.
3.  **Transform**: The raw JSON data from the API is transformed and cleaned into a structured format.
4.  **Load**: The transformed data is loaded into a table in the PostgreSQL database.
5.  **Visualize**: Metabase is connected to the PostgreSQL database, allowing for the creation of interactive charts and dashboards to analyze the weather data.

```
+---------------------+      +----------------+      +-----------------+      +----------------+
| OpenWeatherMap API  |----->|  Airflow 3     |----->|   PostgreSQL    |<-----|     pgAdmin    |
+---------------------+      | (Orchestration)|      +-----------------+      +----------------+
                             +----------------+              ^
                                                             |
                                                             |
                                                     +-------+--------+
                                                     |    Metabase    |
                                                     | (BI Dashboard) |
                                                     +----------------+
```

## 🛠️ Tech Stack

- **Orchestration**: [Apache Airflow 3](https://airflow.apache.org/)
- **Database**: [PostgreSQL](https://www.postgresql.org/)
- **DB Interface**: [pgAdmin](https://www.pgadmin.org/)
- **BI Tool**: [Metabase](https://www.metabase.com/)
- **Executor**: Airflow `LocalExecutor`
- **Containerization**: [Docker](https://www.docker.com/) & [Docker Compose](https://docs.docker.com/compose/)

## 📁 Project Structure

```
.
├── dags/                 # Airflow DAGs
│   └── weather_etl_dag.py
├── plugins/              # Custom Airflow plugins (if any)
├── logs/                 # Logs from Airflow tasks
├── docker-compose.yml    # Docker Compose file for all services
├── Dockerfile            # Dockerfile for the Airflow image
└── README.md
```

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
