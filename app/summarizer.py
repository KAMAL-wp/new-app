from groq import Groq

client = Groq(api_key="")  # Your actual API key

def list_available_models():
    """Helper function to see all available models"""
    try:
        models = client.models.list()
        print("\n" + "="*50)
        print("ACTUALLY AVAILABLE MODELS:")
        print("="*50)
        for model in models.data:
            print(f"✅ {model.id}")
        print("="*50 + "\n")
        return [model.id for model in models.data]
    except Exception as e:
        print(f"Error fetching models: {e}")
        return []

# Call this first to see what's available
available_models = list_available_models()

def summarize(text, filename):
    trimmed = text[:4000]
    if not trimmed.strip():
        return "No text content found in this document."
    
    # Try different models based on what's actually available
    try:
        # Let's try common model names that might work
        models_to_try = [
            "llama-3.3-70b-versatile"  # Common Llama 3.3 model ID
            # "llama3-70b-8192",           # Older Llama 3 70B
            # "mixtral-8x7b-32768",        # Mixtral
            # "gemma2-9b-it",              # Gemma 2
            # "llama-3.1-8b-instant",      # Llama 3.1 8B
        ]
        
        # If we got models from the list, use those instead
        if available_models:
            models_to_try = available_models
        
        last_error = None
        for model_name in models_to_try:
            try:
                print(f"Trying model: {model_name}")
                response = client.chat.completions.create(
                    model=model_name,
                    messages=[
                        {"role": "system", "content": "You are a document summarizer. Summarize in 5-10 sentences."},
                        {"role": "user", "content": f"Summarize this document:\n\n{trimmed}"}
                    ],
                    temperature=0.7,
                    max_tokens=300
                )
                print(f"✅ Success with model: {model_name}")
                return response.choices[0].message.content
            except Exception as e:
                last_error = e
                print(f"❌ Failed with {model_name}: {e}")
                continue
        
        return f"Error: No working model found. Last error: {last_error}"
    
    except Exception as e:
        return f"Error in summarization: {e}"