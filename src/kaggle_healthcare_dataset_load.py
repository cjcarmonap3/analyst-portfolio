# =============================================================
# Import packages
# =============================================================
from pathlib import Path
import os
import shutil
import logging
import chardet
import kagglehub
import pandas as pd

# =============================================================
# Logging configuration
# =============================================================
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

logger = logging.getLogger(__name__)

# =============================================================
# Define paths
# =============================================================
try:
    base_dir = Path(__file__).resolve().parent.parent
except NameError:
    base_dir = Path(os.getcwd())

raw_data_dir = base_dir / "data" / "raw"
clean_data_dir = base_dir / "data" / "clean"
outputs_dir = base_dir / "outputs"

token_path = base_dir / ".kaggle" / "access_token"

# =============================================================
# Configure Kaggle dataset
# =============================================================
dataset_name = "prasad22/healthcare-dataset"

raw_output_name = "healthcare_dataset_raw.csv"
clean_output_name = "healthcare_dataset_clean.csv"

# =============================================================
# Create required directories
# =============================================================
raw_data_dir.mkdir(parents=True, exist_ok=True)
clean_data_dir.mkdir(parents=True, exist_ok=True)
outputs_dir.mkdir(parents=True, exist_ok=True)

logger.info("Project directory: %s", base_dir)
logger.info("Raw data directory: %s", raw_data_dir)
logger.info("Clean data directory: %s", clean_data_dir)
logger.info("Output directory: %s", outputs_dir)

# =============================================================
# Authenticate with Kaggle API
# =============================================================
def authenticate_kaggle() -> None:
    """
    Authenticate with the Kaggle API using the access token stored in the .kaggle directory.
    Expose it through KAGGLE_API_TOKEN, otherwise raise an error if the access token is not found or is empty.
    """

    if not token_path.exists():
        raise FileNotFoundError(f"Kaggle access token not found at {token_path}.")

    kaggle_token = token_path.read_text(encoding="utf-8").strip()

    if not kaggle_token:
        raise ValueError(f"Kaggle access token is empty{token_path}")

    os.environ["KAGGLE_API_TOKEN"] = kaggle_token

    logger.info("Kaggle API token loaded successfully.")

# =============================================================
# Download raw dataset
# =============================================================
def download_dataset() -> Path:
    """
    Download the Kaggle dataset and return the local download path.
    """

    logger.info(
        "Downloading Kaggle dataset: %s", dataset_name
    )

    dataset_path = kagglehub.dataset_download(dataset_name)

    dataset_path = Path(dataset_path)

    if not dataset_path.exists():
        raise FileNotFoundError(f"Dataset download failed. Path not found: {dataset_path}")

    logger.info(
        "Kaggle dataset downloaded to: %s", dataset_path
    )

    return dataset_path

# =============================================================
# Identify CSV file in downloaded dataset
# =============================================================
def find_csv_file(dataset_path: Path) -> Path:
    """
    Locate the CSV files in the downloaded Kaggle dataset.
    Fails if:
        - No CSV files are found
        - More than one CSV file is found
    """

    csv_files = sorted(
        file
        for file in dataset_path.rglob("*")
        if file.is_file() and file.suffix.lower() == ".csv"
    )

    logger.info(
        "Found %d CSV file(s) in Kaggle dataset.",
        len(csv_files)
    )

    for csv_file in csv_files:
        logger.info(
            "  CSV found: %s",
            csv_file
        )

    if len(csv_files) == 0:
        raise FileNotFoundError(
            f"No CSV files were found in Kaggle dataset: "
            f"{dataset_path}"
        )

    if len(csv_files) > 1:
        raise RuntimeError(
            "Multiple CSV files were found in the Kaggle dataset. "
            "Automatic selection is disabled to prevent loading "
            "the wrong file.\n"
            + "\n".join(
                f"  - {file}"
                for file in csv_files
            )
        )

    return csv_files[0]

# =============================================================
# Copy raw CSV into project
# =============================================================
def save_raw_file(source_file: Path) -> Path:
    """
    Copy the Kaggle CSV into data/raw using a standardized name.
    """

    destination_file = raw_data_dir / raw_output_name

    shutil.copy2(
        source_file,
        destination_file
    )

    logger.info(
        "Raw dataset saved to: %s",
        destination_file
    )

    return destination_file

# =============================================================
# Detect file encoding
# =============================================================
def detect_encoding(file_path: Path) -> str:
    """
    Detect the encoding of a CSV file using a sample of the file.
    """

    with open(file_path, "rb") as file:
        sample = file.read(100_000)

    encoding_info = chardet.detect(sample)

    encoding = encoding_info.get("encoding")
    confidence = encoding_info.get("confidence")

    if not encoding:
        raise ValueError(
            f"Unable to determine encoding for: {file_path}"
        )

    logger.info(
        "Detected encoding: %s (confidence: %.2f)",
        encoding,
        confidence or 0
    )

    return encoding

# =============================================================
# Load raw dataset into pandas DataFrame
# =============================================================
def load_dataset(
    file_path: Path,
    encoding: str
) -> pd.DataFrame:
    """
    Load the raw CSV into a pandas DataFrame.
    """

    logger.info(
        "Loading raw dataset: %s",
        file_path
    )

    df = pd.read_csv(
        file_path,
        encoding=encoding
    )

    logger.info(
        "Dataset loaded successfully: %s rows x %s columns",
        f"{len(df):,}",
        f"{len(df.columns):,}"
    )

    return df

# =============================================================
# Save cleaned/processed dataset
# =============================================================
def save_clean_dataset(df: pd.DataFrame) -> Path:
    """
    Save the DataFrame as the processed output.
    """

    clean_file = clean_data_dir / clean_output_name

    df.to_csv(
        clean_file,
        index=False
    )

    logger.info(
        "Processed dataset saved to: %s",
        clean_file
    )

    return clean_file

# =============================================================
# Main pipeline
# =============================================================
def main() -> None:

    logger.info("Starting Kaggle data pipeline.")

    # 1. Authenticate
    authenticate_kaggle()

    # 2. Download dataset
    dataset_path = download_dataset()

    # 3. Automatically find CSV
    source_csv = find_csv_file(dataset_path)

    # 4. Save raw CSV to project
    raw_csv = save_raw_file(source_csv)

    # 5. Detect encoding
    encoding = detect_encoding(raw_csv)

    # 6. Load into pandas
    df = load_dataset(
        raw_csv,
        encoding
    )

    # 7. Save processed dataset
    output_file = save_clean_dataset(df)

    logger.info("Pipeline completed successfully.")
    logger.info("Raw file: %s", raw_csv)
    logger.info("Output file: %s", output_file)


# =============================================================
# Run pipeline
# =============================================================

if __name__ == "__main__":
    main()

