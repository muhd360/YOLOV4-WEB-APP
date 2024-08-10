import os
import cv2
import time
import json

class Yolov7DNNInference:
    
    '''
        target: Inference DNN Opencv with ONNX
        param[1]: path to yolov4 confioguration
        param[2]:  path to yolov4 weights
        
    '''
    
    def __init__(self,  path_to_cfg, path_to_weights):
        
        self.path_to_cfg = path_to_cfg
        self.path_to_weights = path_to_weights
    
    def inference_dnn(self, image):

        # read dnn of yolov4
        # weights and config
        network = cv2.dnn.readNetFromDarknet(self.path_to_cfg, self.path_to_weights)
        # gpu or cpu 
        network.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
        network.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA_FP16) # floating point 16

       #creates net from file with trained weights and config, 
        model = cv2.dnn_DetectionModel(network)

        #set model parameters 

        model.setInputParams(size=(640, 640), scale=1/255, swapRB=True)

        '''
        classIds	Class indexes in result detection.
        [out]	confidences	A set of corresponding confidences.
        [out]	boxes	A set of bounding boxes.
        '''
        classes, scores, boxes = model.detect(image, self.conf_threshold, self.nms_threshold)

        return classes, scores, boxes
    



class Yolov7Processor(Yolov7DNNInference):
    
    
   # INIT of  Parameters
                        #[]=0.3         #[]=0.38
    def __init__(self, nms_threshold, conf_threshold, class_labels, image_path, path_to_cfg, path_to_weights, single_image=False):
        
        super().__init__(path_to_cfg, path_to_weights)

        # non max suppression threshold
        self.nms_threshold = nms_threshold

        # confidence threshold
        self.conf_threshold = conf_threshold
        
        self.images_list = []
        

        # class labels 
        self.class_labels = class_labels
        
        # image path
        self.image_path = image_path
        
        self.single_image = None
        
        self.image_coordinates = []
        
        # read classes coco file with open()
        with open(class_labels, 'r') as read_class:
            self.class_labels= [ classes.strip() for classes in read_class.readlines()]


       

    
        # frame image
        # load images     
        if not single_image: 
        
            self.frames = self.load_images(self.image_path)

            # preprocess images and resize it
            for self.frame in self.frames:
                
                self.image = cv2.imread(self.frame)
                
                # get height and width of images

                self.original_h, self.original_w = self.image.shape[:2]
            
                dimension = (640, 640)

                # resize images
                self.resize_image = cv2.resize(self.image, dimension, interpolation=cv2.INTER_AREA)

                # get new height and width of resized image

                self.new_h, self.new_w = self.resize_image.shape[:2]

                # Call Function Inference RUN
                self.inference_run(self.resize_image)
                        
        else:
            self.single_image = self.image_path
            
     
    '''
            Function Target: Load Images
            param[1] : self
            param[2]: image_path

    '''
    def load_images(self, image_path):

            # list of images

        
        img_list = [os.path.join(image_path, img_original) for img_original in os.listdir(image_path) if img_original.endswith(('.png', '.jpg', '.jpeg'))]
        return img_list

    '''
    target: Inference Run and Draw Bounding boxes
    param[1] : image

    '''
    
    def inference_run(self, image):

        # start 

        start = time.time()

        # get classes, get boxes, get score
        # inference for every frame
        getClasses, getScores, getBoxes = self.inference_dnn(image)
        

        end = time.time()

        # FRAME time

        frame_time = (end-start) * 1000

        # Frame per second

        FPS = 1.0 * (end-start)
 
       
        #calculate new scale of image which is image formed between original and resized
    

        # new image ratio  height
        ratio_h = self.new_h / self.original_h

        # new image ratio width
        ratio_w = self.new_w / self.original_w

       
        
        
        for (class_id, score, box) in zip(getClasses, getScores, getBoxes):
                     
            json_result = {
            "class_name" : self.class_labels[class_id],
            "probability" : str(score),
            "class_id": str(class_id),
            "datetime": time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
            }
            
            self.image_coordinates.append(json_result)
            
              

        
        return self.image_coordinates
        
    
    def convert_results_to_json(self):
        
        
        print("TYPE: ",type(self.image_coordinates))
        print("TYPE JSON: ",type(json.dumps(self.image_coordinates)))
        return json.dumps(self.image_coordinates)
 
    
    def inference_image_run(self, img_name):
        
        self.images_list.clear()
        
        image = cv2.imread(self.single_image)
        
        image_raw  = image.copy()
        
        self.images_list.append(image_raw)
       
       # image = cv2.imread(image_raw)
            
        # get height and width of images

        original_h, original_w = image.shape[:2]
          
        dimension = (640, 640)

        # resize images
        resized_image = cv2.resize(image, dimension, interpolation=cv2.INTER_AREA)

        # get new height and width of resized image

        new_h, new_w = resized_image.shape[:2]
    
        # start 

        start = time.time()

        # get classes, get boxes, get score
        # inference for every frame
        getClasses, getScores, getBoxes = self.inference_dnn(image)
        

        end = time.time()

        # FRAME time

        frame_time = (end-start) * 1000

        # Frame per second

        FPS = 1.0 * (end-start)
 
       
        #calculate new scale of image which is image formed between original and resized
    

        #calculate new scale of image which is image formed between original and resized

        # new image ratio  height
        ratio_h = new_h / original_h

        # new image ratio width
        ratio_w = new_w / original_w


        
        
        for (class_id, score, box) in zip(getClasses, getScores, getBoxes):
            #print(f"Class ID: {class_id}, Score : {score},  Box: {box}")

           # print(f"Box Coordinates: ", box)
            
            # normalize bounding box to detection
            box[0] = int(box[0] * ratio_w) # x
            box[1] = int(box[1] * ratio_h) # y
            box[2] = int(box[2] * ratio_w) # width
            box[3] = int(box[3] * ratio_h) # height


            cv2.rectangle(resized_image, box, (114,114,114), 2)
            label = "Frame Time : %.2f ms, FPS : %.2f , ID: %s, Score: %.2f," % (frame_time, FPS ,self.class_labels[class_id], score)

            # calculate fps
            cv2.putText(resized_image, label, (box[0]-30, box[1]-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5,  (0, 0, 255), 2)

        self.images_list.append(resized_image)
           
        saved_images_path = self.save_image_postprocessed(self.images_list, img_name)      
            
        return saved_images_path
    # save img to flask static uploads
    def save_image_postprocessed(self, images, img_name):
        
        base_img_name = os.path.splitext(img_name)[0]
        
        save_dir = os.path.join('static/uploads', base_img_name)
        
        if not os.path.exists(save_dir):    
            os.makedirs(save_dir)
            print("Created directory:", save_dir)
        else:
            print("Directory already exists:", save_dir)

        
        saved_images = []
        for idx, img in enumerate(images):
            save_path = os.path.join(save_dir, f"image_{idx}.jpg")
           # save_path = os.path.join(save_dir, img)
           # print("IMG", save_path)
            cv2.imwrite(save_path, img)
            saved_images.append(save_path)
        
        return saved_images
    