import matplotlib.pyplot as plt
import torch
import cv2

# Load YOLOv5 model
model = torch.hub.load('ultralytics/yolov5', 'custom', path='models/best.pt')

def inference_dnn(model, image, conf_thres=0.25):
    # Convert image to RGB (YOLOv5 expects RGB)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    # Set model confidence threshold
    model.conf = conf_thres
    
    # Inference
    results = model(image_rgb)

    # Print raw results for debugging
    print(results)

    # Convert results to pandas DataFrame
    return results.pandas().xyxy[0]

if __name__ == '__main__':
    # Load the image
    img = cv2.imread('galaxy.jpeg')
    
    if img is not None:
        # Reduce confidence threshold
        result = inference_dnn(model, img, conf_thres=0.0)  # Set to a lower value like 0.1 for testing
        
        
        
        # Display the image with detections
        for index, row in result.head(1).iterrows():
            x1, y1, x2, y2, conf, cls, label = int(row['xmin']), int(row['ymin']), int(row['xmax']), int(row['ymax']), row['confidence'], int(row['class']), row['name']
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(img, f'{label} {conf:.2f}', (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
        
        # Convert BGR image to RGB for displaying with matplotlib
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        plt.imshow(img_rgb)
        plt.axis('off')
        plt.show()
    else:
        print("Failed to load the image.")
