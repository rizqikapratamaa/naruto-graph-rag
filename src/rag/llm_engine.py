from transformers import AutoModelForCausalLM, AutoTokenizer, TextStreamer, TextIteratorStreamer
import torch
import os

os.environ["TOKENIZERS_PARALLELISM"] = "false"

# Deteksi Device
if torch.backends.mps.is_available(): device = "mps"
elif torch.cuda.is_available(): device = "cuda"
else: device = "cpu"

QWEN_MODEL_NAME = "Qwen/Qwen2.5-1.5B-Instruct"
print(f"Loading LLM on {device}...")

tokenizer = AutoTokenizer.from_pretrained(QWEN_MODEL_NAME)
if tokenizer.pad_token is None: tokenizer.pad_token = tokenizer.eos_token

model = AutoModelForCausalLM.from_pretrained(
    QWEN_MODEL_NAME, torch_dtype=torch.float16, device_map=None
).to(device)

def get_tokenizer():
    return tokenizer

def generate_answer(context: str, question: str, streamer=None):
    """
    kalo dipanggil dari terminal, pake TextStreamer, kalo dari streamlit, pake TextIteratorStreamer
    """
    system_prompt = "Kamu asisten Naruto. Jawab hanya berdasarkan Konteks. Jika tidak ada di konteks, bilang tidak tahu."
    user_prompt = f"Konteks:\n{context}\n\nPertanyaan:\n{question}"
    
    messages = [{"role": "system", "content": system_prompt}, {"role": "user", "content": user_prompt}]
    text = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    
    inputs = tokenizer([text], return_tensors="pt").to(device)
    
    if streamer is None:
        streamer = TextStreamer(tokenizer, skip_prompt=True)
        print("\nBot: ", end="", flush=True)

    model.generate(
        **inputs, 
        max_new_tokens=256, 
        temperature=0.7, 
        repetition_penalty=1.1, 
        streamer=streamer, 
        pad_token_id=tokenizer.eos_token_id
    )
    
    if streamer is None:
        print("\n")