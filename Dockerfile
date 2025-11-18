FROM python:3.11-slim

# container's working directory
WORKDIR /app

# install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# copy application code + codeqc files
COPY src/__init__.py /app/src/
COPY src/ /app/src/
COPY tests/ /app/tests/
COPY pytest.ini /app/
COPY .flake8 /app/
COPY .pylintrc /app/

# the data files (input/output) are mounted as a volume via docker yml

# run test when container starts
CMD ["pytest", "tests/"]