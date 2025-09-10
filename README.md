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

## 🚀 Getting Started

### Prerequisites

- [Docker](https://www.docker.com/get-started) and [Docker Compose](https://docs.docker.com/compose/install/)
- An API key from [OpenWeatherMap](https://home.openweathermap.org/api_keys)

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/c2012mato/openweatherapi_airflow3.git
    cd openweatherapi_airflow3
    ```

2.  **Set up environment variables:**
    Create a `.env` file in the root of the project and add your OpenWeatherMap API key:
    ```env
    OPENWEATHER_API_KEY=your_api_key_here
    ```

3.  **Configure Airflow Connections:**
    You'll need to set up an Airflow connection for your PostgreSQL database. This can be done via the Airflow UI once it's running.
    - **Conn Id**: `postgres_default`
    - **Conn Type**: `Postgres`
    - **Host**: `postgres`
    - **Schema**: `airflow`
    - **Login**: `airflow`
    - **Password**: `airflow`
    - **Port**: `5432`

    Also, add your OpenWeather API key as an Airflow Variable.
    - **Key**: `OPENWEATHER_API_KEY`
    - **Value**: `your_api_key_here`

4.  **Build and run the services:**
    ```bash
    docker-compose up --build
    ```

### Accessing the Services

- **Airflow UI**: [http://localhost:8080](http://localhost:8080) (Login with `airflow`/`airflow`)
- **pgAdmin**: [http://localhost:5050](http://localhost:5050)
- **Metabase**: [http://localhost:3000](http://localhost:3000)

## 📖 Usage

1.  **Enable the DAG**: Open the Airflow UI, find the `weather_etl_dag`, and enable it.
2.  **Trigger the DAG**: You can wait for the scheduled run or trigger it manually from the UI.
3.  **View Data in pgAdmin**: Once the DAG has run successfully, you can connect to the PostgreSQL server in pgAdmin to see the newly populated tables.
4.  **Create Dashboards in Metabase**:
    - Log in to Metabase and set up a new database connection to your PostgreSQL instance.
    - Use the same credentials as the Airflow connection. The hostname will be `postgres`.
    - Start exploring the data and building your dashboards!

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

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
