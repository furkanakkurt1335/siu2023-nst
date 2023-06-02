# BERT for text classification

import torch
import torch.nn as nn
from transformers import AutoModel

class BertForSequenceClassification(nn.Module):
    """BERT model for classification tasks.
    This module is composed of the BERT model with a linear layer on top of
    the pooled output.
    """

    def __init__(self, config, num_labels):
        super().__init__()
        self.num_labels = num_labels
        self.bert = AutoModel.from_pretrained('bert-base-turkish-uncased', config=config)
        self.dropout = nn.Dropout(config.hidden_dropout_prob)
        self.classifier = nn.Linear(config.hidden_size * 2, num_labels)
        self.relu = nn.ReLU()

    def forward(self, input_ids, token_type_ids=None, attention_mask=None, labels=None, position_ids=None, head_mask=None):
        _, pooled_output = self.bert(input_ids, token_type_ids, attention_mask, position_ids, head_mask)
        pooled_output = self.dropout(pooled_output)
        logits = self.classifier(pooled_output)
        return logits
