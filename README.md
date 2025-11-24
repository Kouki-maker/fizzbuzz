## Requirements

- Docker & Docker Compose

## Quick Start with docker 

```bash
# Clone repository
git clone https://github.com/Kouki-maker/fizzbuzz
cd fizzbuzz
````

```bash
# Build containers
docker-compose build && docker-compose up -d
```

The API is available in http://localhost:8000

## Test the API

```bash
# test fizz-buzz endpoint
curl "http://localhost:8000/fizz-buzz?int1=3&int2=5&str1=fizz&str2=buzz&limit=50"
```

```bash
# Get the most used parameters of the most used endpoint
curl http://localhost:8000/stats
```
