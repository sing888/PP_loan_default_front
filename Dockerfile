FROM python:3.9.slim

# Set the working directory
WORKDIR /app

# Copy the current directory contents into the container
COPY . /app

# Install dependencies
RUN pip install -r requirements.txt

# Expose the port Streamlit will run on
EXPOSE 8501

# Command to run the app
CMD ["streamlit", "run", "app.py"]
