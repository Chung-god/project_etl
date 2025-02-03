# 🚀 Amazon ML Challenge 2023 ETL Pipeline

## **Project Overview**
This project focuses on building an **ETL (Extract, Transform, Load) pipeline** using data from the **Amazon ML Challenge 2023**. The primary goal is to **process large-scale data efficiently using Spark** and **store it in AWS for analysis and visualization**.

### **Ultimate Goal**
- Develop a **React-based frontend** for mock data collection and traffic simulation.
- Implement an **admin panel** for CRM data visualization and management.
- Build an **end-to-end data pipeline** to handle real-time and batch processing.

---

## **📌 ETL Pipeline Architecture**
Below is a high-level overview of the ETL pipeline:

![ETL Pipeline Diagram](./docs/etl_pipeline.png) *(Replace with actual image path in GitHub repo)*

### **1️⃣ Extract (데이터 추출)**
- **Source**: Amazon ML Challenge dataset
- **Process**:
  - Load raw data from local storage or an external source.
  - Parse and structure the data using Spark.

### **2️⃣ Transform (데이터 변환)**
- **Process**:
  - Clean and preprocess data (handling missing values, normalization, etc.).
  - Generate meaningful metrics for further analysis.
  - Aggregate, filter, and optimize data.

### **3️⃣ Load (데이터 적재)**
- **Destination**:
  - AWS **S3** (for raw and processed data storage)
  - AWS **RDS** (for structured, relational data)
- **Process**:
  - Store cleaned data for future use in machine learning models and dashboards.

---

## **🗂 Folder Structure**

project-etl/
│
├── data/               # Raw and processed data storage
├── scripts/            # ETL scripts
│   ├── extract.py      # Extracts data from source
│   ├── transform.py    # Processes and cleans data
│   └── load.py         # Loads data into AWS
├── dashboards/         # Tableau dashboards
├── docker/             # Docker-related configurations
│   ├── Dockerfile      # Defines the containerized environment
│   ├── docker-compose.yml  # Multi-container setup
├── frontend/           # React-based web application
│   ├── src/            # Frontend source code
│   ├── public/         # Static files
│   ├── package.json    # Dependencies
├── docs/               # Documentation files
│   ├── etl_pipeline.png  # ETL pipeline diagram
├── README.md           # Project documentation
└── requirements.txt    # Python dependencies

---

## **🔧 Setup & Installation**
### **1️⃣ Prerequisites**
Ensure you have the following installed:
- **Python 3.8+**
- **Docker 20.10+**
- **AWS CLI (configured)**
- **Tableau (for visualization)**

### **2️⃣ Clone the Repository**
```bash
git clone https://github.com/your-repo/project-etl.git
cd project-etl

3️⃣ Run Docker

docker-compose up

4️⃣ Run ETL Scripts

python scripts/extract.py
python scripts/transform.py
python scripts/load.py

5️⃣ View Tableau Dashboard

Open Tableau and connect to the processed data stored in AWS RDS.

🚀 Future Enhancements
	•	✅ Develop a frontend dashboard using React for better data visualization.
	•	✅ Simulate mock traffic and analyze user behavior trends.
	•	✅ Enhance automation for real-time data processing.
	•	✅ Deploy the project on AWS for full-scale production.
