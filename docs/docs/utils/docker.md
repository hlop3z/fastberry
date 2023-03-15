# **Docker**

Using **docker** for **deployment**

---

## Docker**File**

---

```dockerfile title="Dockerfile"
# syntax=docker/dockerfile:1

# Base Configurations
FROM python:3.10-alpine

# Copy Data to "project/"
WORKDIR /project
COPY . .

# Scripts: Before Starting
# RUN apk add curl
RUN python3 -m pip install -r requirements.txt

# Run App
ENTRYPOINT ["python3"]
CMD ["manage.py", "run", "--port", "8080", "--workers", "1"]
```

### **Create** Image

```sh
docker build -t fastberry-image .
```

---

### **Run** Image

```sh
docker run -d --name fastberry_app -p 8080:8080 fastberry-image
```

---

## Docker **Compose**

---

```yaml title="docker-compose.yaml"
networks:
  # Network(s)
  shared:
    driver: bridge

services:
  # App | Container
  app:
    container_name: fastberry_app
    ports:
      - "8080:8080"
    volumes:
      - ./data:/data
    build:
      context: .
    # restart: always
```

### **Run** via Compose

```sh
docker compose up -d
```

---

## **Custom** Image (**Save | Load**)

---

### **Save** Image

```sh
docker save fastberry-image | gzip > project.tar.gz
```

### **Load** Image

```sh
docker load -i project.tar.gz
```
