import os

from ray.train import ScalingConfig
import evaluate
import numpy as np
from transformers import (
    Trainer,
    TrainingArguments,
    AutoTokenizer,
    AutoModelForSequenceClassification,
)
import ray.train.huggingface.transformers
from ray.train import ScalingConfig
from ray.train.torch import TorchTrainer
import json

from datasets import Dataset


fp = "data_test.json"
with open(fp, 'r') as file:
        dataset_tejson = json.load(file)
fp2 = "data_train.json"
with open(fp2, 'r') as file:
        dataset_trjson = json.load(file)

def gen1():
     for item in dataset_tejson:
          yield {"text":item["text"], "label": item["label"]}

def gen2():
     for item in dataset_trjson:
          yield {"text":item["text"], "label": item["label"]}

dataset_test = Dataset.from_generator(gen1)
dataset_train = Dataset.from_generator(gen2)

def train_func():
    tokenizer = AutoTokenizer.from_pretrained("bert-base-cased")

    def tokenize_function(examples):
        return tokenizer(examples["text"], padding="max_length", truncation=True)

    small_train_dataset = (
        dataset_train.select(range(1000)).map(tokenize_function, batched=True)
    )

    small_eval_dataset = (
        dataset_test["test"].select(range(1000)).map(tokenize_function, batched=True)
    )

    # Model
    model = AutoModelForSequenceClassification.from_pretrained(
        "bert-base-cased", num_labels=5
    )

    # Evaluation Metrics
    metric = evaluate.load("accuracy")

    def compute_metrics(eval_pred):
        logits, labels = eval_pred
        predictions = np.argmax(logits, axis=-1)
        return metric.compute(predictions=predictions, references=labels)
    
    # Hugging Face Trainer
    training_args = TrainingArguments(
        output_dir="test_trainer",
        evaluation_strategy="epoch",
        save_strategy="epoch",
        report_to="none",
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=small_train_dataset,
        eval_dataset=small_eval_dataset,
        compute_metrics=compute_metrics,
    )

    # [2] Report Metrics and Checkpoints to Ray Train
    # ===============================================
    callback = ray.train.huggingface.transformers.RayTrainReportCallback()
    trainer.add_callback(callback)

    # [3] Prepare Transformers Trainer
    # ================================
    trainer = ray.train.huggingface.transformers.prepare_trainer(trainer)

    # Start Training
    trainer.train()


# [4] Define a Ray TorchTrainer to launch `train_func` on all workers
# ===================================================================
ray_trainer = TorchTrainer(
    train_func,
    scaling_config=ScalingConfig(num_workers=1, use_gpu=False),
    # [4a] If running in a multi-node cluster, this is where you
    # should configure the run's persistent storage that is accessible
    # across all worker nodes.
    # run_config=ray.train.RunConfig(storage_path="s3://..."),
)
result: ray.train.Result = ray_trainer.fit()

# [5] Load the trained model.
with result.checkpoint.as_directory() as checkpoint_dir:
    checkpoint_path = os.path.join(
        checkpoint_dir,
        ray.train.huggingface.transformers.RayTrainReportCallback.CHECKPOINT_NAME,
    )
    model = AutoModelForSequenceClassification.from_pretrained(checkpoint_path)