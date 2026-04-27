# =============================================================
# Import packages
# =============================================================
import os
from dotenv import load_dotenv
import kagglehub
from kagglehub import KaggleDatasetAdapter
import chardet
import inspect
from pathlib import Path

# =============================================================
# Load environment variables
#   - define base directory
#   - define path where .env file lives
# =============================================================
current_file = Path(__file__).resolve()

print("Script path:", current_file)
print("Directory:", current_file.parent)


print("__file__:", __file__)
print("resolved:", Path(__file__).resolve())


try:
    base_dir = Path(__file__).resolve().parents[2]
except NameError:
    base_dir = Path(os.getcwd())

env_path = os.path.join(base_dir, '.env')

#load_dotenv(env_path)
print(base_dir)
print(base_dir.parent)
print(env_path)


# =============================================================
# Set Kaggle credentials
# =============================================================
os.environ['KAGGLE_API_TOKEN'] = os.getenv('KAGGLE_API_TOKEN')

# =============================================================
# Configure Kaggle dataset
# =============================================================
dataset_name = "prasad22/healthcare-dataset"
file_path = "healthcare_dataset_raw.csv"

# =============================================================
# Download raw dataset locally
# =============================================================
local_path = kagglehub.dataset_download(dataset_name)
full_file_path = os.path.join(local_path, file_path)
if not os.path.exists(full_file_path):
    raise FileNotFoundError(f"{file_path} not found in dataset")

# =============================================================
# Detect file encoding
# =============================================================
with open(full_file_path, 'rb') as f:
    sample = f.read(10000)
    encoding_info = chardet.detect(sample)

encoding = encoding_info['encoding']
print(f"Detected encoding: {encoding}")

# =============================================================
# Load latest version of Kaggle raw dataset
# =============================================================
df = kagglehub.dataset_load(
  KaggleDatasetAdapter.PANDAS,
  dataset_name,
  file_path,
  pandas_kwargs={"encoding": encoding}
)

output_path = os.path.join(base_dir, "healthcare_dataset_clean.csv")
df.to_csv(output_path, index=False)
print(f"File saved to: {output_path}")

# =============================================================
# Preview raw data
# =============================================================
print("First 5 records:")
print(df.head())

print("\nDataset info:")
print(df.info())
