# from transformers import AutoTokenizer, AutoModelForCasualLM
#
# model = AutoModelForCasualLM.from_pretrained("RWKV/v5-Eagle-7B-HF", trust_remote_code=True).to(torch.float32)
# tokenizer = AutoTokenizer.from_pretrained("RWKV/v5-Eagle-7B-HF", trust_remote_code=True)
#
# indices = [103, 109, 98, 104, 124, 99, 99, 50, 54, 53, 99, 101, 103, 49, 49, 51, 98, 55, 51, 49, 101, 99, 55, 54, 56, 99, 57, 101, 103, 57, 53, 98, 57, 56, 49, 55, 53, 126]
# tokens = [tokenizer.decode([idx]) for idx in indices]
# print(tokens)

print("".join(['f', 'l', 'a', 'g', '{', 'b', 'b', '1', '5', '4', 'b', 'd', 'f', '0', '0', '2', 'a', '6', '2', '0', 'd', 'b', '6', '5', '7', 'b', '8', 'd', 'f', '8', '4', 'a', '8', '7', '0', '6', '4', '}']))