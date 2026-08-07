import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
from peft import PeftModel, PeftConfig
import sqlite3

BASE_MODEL = "Qwen/Qwen2.5-3B-Instruct"
ADAPTER_MODEL = "Sana2030/sqlmind-lora"

_model = None
_tokenizer = None


def load_model():
    global _model, _tokenizer

    if _model is not None:
        return _model, _tokenizer

    print("=" * 50)
    print("CUDA Available:", torch.cuda.is_available())

    if torch.cuda.is_available():
        print("GPU:", torch.cuda.get_device_name(0))
    else:
        print("Running on CPU")

    print("=" * 50)

    print("Loading tokenizer...")
    _tokenizer = AutoTokenizer.from_pretrained(
        BASE_MODEL,
        trust_remote_code=True
    )
    print("Tokenizer loaded.")

    if torch.cuda.is_available():

        print("Loading model on GPU...")

        bnb_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_compute_dtype=torch.float16,
            bnb_4bit_use_double_quant=True,
        )

        base_model = AutoModelForCausalLM.from_pretrained(
            BASE_MODEL,
            quantization_config=bnb_config,
            device_map="auto",
            trust_remote_code=True,
        )

    else:

        print("Loading model on CPU...")

        base_model = AutoModelForCausalLM.from_pretrained(
            BASE_MODEL,
            dtype=torch.float32,  
            low_cpu_mem_usage=True,
            trust_remote_code=True,
        )

    print("Base model loaded.")

    print("Loading adapter config...")
    config = PeftConfig.from_pretrained(ADAPTER_MODEL)
    print("Adapter config loaded.")

    print("Adapter trained on:", config.base_model_name_or_path)

    print("Loading LoRA adapter...")

    try:
        _model = PeftModel.from_pretrained(
            base_model,
            ADAPTER_MODEL,
        )
        print("Adapter loaded.")

    except Exception as e:
        print("ERROR while loading adapter:")
        print(e)
        raise

    _model.eval()

    print("Model loaded successfully!")

    return _model, _tokenizer
def get_database_schema():

    conn = sqlite3.connect("database/northwind2000.sqlite")

    cursor = conn.cursor()

    cursor.execute("""
        SELECT name
        FROM sqlite_master
        WHERE type='table'
        AND name NOT LIKE 'sqlite_%'
    """)

    tables = cursor.fetchall()

    schema = ""

    for table in tables:

        table_name = table[0]

        cursor.execute(f"PRAGMA table_info('{table_name}')")

        columns = cursor.fetchall()

        column_names = ", ".join(col[1] for col in columns)

        schema += f"{table_name}({column_names})\n"

    conn.close()

    return schema

def generate_sql(question):

    model, tokenizer = load_model()

    schema = get_database_schema()

    prompt = f"""
You are an expert SQLite developer.

Database Schema:
{schema}

Important Rules:

1. Use ONLY the table names above.
2. Use ONLY the column names above.
3. NEVER invent a table or column.
4. If the table is Products, use ProductName instead of product.
5. Return ONLY SQL.

Question:
{question}

### Response:
"""

    print("=" * 50)
    print(prompt)
    print("=" * 50)

    inputs = tokenizer(
        prompt,
        return_tensors="pt"
    )

    inputs = {
        k: v.to(model.device)
        for k, v in inputs.items()
    }

    with torch.no_grad():

        outputs = model.generate(
            **inputs,
            max_new_tokens=128,
            temperature=0.1,
            do_sample=False,
            pad_token_id=tokenizer.eos_token_id,
        )

    generated_text = tokenizer.decode(
        outputs[0],
        skip_special_tokens=True
    )

    sql = generated_text.split("### Response:")[-1].strip()

    # ==========================
    # SQL Validation
    # ==========================


    return sql
if __name__ == "__main__":
    print("Testing model loading...")
    load_model()
    print("Done.")
