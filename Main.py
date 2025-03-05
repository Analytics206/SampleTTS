from datasets import load_dataset, DatasetDict
from transformers import AutoTokenizer
from pyexpat import features
checkpoint = "bert-base-uncased"
tokenizer = AutoTokenizer.from_pretrained(checkpoint)
tokenizer(["My name is bob."],["Bob works at the deli"],
          padding=True)

raw_datasets = load_dataset("glue","mrpc")

# DatasetDict({
#     train: Dataset({
#         features: ['sentence1','sentence2','label','idx'],
#         num_rows: 3668
#     })
#     validation: Dataset({
#         features: ['sentence1','sentence2','label','idx'],
#         num_rows: 408
#     })
#     test: Dataset({
#         features: ['sentence1', 'sentence2', 'label', 'idx'],
#         num_rows: 1725
#     })
# })