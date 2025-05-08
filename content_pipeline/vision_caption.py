import openai, os, base64

def caption_image(image_path: str) -> str:
    openai.api_key = os.getenv("OPENAI_API_KEY")
    if not openai.api_key:
        return "[Error: OPENAI_API_KEY not set]"
    try:
        with open(image_path, "rb") as image_file:
            b64_image = base64.b64encode(image_file.read()).decode("utf-8")
        prompt = "Describe what signal this chart is indicating. Keep it factual and under 40 words."
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[
                {"role": "user", "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{b64_image}"}}
                ]}
            ]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"[Error generating caption: {str(e)}]"
