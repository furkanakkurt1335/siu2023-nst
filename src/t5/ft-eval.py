from datasets import load_from_disk
from transformers import T5Tokenizer, T5ForConditionalGeneration, TrainingArguments, Trainer
import torch, evaluate, os, json, sys, argparse
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))
from smtp_gmail import send_email

parser = argparse.ArgumentParser()
parser.add_argument('--feature', type=str, required=True)
args = parser.parse_args()

THIS_DIR = os.path.dirname(os.path.realpath(__file__))

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print('Device:', device)

feature = args.feature
dataset_path = os.path.join(THIS_DIR, 'datasets', feature)
dataset_name = 'nst-{}'.format(feature)
if os.path.exists(dataset_path):
    dataset = load_from_disk(dataset_path)
    print('Dataset is loaded.')
    print('Dataset:', dataset)
else:
    print('Dataset is not found.')
    exit()

model_name = 'Turkish-NLP/t5-efficient-large-turkish'
print('Model:', model_name)
print('Loading tokenizer...')
tokenizer = T5Tokenizer.from_pretrained(model_name)
print('Tokenizer is loaded.')

prefix = 'Bu metin nefret söylemi içeriyor mu?'
max_length = 64

def tokenize_function(examples):
    inputs = [prefix + inp for inp in examples['text']]
    model_inputs = tokenizer(inputs, text_target=examples[feature], max_length=max_length, truncation=True, padding='max_length')
    return model_inputs

tokenized_datasets = dataset.map(tokenize_function, batched=True)

print('Loading model...')
model = T5ForConditionalGeneration.from_pretrained(model_name)
print('Model is loaded.')
model.to(device)

batch_size = 16
output_dir = os.path.join(THIS_DIR, 'model-{}'.format(feature))
training_args = TrainingArguments(
    output_dir=output_dir,
    per_device_train_batch_size=batch_size,
    per_device_eval_batch_size=batch_size,
    evaluation_strategy='epoch',
    save_strategy='no',
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_datasets['train'],
    eval_dataset=tokenized_datasets['validation'],
)

print('Training is starting.')
trainer.train()
print('Training is finished.')

print('Saving model.')
trainer.save_model(output_dir)
print('Model is saved.')

print('Predictions are starting.')
pred_l = []
for el in dataset['test']:
    text = prefix + el['text']
    tokenized_text = tokenizer.encode(text, return_tensors='pt', truncation=True, max_length=max_length).to(device)
    summary_ids = model.generate(tokenized_text, top_k=50, top_p=0.95, max_length=max_length, early_stopping=True)
    output = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    print('Input:', text)
    print('Output:', output)
    pred_l.append(output)
print('Predictions are finished.')

print('Saving predictions.')
pred_path = os.path.join(THIS_DIR, 'predictions.json')
if os.path.exists(pred_path):
    with open(pred_path, 'r') as f:
        old_predictions = json.load(f)
    old_predictions.append({'model': model_name, 'dataset': dataset_name, 'predictions': pred_l})
    with open(pred_path, 'w') as f:
        json.dump(old_predictions, f, indent=4, ensure_ascii=False)
else:
    with open(pred_path, 'w') as f:
        json.dump([{'model': model_name, 'dataset': dataset_name, 'predictions': pred_l}], f, indent=4, ensure_ascii=False)
print('Predictions are saved.')

print('Evaluation is starting.')
accuracy = evaluate.accuracy(pred_l, dataset['test'][feature])
print('Evaluation is finished.')

print('Model:', model_name)
print('Dataset:', dataset_name)
print('Accuracy:', accuracy)

send_email(model_name, dataset_name, accuracy, 'furkanakkurt9285@gmail.com')
print('Email is sent.')