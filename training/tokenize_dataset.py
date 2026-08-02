from datasets import load_dataset
from transformers import AutoTokenizer

# Load Spider Dataset
dataset = load_dataset("xlangai/spider")

# Load Qwen Tokenizer
tokenizer = AutoTokenizer.from_pretrained(
    "Qwen/Qwen2.5-3B-Instruct"
)


def format_prompt(example):
    prompt = f"""### Instruction:
Generate a SQL query for the following question.

### Question:
{example["question"]}

### Response:
{example["query"]}"""

    return {"text": prompt}


# Convert to prompt format
dataset = dataset.map(format_prompt)


def tokenize(example):
    return tokenizer(
        example["text"],
        truncation=True,
        max_length=512
    )


# Tokenize the dataset
tokenized_dataset = dataset.map(tokenize)

# Print one example
print(tokenized_dataset["train"][0])
# Save tokenized dataset
import os

os.makedirs("data/processed/tokenized_spider", exist_ok=True)
tokenized_dataset.save_to_disk("data/processed/tokenized_spider")

print("Dataset saved successfully!")