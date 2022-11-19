import os
import pandas as pd
import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer

def predict(df):
    package = 'neuralmind/bert-large-portuguese-cased'
    tokenizer = AutoTokenizer.from_pretrained(package)
    model = AutoModelForSequenceClassification.from_pretrained(package)

    with open('comments_with_sentiment.txt', 'w', encoding = 'utf-8') as f:
        f.write("Frase; Negativo; Positivo; \n")

        for frase in df['Frases']:
            pt_batch = tokenizer(
                frase,
                padding=True,
                truncation=True,
                max_length=512,
                return_tensors="pt",
            )

            outputs = model(**pt_batch)
            scores = torch.nn.functional.softmax(outputs[0], dim=1)
            scores = scores.detach().numpy().tolist()[0]
            f.write(frase + "; " + str(scores[0]) + str(scores[1]) + "\n" )


def get_file(DIR, file_name):
    for file_name in os.listdir(DIR):
        file_path = os.path.join(DIR, file_name)
        if(os.path.isfile(file_path)):
            df = pd.read_csv(file_name, sep = '\n', enconding="UTF-8")
            predict(df)