from src import get_data, clean_data, add_features


RAW_DATA_PATH = "data/raw/data.xlsx"
DATA_PATH = "data/processed/data.csv"
CLEANED_DATA_PATH = "data/processed/data_cleaned.csv"
FEATURED_DATA_PATH = "data/processed/data_featured.csv"

def run():
    get_data(RAW_DATA_PATH, DATA_PATH)
    clean_data(DATA_PATH, CLEANED_DATA_PATH)
    add_features(CLEANED_DATA_PATH, FEATURED_DATA_PATH)


if __name__ == "__main__":
    get_data(RAW_DATA_PATH, DATA_PATH)
    clean_data(DATA_PATH, CLEANED_DATA_PATH)
    add_features(CLEANED_DATA_PATH, FEATURED_DATA_PATH)
