import numpy as np 
import cv2
from PIL import Image
import torch 
import torch.nn as nn 
import torchvision.models as models
import torch.nn.functional as F
categories = ["Dyskeratotic", "Koilocytotic", "Metaplastic", "Parabasal", "Superficial-Intermediate"]

efficientnet_b5 = models.efficientnet_b5(pretrained = True)

num_features = efficientnet_b5.classifier[1].in_features
efficientnet_b5.classifier[1] = nn.Linear(num_features, 5)

class EfficientNetWithSoftmax(nn.Module):
    def __init__(self, base_model):
        super(EfficientNetWithSoftmax, self).__init__()
        self.base_model = base_model

    def forward(self, x):
        logits = self.base_model(x) 
        return logits
    
model = EfficientNetWithSoftmax(efficientnet_b5)
model.load_state_dict(torch.load('model/model_V3.pth'))

def predict(image_path):

    image = cv2.imread(image_path)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image_pil = Image.fromarray(image_rgb)
    image_resized = image_pil.resize((64, 64))
    image_array = np.array(image_resized) / 255.0
    image_tensor = torch.tensor(image_array, dtype=torch.float32)

    image_tensor = image_tensor.permute(2, 0, 1).unsqueeze(0) 

    model.eval()  
    with torch.no_grad():
        output = model(image_tensor)  
    _, predicted_class = torch.max(output, 1)  
    predicted_class = predicted_class.item()

    predicted_label = categories[predicted_class]
    true_label = categories[predicted_class]

    return {
        "predicted_class": predicted_class,
        "true_class": predicted_class,
        "predicted_label": predicted_label,
        "true_label": true_label
    }
