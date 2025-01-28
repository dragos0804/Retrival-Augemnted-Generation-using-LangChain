from transformers import AutoModelForCausalLM
from PIL import Image

def interpret_chart(image_path):
    model = AutoModelForCausalLM.from_pretrained("damerajee/GPTVision-1-ft", trust_remote_code=True)
    image = Image.open(image_path)
    image = image.convert('RGB')
    gen_kwargs = {
        "do_sample": True,
        "temperature": 0.8,
        "top_p": 0.6,
        "repetition_penalty": 1.6,

        }

    question = "What does the plot/chart/graph say?"
    answer = model.generate(image=image,question=question,max_new_tokens=80,**gen_kwargs)
    return answer

