from openai import OpenAI
# from navtest import rtr_rs

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key="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",
)
def main(prompt):

    # API request
    completion = client.chat.completions.create(
        extra_headers={
            "HTTP-Referer": "<YOUR_SITE_URL>",
            "X-Title": "<YOUR_SITE_NAME>",
        },
        extra_body={},
        model="deepseek/deepseek-r1:free",
        messages=[{"role": "user", "content": prompt}],
    )

    # Print response
    airecommeded_movieseries_str = "".join(completion.choices[0].message.content)
    return airecommeded_movieseries_str

print(main("Recommend 5 series related to loki"))
