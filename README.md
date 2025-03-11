
# 🎵 **Spotify ETL Pipeline using Apache Airflow**  

This project is an **ETL (Extract, Transform, Load) pipeline** for **Spotify playlist data**, built using **Apache Airflow**. It automates the process of:  

- **Extracting** playlist track data from **Spotify API**  
- **Transforming** the data into a structured format using **PySpark**  
- **Loading** the transformed data into **AWS S3** for further analysis  

---
![Spotify Etl Pipeline](https://github.com/shivatadha/Spotify-ETL-Pipeline-using-Apache-Airflow/blob/185bebdc5dfabe069a4d1e80217d9a3d08345b0a/Spotify%20etl%20pipeline.png)
---

## 🚀 **Features**  

✔️ **Extract** → Fetches playlist track data from **Spotify API**  
✔️ **Transform** → Processes and cleans data using **Apache Spark**  
✔️ **Load** → Stores transformed data in **AWS S3** as **Parquet**  
✔️ **Cleanup** → Deletes temporary files after processing  
✔️ **Automation** → Uses **Apache Airflow DAGs** for scheduling  

---

## 📂 **Project Structure**  

```plaintext
spotify-etl-pipeline/
│── dags/                         # Airflow DAGs and ETL scripts
│   ├── fetch_spotify_data.py     # Extracts data from Spotify API
│   ├── spotify_transformation.py # Transforms raw JSON using PySpark
│   ├── parquet_writer.py         # Saves transformed data as Parquet
│   ├── upload_to_s3.py           # Uploads Parquet files to AWS S3
│   ├── cleanup_local_data.py     # Deletes local processed files
│   ├── config.py                 # Configuration file (API keys, paths)
│   ├── spark_session.py          # Initializes PySpark session
│   ├── s3_client_object.py       # Creates AWS S3 client using Boto3
│
│── data/                         # Data storage
│   ├── processed_data/           # Transformed data saved as Parquet
│   ├── raw_data/                 # Raw JSON data fetched from Spotify API
│
│── db/                           # Database-related files (if needed)
│── logs/                         # Airflow logs and pipeline logs
│── plugins/                      # Custom Airflow plugins (if needed)
│
│── test/                         # Testing framework
│   ├── test.py                   # Unit tests for ETL scripts
│
│── dockerfile                     # Docker container setup
│── docker-compose.yaml             # Docker Compose configuration
│── requirements.txt                # Dependencies
│── README.md                       # Project documentation
               
```

---

## 📜 **Module Breakdown**  

### 1️⃣ **Data Extraction - `fetch_spotify_data.py`**  
- Connects to **Spotify API** using **Spotipy**  
- Fetches playlist track metadata (**song name, artist, album, popularity, etc.**)  
- Saves data as a **JSON file** in the `raw_data/` directory  

### 2️⃣ **Data Transformation - `spotify_transformation.py`**  
- Uses **Apache Spark** to process raw JSON  
- Extracts structured **albums, artists, and songs information**  
- Cleans and **deduplicates** data before storage  

### 3️⃣ **Parquet Storage - `parquet_writer.py`**  
- Converts transformed data into **Parquet format** for optimized storage  
- Stores data in the `processed_data/` directory  

### 4️⃣ **Uploading to AWS S3 - `upload_to_s3.py`**  
- Uses **Boto3** to upload Parquet files to an **S3 bucket**  
- Runs **parallel uploads** using **multithreading** for efficiency  

### 5️⃣ **Cleanup Process - `cleanup_local_data.py`**  
- Deletes **raw & processed data** from local storage after successful upload  

### 6️⃣ **Configuration & Setup - `config.py`**  
- Stores **Spotify API credentials**  
- Stores **AWS S3 bucket details**  
- Defines local directories for **raw and processed data**  

### 7️⃣ **S3 Client Initialization - `s3_client_object.py`**  
- Creates a reusable **AWS S3 client** using **Boto3**  
- Provides secure access to **S3 for uploading files**  

### 8️⃣ **Spark Session Manager - `spark_session.py`**  
- Initializes **Apache Spark session** for data processing  
- Configures **Spark parameters** for performance tuning  

---

## 🛠️ **Tech Stack**  

🔹 **Apache Airflow** → ETL orchestration  
🔹 **Apache Spark** → Data processing & transformation  
🔹 **Spotipy** → Spotify API wrapper  
🔹 **Boto3** → AWS S3 integration  
🔹 **Parquet** → Optimized data storage format  
🔹 **Python** → Core programming language  

---

## ⚙️ **Installation & Setup**  

### 1️⃣ **Clone Repository**  

```bash
https://github.com/shivatadha/Spotify-ETL-Pipeline-using-Apache-Airflow.git
cd spotify-etl-airflow
```

### 2️⃣ **Install Dependencies**  

```bash
pip install -r requirements.txt
```

### 3️⃣ **Set Up Airflow**  

```bash
export AIRFLOW_HOME=~/airflow
airflow db init
airflow scheduler &
airflow webserver
```

### 4️⃣ **Set Up Configuration**  
- Open **`config.py`** and update your **Spotify API credentials** and **AWS S3 credentials**  

---

## 🏗️ **Running the Pipeline**  

1️⃣ Open **Airflow UI** → [http://localhost:8080](http://localhost:8080)  
2️⃣ **Trigger the `spotify_etl_dag`** to start the pipeline  

---

## 📌 **Future Improvements**  

✔️ **Integrate with PostgreSQL** for analytics  
✔️ **Add real-time streaming** using **Kafka**  
✔️ **Automate Spotify API token refresh**  

---

