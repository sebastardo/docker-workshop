import pandas as pd
from sqlalchemy import create_engine
from tqdm.auto import tqdm
import click

dtype = {
    "VendorID": "Int64",
    "passenger_count": "Int64",
    "trip_distance": "float64",
    "RatecodeID": "Int64",
    "store_and_fwd_flag": "string",
    "PULocationID": "Int64",
    "DOLocationID": "Int64",
    "payment_type": "Int64",
    "fare_amount": "float64",
    "extra": "float64",
    "mta_tax": "float64",
    "tip_amount": "float64",
    "tolls_amount": "float64",
    "improvement_surcharge": "float64",
    "total_amount": "float64",
    "congestion_surcharge": "float64"
}

parse_dates = [
    "tpep_pickup_datetime",
    "tpep_dropoff_datetime"
]


@click.command()
@click.option('--user', default='root', help='PostgreSQL user')
@click.option('--password', default='root', help='PostgreSQL password')
@click.option('--host', default='localhost', help='PostgreSQL host')
@click.option('--port', default=5432, type=int, help='PostgreSQL port')
@click.option('--db', default='ny_taxi', help='PostgreSQL database name')
@click.option('--table', default='yellow_taxi_data', help='Target table name')
@click.option('--year', default='2019', help='Year of the file')
@click.option('--month', default='1', help='Month of the file')
def run(user, password, host, port, db, table, year, month):

    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')

    prefix = 'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/'
    
    df_iter = pd.read_csv(
        prefix+ f'yellow_tripdata_{year}-01.csv.gz',
        iterator=True,
        chunksize=100000,
        dtype=dtype,
        parse_dates=parse_dates
    )

    first_chunk = next(df_iter)

    first_chunk.head(0).to_sql(
        name=table,
        con=engine,
        if_exists="replace"
    )

    print("Table created")

    first_chunk.to_sql(
        name=table,
        con=engine,
        if_exists="append"
    )

    for df_chunk in tqdm(df_iter):
        df_chunk.to_sql(
            name=table,
            con=engine,
            if_exists="append"
        )
        print("Inserted chunk:", len(df_chunk))


if __name__ == "__main__":
    run()



'''
uv run python ingest_data.py \
  --user=root \
  --password=root \
  --host=localhost \
  --port=5432 \
  --db=ny_taxi \
  --table=yellow_taxi_trips \
  --year=2021 \
  --month=2
'''