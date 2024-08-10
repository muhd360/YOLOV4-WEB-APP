import cv2
import numpy as np

# Paths to your custom model files
config_path = "/home/muhd/Desktop/python-proj/FullStack_Web_APP/Web_Dev_AI/models/yolov7-tiny.cfg"
weights_path = "/home/muhd/Desktop/python-proj/FullStack_Web_APP/Web_Dev_AI/models/yolov7-tiny.weights"
names_path = "/home/muhd/Desktop/python-proj/FullStack_Web_APP/Web_Dev_AI/models/coco-classes.txt"

# Load YOLO model
net = cv2.dnn.readNet(weights_path, config_path)

# Load class names
with open(names_path, "r") as f:
    classes = [line.strip() for line in f.readlines()]

# Get the output layer names
# Get the output layer names
layer_names = net.getLayerNames()

# Get the indices of the output layers
unconnected_out_layers = net.getUnconnectedOutLayers()

# Handle single layer and multiple layers scenario
if isinstance(unconnected_out_layers, np.ndarray):
    output_layers = [layer_names[i - 1] for i in unconnected_out_layers.flatten()]
else:
    output_layers = [layer_names[unconnected_out_layers - 1]]
# Load an image
img = cv2.imread("static/uploads/horse.jpeg")
height, width, channels = img.shape

# Prepare the image for the model
blob = cv2.dnn.blobFromImage(img, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
net.setInput(blob)

# Forward pass
outs = net.forward(output_layers)

# Analyze the detections
class_ids = []
confidences = []
boxes = []
for out in outs:
    for detection in out:
        scores = detection[5:]
        class_id = np.argmax(scores)
        confidence = scores[class_id]
        if confidence > 0.5:  # You can adjust this threshold
            center_x = int(detection[0] * width)
            center_y = int(detection[1] * height)
            w = int(detection[2] * width)
            h = int(detection[3] * height)

            # Rectangle coordinates
            x = int(center_x - w / 2)
            y = int(center_y - h / 2)

            boxes.append([x, y, w, h])
            confidences.append(float(confidence))
            class_ids.append(class_id)

# Draw bounding boxes and labels
for i in range(len(boxes)):
    x, y, w, h = boxes[i]
    label = str(classes[class_ids[i]])
    color = (0, 255, 0)  # Green color
    cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)
    cv2.putText(img, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)

# Show the image with detections
cv2.imshow("Image", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
