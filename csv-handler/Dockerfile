# Docker image to run the csv utlity
FROM python:3.11-slim
LABEL developer="Jayant Sogikar" version="1.0" description="A Docker image to run a CSV utility for processing CSV files"
# Get dependencies
COPY . .
RUN pip install -r requirements.txt
# Set the entrypoint to the csv utility
ENTRYPOINT ["python3", "-u", "csv_reader.py"]
# Set the default command to run the utility
CMD ["--help"]