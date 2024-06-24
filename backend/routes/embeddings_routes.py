import openai

openai.api_key = "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"

def get_embedding(text):
    response = openai.Embedding.create(
        model="text-embedding-ada-002",
        input=text
    )
    embedding = response['data'][0]['embedding']
    return embedding
