import io
import os
from google.cloud import vision

# Set the path to the service account key file
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'Document from Muhd.json'

def detect_objects(image_path):
    # Initialize the Vision API client
    client = vision.ImageAnnotatorClient()

    # Load the image into memory
    with io.open(image_path, 'rb') as image_file:
        content = image_file.read()
    image = vision.Image(content=content)

    # Perform object detection
    response = client.object_localization(image=image)
    objects = response.localized_object_annotations

    print('Objects:')
    for object_ in objects:
        print(f'\nName: {object_.name}')
        print(f'Score: {object_.score}')
        print('Bounding Polygon:')
        for vertex in object_.bounding_poly.normalized_vertices:
            print(f' - ({vertex.x}, {vertex.y})')

    if response.error.message:
        raise Exception(f'{response.error.message}')

# Example usage
detect_objects('horsey.webp')
