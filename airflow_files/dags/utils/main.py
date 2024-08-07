import awswrangler as wr
import boto3
import pandas as pd
import requests


def extract_file(url):
    """
    Extracts country data from the REST Countries API and formats it into
    a list of dictionaries.

    The function makes a GET request to the REST Countries API
    ("https://restcountries.com/v3.1/all") to retrieve data about all
    countries. It then processes the data to extract and format specific
    information into a list of dictionaries, where each dictionary contains
    details about a country. This data includes:
    - country name: The common name of the country.
    - independency: Indicates whether the country is independent
      (Boolean value).
    - United Nation Member: Indicates whether the country is a
      member of the United Nations (Boolean value).
    - startOfWeek: The day of the week on which the country starts its week.
    - And all other listed columns in the main code.

    The columns `Currency Code`, `Currency name`, and `Currency symbol`
    are derived from the `currencies` field in the API response.
    The `Country code` is constructed from the `idd` (International Direct
    Dialing) field, combining the `root` and the first `suffix`.
    The `Capital` is extracted from the `capital` field, which may contain
    a list of capital cities, with the first entry used.

    Returns:
        list: A list of dictionaries, each containing information about a
        country.
    """
    response = requests.get(url)
    data = response.json()

    country_list = []  # Initialize country_list outside the loop
    for item in data:
        currencies = item.get("currencies", {})
        currency_values = list(currencies.values())
        first_currency = currency_values[0] if currency_values else {}
        currency_name = first_currency.get("name", "")
        currency_symbol = first_currency.get("symbol", "")
        idd = item.get('idd', {})
        root = idd.get('root', '')
        suffixes = idd.get('suffixes', [''])
        first_suffix = suffixes[0] if suffixes else ''

        countries = {
            "country name": item.get("name", {}).get("common", ""),
            "independency": item.get("independent", None),
            "United Nation Member": item.get("unMember", ""),
            "startOfWeek": item.get("startOfWeek", ""),
            "Official country name": item.get("name", {}).get("official", ""),
            "Common native name": next(
                iter(item.get("name", {}).get("nativeName", {}).values()), {}
            ).get("common", ""),
            "Area": item.get("area", 0),
            "Population": item.get("population", 0),
            "Region": item.get("region", ""),
            "Sub region": item.get("subregion", ""),
            "Continents": ", ".join(item.get("continents", [])),
            "Languages": ", ".join(item.get("languages", {}).values()),
            "Currency Code": next(iter(item.get("currencies", {}).keys()), ""),
            "Currency name": currency_name,
            "Currency symbol": currency_symbol,
            "Country code": f"+{root}{first_suffix}",
            "Capital": next(iter(item.get("capital", [""])), ""),
        }
        # Append each country's data to the list
        country_list.append(countries)
    return country_list  # Return the full list after the loop


# Extract the data and convert it to a DataFrame
country_list = extract_file(url="https://restcountries.com/v3.1/all")
df = pd.DataFrame(country_list)
# print(df)


# copying the extracted dataset to s3 bucket
def copy_to_s3(df):
    bucket_name = "apidataset"
    s3_path = f's3://{bucket_name}/api_countries_dataset.parquet'
    # Write DataFrame to Parquet and upload to S3
    wr.s3.to_parquet(
        df=df,
        path=s3_path,
        # optional if AWS credentials are already configured
        boto3_session=boto3.Session(),
        dataset=True,
        mode="append",
        database="api_data",
        table="api_countries"
    )


copy_to_s3(df)
print("Parquet file uploaded successfully!")
