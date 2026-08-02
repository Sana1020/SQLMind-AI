MODEL_NAME = "Qwen/Qwen2.5-3B-Instruct"

DATASET_PATH = "data/processed/tokenized_spider"

OUTPUT_DIR = "outputs/sqlmind-lora"

MAX_LENGTH = 512

BATCH_SIZE = 2

LEARNING_RATE = 2e-4

EPOCHS = 3

LORA_R = 16
LORA_ALPHA = 32
LORA_DROPOUT = 0.05