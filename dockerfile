FROM apache/airflow:2.1.1-python3.8

# Install Java as root
USER root

# Step 1: Update package lists and install Java runtime first
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        openjdk-11-jre-headless && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Step 2: Install ca-certificates-java and openjdk-11-jdk
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        ca-certificates-java \
        openjdk-11-jdk && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    # Verify Java is installed
    command -v java >/dev/null 2>&1 || { echo "Java installation failed"; exit 1; } && \
    java -version

# Set Java environment variables
ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
ENV PATH="${JAVA_HOME}/bin:${PATH}"

# Switch back to airflow user
USER airflow

# Verify Java is available for airflow user
RUN command -v java >/dev/null 2>&1 || { echo "Java not found for airflow user"; exit 1; } && \
    java -version

# Install Python packages
RUN pip install \
    spotipy \
    pycryptodome \
    loguru \
    boto3 \
    pyspark==3.3.2 \
    findspark
