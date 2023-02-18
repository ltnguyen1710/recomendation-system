import pandas as pd
import numpy as np
import torch
from transformers import AutoTokenizer, AutoModel

tokenizer = AutoTokenizer.from_pretrained(
    'sentence-transformers/bert-large-nli-stsb-mean-tokens')
model = AutoModel.from_pretrained(
    'sentence-transformers/bert-large-nli-stsb-mean-tokens')


class BERT(object):
    def __init__(self):
        pass

    def mean_pooling(self, model_output, attention_mask):
        # First element of model_output contains all token embeddings
        token_embeddings = model_output[0]
        input_mask_expanded = attention_mask.unsqueeze(
            -1).expand(token_embeddings.size()).float()
        return torch.sum(token_embeddings * input_mask_expanded, 1) / torch.clamp(input_mask_expanded.sum(1), min=1e-9)

    def fit_model_SBert(self, senquence):
        # Tokenize sentences
        encoded_input = tokenizer(
            senquence, padding=True, truncation=True, return_tensors='pt')

        # Compute token embeddings
        with torch.no_grad():
            model_output = model(**encoded_input)

        # Perform pooling. In this case, max pooling.
        sentence_embeddings = self.mean_pooling(
            model_output, encoded_input['attention_mask'])
        return sentence_embeddings

    def train(self, sentences):
        bert_results = []
        for idx in range(len(sentences)):
            vector_bert = self.fit_model_SBert(sentences[idx]).tolist()
            bert_results.append(vector_bert)
        bert_results = np.array(bert_results)
        bert_results = np.array(bert_results[:, 0, :])
        return bert_results.T
