import tensorflow as tf, matplotlib.pyplot as plt, numpy as np, cv2, os, random
from sklearn.utils import shuffle
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
from tensorflow.keras.applications import EfficientNetB0
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout

"""
classification model for the backend api
"""

train_dataset = 'dataset/training/' 
test_dataset = 'dataset/testing/'

encode = {'notumor': 0, 'meningioma': 1, 'glioma': 2, 'pituitary': 3}
decode = {0: 'notumor', 1: 'meningioma', 2: 'glioma', 3: 'pituitary'}

image_size_x, image_size_y = 224, 224

def preprocess_image(img_path):
    # read in the image
    if type(img_path) == np.ndarray:
        img = img_path
    else:
        img = cv2.imread(img_path)
        
    # convert image to grayscale
    # img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # normalize the image array
    # img = img / 255

    # resize the image for uniformity
    img = cv2.resize(img, (image_size_x, image_size_y))

    return img

def load_data(dataset_path):
    x_data = [] # images
    y_data = [] # labels

    for folder in os.listdir(dataset_path):
        folder_path = os.path.join(dataset_path, folder)

        # check if the path is a directory and skip if not
        if not os.path.isdir(folder_path):
            continue  
        
        for file in os.listdir(folder_path):
            # find path of the image
            file_path = os.path.join(folder_path, file)

            # preprocess the image
            img = preprocess_image(file_path)

            # append the new image to the x array
            x_data.append(img)

            # append the label to the y array
            y_data.append(encode[folder])
    
    x_data = np.array(x_data)
    y_data = np.array(y_data)

    # shuffle data for better training
    x_data, y_data = shuffle(x_data, y_data, random_state=101)
    
    return x_data, y_data

x_train, y_train = load_data(train_dataset)
x_test, y_test = load_data(test_dataset)

y_train = tf.keras.utils.to_categorical(y_train, num_classes=4)
y_test = tf.keras.utils.to_categorical(y_test, num_classes=4)

efficient_net = EfficientNetB0(weights='imagenet', include_top=False, input_shape=(image_size_x, image_size_y, 3))

model = Sequential([
    efficient_net,
    GlobalAveragePooling2D(),
    Dropout(0.5),
    Dense(4, activation='softmax') 
])

model.compile(optimizer=tf.optimizers.legacy.Adam(learning_rate=0.0001), loss='categorical_crossentropy', metrics=['accuracy'])
model.save('model.h5')