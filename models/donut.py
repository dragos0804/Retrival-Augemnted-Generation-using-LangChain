from transformers import DonutProcessor, VisionEncoderDecoderModel
from PIL import Image

def interpret_chart(image_path):
    processor = DonutProcessor.from_pretrained("naver-clova-ix/donut-base-finetuned-docvqa")
    model = VisionEncoderDecoderModel.from_pretrained("naver-clova-ix/donut-base-finetuned-docvqa")
    image = Image.open(image_path)
    pixel_values = processor(image, return_tensors="pt").pixel_values
    outputs = model.generate(pixel_values, max_length=512)
    generated_text = processor.batch_decode(outputs, skip_special_tokens=True)[0]
    return generated_text

# generated_text = interpret_chart(image_path)

