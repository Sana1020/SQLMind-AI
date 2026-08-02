import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
from peft import PeftModel

BASE_MODEL = "Qwen/Qwen2.5-3B-Instruct"
ADAPTER_MODEL = "Sana2030/sqlmind-lora"

_model = None
_tokenizer = None


def load_model():
    global _model, _tokenizer

    if _model is None:
        print("Loading tokenizer...")

        _tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL)

        print("Loading base model...")

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
        )

        print("Loading adapter...")

        _model = PeftModel.from_pretrained(
            base_model,
            ADAPTER_MODEL,
        )

        _model.eval()

        print("Model loaded successfully!")

    return _model, _tokenizer


def generate_sql(question):
    model, tokenizer = load_model()

    prompt = f"""### Instruction:
Generate a SQL query for the following question.

### Question:
{question}

### Response:
"""

    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)

    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=128,
            temperature=0.1,
            do_sample=False,
            pad_token_id=tokenizer.eos_token_id,
        )

    generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    sql = generated_text.split("### Response:")[-1].strip()

    return sql