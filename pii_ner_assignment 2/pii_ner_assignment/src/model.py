from transformers import AutoModelForTokenClassification, AutoConfig
from labels import LABEL2ID, ID2LABEL

def create_model(model_name: str):
    config = AutoConfig.from_pretrained(
        model_name,
        num_labels=len(LABEL2ID),
        id2label=ID2LABEL,
        label2id=LABEL2ID,
        dropout=0.3,
        attention_dropout=0.3,
    )
    model = AutoModelForTokenClassification.from_pretrained(
        model_name,
        config=config
    )
    return model
