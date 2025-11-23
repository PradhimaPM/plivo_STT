import json
import random
import os
from datetime import datetime

# -------------------------
# DATA COMPONENTS
# -------------------------
names = ["ramesh", "sneha", "kavya", "rahul", "anju", "vikram", "arjun", "priya",
         "rohan", "amit", "aravind", "kiran", "deepak", "akash"]

cities = ["chennai", "mumbai", "delhi", "pune", "hyderabad", "bangalore", "kolkata"]

locations = ["near airport", "beside railway station", "close to bus stand",
             "near marina beach", "opposite city mall", "next to metro station"]

digits = ["zero","one","two","three","four","five","six","seven","eight","nine"]

month_words = ["january","february","march","april","may","june",
               "july","august","september","october","november","december"]

fillers = ["uh", "umm", "basically", "like", "actually", "yaar", "okay", "right"]

email_domains = ["gmail", "yahoo", "outlook", "hotmail"]


# -------------------------
# GENERATION FUNCTIONS
# -------------------------

def gen_phone():
    d = random.choices(digits, k=10)
    return " ".join(d)

def gen_credit_card():
    d = random.choices(digits, k=16)
    return " ".join(d)

def gen_date():
    year = random.choice(["twenty twenty", "twenty twenty one", "twenty twenty two", "twenty twenty three"])
    day = random.choice(["first","second","third","fourth","fifth","sixth","seventh","eighth","ninth","tenth",
                         "eleventh","twelfth","thirteenth","fourteenth","fifteenth",
                         "sixteenth","seventeenth","eighteenth","nineteenth","twentieth"])
    month = random.choice(month_words)
    return f"{day} {month} {year}"

def gen_email(name):
    return f"{name} at {random.choice(email_domains)} dot com"

def annotate(text, substring, label):
    start = text.index(substring)
    end = start + len(substring)
    return {"start": start, "end": end, "label": label}


# -------------------------
# EXAMPLE GENERATOR
# -------------------------

def make_example(id_num):
    name = random.choice(names)
    phone = gen_phone()
    card = gen_credit_card()
    email = gen_email(name)
    city = random.choice(cities)
    location = random.choice(locations)
    date_str = gen_date()

    templates = [
        f"my phone number is {phone} and my email is {email}",
        f"call {name} on {phone} he lives in {city}",
        f"send the report to {email} on {date_str}",
        f"the credit card number is {card} please keep it secret",
        f"i stay {location} in {city}",
        f"{name} booked tickets on {date_str} and his phone is {phone}",
        f"email {name} at {email} by tomorrow",
        f"the meeting is on {date_str} at {location} {city}",
    ]

    text = random.choice(templates)

    # Insert noise
    if random.random() < 0.3:
        text = random.choice(fillers) + " " + text
    if random.random() < 0.3:
        text += " " + random.choice(fillers)

    entities = []
    parts = [(phone, "PHONE"), (card, "CREDIT_CARD"), (email, "EMAIL"),
             (name, "PERSON_NAME"), (city, "CITY"),
             (location, "LOCATION"), (date_str, "DATE")]

    for span, label in parts:
        if span in text:
            entities.append(annotate(text, span, label))

    return {"id": f"utt_{id_num:04d}", "text": text, "entities": entities}


#-------------------------
# GENERATE AND SAVE DATASETS
# -------------------------

train_size = 800
dev_size = 150

train = [make_example(i) for i in range(train_size)]
dev = [make_example(i + train_size) for i in range(dev_size)]

output_dir = "/home/prahima/plivo/pii_ner_assignment 2/pii_ner_assignment/data"
os.makedirs(output_dir, exist_ok=True)

with open(f"{output_dir}/train_generated.jsonl", "w") as f:
    for ex in train:
        f.write(json.dumps(ex) + "\n")

with open(f"{output_dir}/dev_generated.jsonl", "w") as f:
    for ex in dev:
        f.write(json.dumps(ex) + "\n")

print("Generated:")
print(f"- {output_dir}/train_generated.jsonl  ({len(train)} examples)")
print(f"- {output_dir}/dev_generated.jsonl    ({len(dev)} examples)")

