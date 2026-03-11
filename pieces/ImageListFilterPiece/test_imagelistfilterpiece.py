from domino.testing import piece_dry_run
from pathlib import Path
from PIL import Image
from io import BytesIO
import base64


img_path = str(Path(__file__).parent / "test_image.png")
img = Image.open(img_path)
buffered = BytesIO()
img.save(buffered, format="PNG")
base64_image = base64.b64encode(buffered.getvalue()).decode("utf-8")


def test_imagelistfilterpiece():
    input_data = dict(
        input_images=[base64_image, base64_image],
        sepia=True,
        blue=True,
        output_type="both"
    )
    piece_output = piece_dry_run(
        piece_name="ImageListFilterPiece",
        input_data=input_data
    )
    assert piece_output is not None
    assert len(piece_output.get('image_file_paths')) == 2
    assert all(p.endswith('.png') for p in piece_output.get('image_file_paths'))
    assert len(piece_output.get('image_base64_strings')) == 2
    assert all(s for s in piece_output.get('image_base64_strings'))
