import tiktoken
enc=tiktoken.encoding_for_model("gpt-4o")
text = "Hello, I am Anirban!"

encoded_tokens = enc.encode(text)

print("Encoded Tokens: ", encoded_tokens)

decoded_tokens = enc.decode(encoded_tokens)

print("="*30)
print(decoded_tokens)

