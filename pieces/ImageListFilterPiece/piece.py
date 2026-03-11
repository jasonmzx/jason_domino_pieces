from domino.base_piece import BasePiece
from .models import InputModel, OutputModel
from pathlib import Path
from PIL import Image
from io import BytesIO
import numpy as np
import base64
import os


filter_masks = {
    'sepia': ((0.393, 0.769, 0.189), (0.349, 0.686, 0.168), (0.272, 0.534, 0.131)),
    'black_and_white': ((0.333, 0.333, 0.333), (0.333, 0.333, 0.333), (0.333, 0.333, 0.333)),
    'brightness': ((1.4, 0, 0), (0, 1.4, 0), (0, 0, 1.4)),
    'darkness': ((0.6, 0, 0), (0, 0.6, 0), (0, 0, 0.6)),
    'contrast': ((1.2, 0.6, 0.6), (0.6, 1.2, 0.6), (0.6, 0.6, 1.2)),
    'red': ((1.6, 0, 0), (0, 1, 0), (0, 0, 1)),
    'green': ((1, 0, 0), (0, 1.6, 0), (0, 0, 1)),
    'blue': ((1, 0, 0), (0, 1, 0), (0, 0, 1.6)),
    'cool': ((0.9, 0, 0), (0, 1.1, 0), (0, 0, 1.3)),
    'warm': ((1.2, 0, 0), (0, 0.9, 0), (0, 0, 0.8)),
}


class ImageListFilterPiece(BasePiece):

    def piece_function(self, input_data: InputModel):

        all_filters = [
            name for name in filter_masks
            if getattr(input_data, name, False)
        ]

        max_path_size = int(os.pathconf('/', 'PC_PATH_MAX'))

        image_base64_strings = []
        image_file_paths = []

        for idx, input_image in enumerate(input_data.input_images):
            # Load image from file path or base64 string
            if len(input_image) < max_path_size and Path(input_image).exists() and Path(input_image).is_file():
                image = Image.open(input_image)
            else:
                self.logger.info(f"Image {idx}: not a file path, trying base64 decode")
                try:
                    decoded_data = base64.b64decode(input_image)
                    image_stream = BytesIO(decoded_data)
                    image = Image.open(image_stream)
                    image.verify()
                    image = Image.open(image_stream)
                except Exception:
                    raise ValueError(f"Image at index {idx} is not a valid file path or base64 encoded string")

            # Apply filters
            np_image = np.array(image, dtype=float)
            self.logger.info(f"Image {idx}: applying filters: {', '.join(all_filters)}")
            for filter_name in all_filters:
                np_mask = np.array(filter_masks[filter_name], dtype=float)
                for y in range(np_image.shape[0]):
                    for x in range(np_image.shape[1]):
                        rgb = np_image[y, x, :3]
                        np_image[y, x, :3] = np.dot(np_mask, rgb)
                np_image = np.clip(np_image, 0, 255)

            modified_image = Image.fromarray(np_image.astype(np.uint8))

            # Save to file
            file_path = ""
            if input_data.output_type in ("file", "both"):
                file_path = f"{self.results_path}/modified_image_{idx}.png"
                modified_image.save(file_path)
            image_file_paths.append(file_path)

            # Convert to base64 string
            b64_string = ""
            if input_data.output_type in ("base64_string", "both"):
                buffered = BytesIO()
                modified_image.save(buffered, format="PNG")
                b64_string = base64.b64encode(buffered.getvalue()).decode('utf-8')
            image_base64_strings.append(b64_string)

        return OutputModel(
            image_base64_strings=image_base64_strings,
            image_file_paths=image_file_paths,
        )
