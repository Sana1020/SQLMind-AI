from datasets import load_dataset

dataset = load_dataset("xlangai/spider")


def format_example(example):
    prompt = f"""### Instruction:
Generate a SQL query for the following question.

### Question:
{example["question"]}

### Response:
{example["query"]}"""

    return {"text": prompt}


formatted_dataset = dataset.map(format_example)

print(formatted_dataset["train"][0]["text"])