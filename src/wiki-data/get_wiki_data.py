from datasets import load_dataset

data = load_dataset(
    "wikipedia", language="en", date="20220120", beam_runner="DirectRunner"
)


data.save_to_disk("wikipedia")
