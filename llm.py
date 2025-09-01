import os
from langchain_huggingface import HuggingFaceEndpoint
from huggingface_hub import InferenceClient

DEFAULT_REPO_ID = "microsoft/DialoGPT-medium"  # Changed to a more stable model

def get_hf_llm(hf_token: str = None, temperature: float = 0.2, max_new_tokens: int = 600):
    token = hf_token or os.getenv("HF_API_KEY", "")
    
    # Try multiple models in order of preference
    models_to_try = [
        "microsoft/DialoGPT-medium",
        "gpt2",
        "google/flan-t5-base",
        "facebook/opt-350m"
    ]
    
    for model in models_to_try:
        try:
            return HuggingFaceEndpoint(
                repo_id=model,
                task="text-generation",
                huggingfacehub_api_token=token,
                temperature=temperature,
                max_new_tokens=max_new_tokens,
                repetition_penalty=1.05,
                do_sample=True,
                timeout=300,  # Increased timeout
            )
        except Exception as e:
            print(f"Failed to load {model}: {e}")
            continue
    
    # Fallback: return a mock response if all models fail
    raise Exception("All Hugging Face models failed to load. Please check your API token and internet connection.")

# Alternative function for direct inference without LangChain wrapper
def get_hf_inference_client(hf_token: str = None):
    token = hf_token or os.getenv("HF_API_KEY", "")
    return InferenceClient(token=token)

def safe_text_generation(prompt: str, hf_token: str = None, model: str = "microsoft/DialoGPT-medium"):
    """
    Safe text generation that handles StopIteration errors
    """
    try:
        client = get_hf_inference_client(hf_token)
        response = client.text_generation(
            prompt=prompt,
            model=model,
            max_new_tokens=150,
            temperature=0.7,
            do_sample=True,
            return_full_text=False
        )
        return str(response) if response else "No response generated."
    except Exception as e:
        return f"Error generating text: {str(e)}"
