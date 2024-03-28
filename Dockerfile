# My Base Image
FROM python:3.11.5-slim-bookworm

# Set Working Directory in the image
WORKDIR /DocQna

# Copy Everything for dockerfile loc to -> /DocQna in image
COPY . .

# pip install dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# The port to be exposed
EXPOSE 8501

# Command to run when the container starts
CMD [ "streamlit", "run", "./src/app.py", "--server.port=8501", "--server.address=0.0.0.0", "--server.maxUploadSize=4000" ]