from transformers import AutoTokenizer
from transformers import DataCollatorWithPadding
import evaluate, torch, os, json
from transformers import AutoModelForSequenceClassification, TrainingArguments, Trainer
from transformers import pipeline
from datasets import Dataset
import numpy as np

model_name = 'dbmdz/bert-base-turkish-uncased'
tokenizer = AutoTokenizer.from_pretrained(model_name)

def preprocess_function(examples):
    return tokenizer(examples["text"], truncation=True)

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(THIS_DIR, '../../data')
filename = 'data.json'
filepath = os.path.join(data_path, filename)
with open(filepath, encoding='utf-8') as f:
    data = json.load(f)
new_data = []
for el in data:
    if 'existence' in el.keys():
        new_data.append(el)
test_filename = 'test-data.json'
test_filepath = os.path.join(data_path, test_filename)
with open(test_filepath, encoding='utf-8') as f:
    test_data = json.load(f)
new_test_data = []
for el in test_data:
    if el['subtask'] == '2':
        new_test_data.append(el)
dataset = Dataset.from_list(data)
test_dataset = Dataset.from_list(test_data)

tokenized_dataset = dataset.map(preprocess_function, batched=True)
tokenized_test_dataset = test_dataset.map(preprocess_function, batched=True)

data_collator = DataCollatorWithPadding(tokenizer=tokenizer)

accuracy = evaluate.load("accuracy")

def compute_metrics(eval_pred):
    predictions, labels = eval_pred
    predictions = np.argmax(predictions, axis=1)
    return accuracy.compute(predictions=predictions, references=labels)

id2label = {'0': "değil", '1': "nefret"}
label2id = {"değil": '0', "nefret": '1'}

model = AutoModelForSequenceClassification.from_pretrained(
    model_name, num_labels=2, id2label=id2label, label2id=label2id
)

training_args = TrainingArguments(
    output_dir="my_awesome_model",
    learning_rate=2e-5,
    per_device_train_batch_size=16,
    per_device_eval_batch_size=16,
    num_train_epochs=2,
    weight_decay=0.01,
    evaluation_strategy="epoch",
    save_strategy="epoch",
    load_best_model_at_end=True,
    push_to_hub=True,
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_dataset,
    eval_dataset=tokenized_test_dataset,
    tokenizer=tokenizer,
    data_collator=data_collator,
    compute_metrics=compute_metrics,
)

trainer.train()

# trainer.evaluate()

test_texts = []
tokenizer = AutoTokenizer.from_pretrained(model_name)
for text in test_texts:
    inputs = tokenizer(text, return_tensors="pt")
    with torch.no_grad():
        logits = model(**inputs).logits
    predicted_class_id = logits.argmax().item()
    label = model.config.id2label[predicted_class_id]
    print(f"{text}\t{label}")
# classifier = pipeline("sentiment-analysis", model="stevhliu/my_awesome_model")
# classifier(text)