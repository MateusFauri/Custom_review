import os
import pandas as pd
import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer

def predict(df):
    package = 'neuralmind/bert-large-portuguese-cased'
    tokenizer = AutoTokenizer.from_pretrained(package)
    model = AutoModelForSequenceClassification.from_pretrained(package)

    print("Starting the process...")

    with open('comments_with_sentiment.txt', 'w', encoding = 'utf-8') as f:
        f.write("Phrase; negative; positive; \n")

        for phrase in df['Phrase']:

            pt_batch = tokenizer(
                phrase,
                padding=True,
                truncation=True,
                max_length=512,
                return_tensors="pt"
            )

            outputs = model(**pt_batch)

            scores = torch.nn.functional.softmax(outputs[0], dim=1)
            scores = scores.detach().numpy().tolist()[0]

            f.write(f'{phrase}; {scores[0]:,.3f}; {scores[1]:.2f}\n')

    print("End of process!")

def get_file(DIR, file_name):
    have_file = False

    for file in os.listdir(DIR):
        if(file == file_name):
            have_file = True

            file_path = os.path.join(DIR, file_name)

            if(os.path.isfile(file_path)):
                df = pd.read_csv(file_name, sep='\r\n',on_bad_lines='skip')

                predict(df)
    if not have_file:
        print("You don't have that file!")

