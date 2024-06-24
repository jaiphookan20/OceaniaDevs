from openai import OpenAI

client = OpenAI(api_key="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")

def get_embedding(text, model="text-embedding-3-small"):
    response = client.embeddings.create(
        model=model,
        input=text.replace("\n", " ")
    )
    embedding = response.data[0].embedding
    return embedding