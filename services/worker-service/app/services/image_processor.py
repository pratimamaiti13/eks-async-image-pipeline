from PIL import Image
from pathlib import Path


class ImageProcessor:

    @staticmethod
    def resize(input_path: str, output_path: str):
        with Image.open(input_path) as image:
            image = image.convert("RGB")
            image.thumbnail((800, 800))  # preserves aspect ratio, unlike resize()

            Path(output_path).parent.mkdir(parents=True, exist_ok=True)
            image.save(output_path, "JPEG", quality=85)

        return output_path