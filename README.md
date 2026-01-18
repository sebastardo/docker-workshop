# Run Pipeline

_Ahora offline!_  
_Ahora en linux!_

## Docker

### 1.Network
`docker network create pg-network`

### 2.postgresql
```
docker run -it \
  -e POSTGRES_USER="root" \
  -e POSTGRES_PASSWORD="root" \
  -e POSTGRES_DB="ny_taxi" \
  -v ny_taxi_postgres_data:/var/lib/postgresql \
  -p 5432:5432 \
  --network=pg-network \
  --name pgdatabase \
  postgres:18
```

### 3.pgadmin
```
docker run -it \
  -e PGADMIN_DEFAULT_EMAIL="admin@admin.com" \
  -e PGADMIN_DEFAULT_PASSWORD="root" \
  -v pgadmin_data:/var/lib/pgadmin \
  -p 8085:80 \
  --network=pg-network \
  --name pgadmin \
  dpage/pgadmin4
```

### 4.pipeline
`docker build -t taxi_ingest:v001 .`

```
docker run -it \
  --network=pg-network \. 
  taxi_ingest:v001 \
    --user=root \
    --password=root \
    --host=pgdatabase \
    --port=5432 \
    --db=ny_taxi \
    --table=yellow_taxi_trips \
    --year=2021 \
    --month=2
```

## docker-compose

`docker compose up`

`docker network ls` con la respuesta cambio el `--nerwork` del pipeline


