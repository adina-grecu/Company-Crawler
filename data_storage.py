import json
import pandas as pd
from elasticsearch import Elasticsearch, helpers

ES_INDEX = 'company_profiles'

def load_data(filename):
    with open(filename, 'r') as f:
        return json.load(f)

def merge_data(scraped_data, company_names_csv):
    df_scraped = pd.DataFrame(scraped_data)
    df_company_names = pd.read_csv(company_names_csv)

    # Strip URL prefix 
    df_scraped['domain'] = df_scraped['website'].str.replace('https://', '').str.rstrip('/')
    df_scraped = df_scraped.drop(columns=['website'])

    # Merge data on domain
    merged_data = pd.merge(df_scraped, df_company_names, on='domain', how='outer')
    print(merged_data)
    
    return merged_data

def store_to_elasticsearch(data, index_name):
    es = Elasticsearch(hosts=['http://localhost:9200'])

    # Replace NaN values with None
    data = data.where(pd.notna(data), None)

    # Convert data to a format that Elasticsearch can understand
    records = data.to_dict(orient='records')

    CHUNK_SIZE = 100
    for i in range(0, len(records), CHUNK_SIZE):
        chunk = records[i:i+CHUNK_SIZE]
        actions = [
            {
                "_op_type": "index",
                "_index": index_name,
                "_source": record
            }
            for record in chunk
        ]
        
        # Insert data chunk by chunk
        try:
            helpers.bulk(es, actions)
            print(f"Inserted {len(chunk)} records.")
        except helpers.BulkIndexError as e:
            for error in e.errors:
                # Print the error message for each failed document
                print(error['index']['error'])
                
    es.indices.refresh(index=index_name)
    
    print(f"Data insertion completed for Elasticsearch index: {index_name}")

def main():
    scraped_data = load_data('output.json')
    merged_data = merge_data(scraped_data, 'data/sample-websites-company-names.csv')
    store_to_elasticsearch(merged_data, ES_INDEX)

if __name__ == "__main__":
    main()
