from datasets import load_from_disk

from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
    TrainingArguments,
    BitsAndBytesConfig
)

from peft import (
    LoraConfig,
    get_peft_model,
    prepare_model_for_kbit_training
)

from trl import SFTTrainer

from configs.training_config import *

import torch

print("Train.py started")


# =========================
# Load Dataset
# =========================

dataset = load_from_disk(DATASET_PATH)


# =========================
# Load Tokenizer
# =========================

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

tokenizer.pad_token = tokenizer.eos_token


# =========================
# QLoRA Configuration
# =========================

bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,

    bnb_4bit_quant_type="nf4",

    bnb_4bit_compute_dtype=torch.float16,

    bnb_4bit_use_double_quant=True
)


# =========================
# Load Model
# =========================

model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,

    quantization_config=bnb_config,

    device_map="auto"
)


# =========================
# Prepare Model for QLoRA
# =========================

model = prepare_model_for_kbit_training(model)


# Enable Gradient Checkpointing
model.gradient_checkpointing_enable()


# Disable cache for training
model.config.use_cache = False



# =========================
# LoRA Configuration
# =========================

lora_config = LoraConfig(
    r=LORA_R,

    lora_alpha=LORA_ALPHA,

    lora_dropout=LORA_DROPOUT,

    bias="none",

    task_type="CAUSAL_LM",

    target_modules=[
        "q_proj",
        "k_proj",
        "v_proj",
        "o_proj",
        "gate_proj",
        "up_proj",
        "down_proj"
    ]
)



# =========================
# Apply LoRA Adapter
# =========================

model = get_peft_model(
    model,

    lora_config
)



# Print trainable parameters

model.print_trainable_parameters()



# =========================
# Training Arguments
# =========================

training_args = TrainingArguments(

    output_dir=OUTPUT_DIR,

    per_device_train_batch_size=BATCH_SIZE,

    learning_rate=LEARNING_RATE,

    num_train_epochs=EPOCHS,

    logging_steps=10,

    save_strategy="epoch",

    fp16=True,

    report_to="none"
)



# =========================
# Trainer
# =========================

trainer = SFTTrainer(

    model=model,

    train_dataset=dataset["train"],

    eval_dataset=dataset["validation"],

    processing_class=tokenizer,

    args=training_args
)



# =========================
# Train
# =========================

trainer.train()



# =========================
# Save LoRA Adapter
# =========================

model.save_pretrained(OUTPUT_DIR)

tokenizer.save_pretrained(OUTPUT_DIR)


print("Training Finished Successfully!")