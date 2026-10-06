def piga_gpt4o(client, pro_prompt):
    """Inapiga radi kuelekea OpenAI seva kiusalama"""
    jibu = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": pro_prompt}]
    )
    return jibu.choices.message.content
