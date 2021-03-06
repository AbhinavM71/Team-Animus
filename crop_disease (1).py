# -*- coding: utf-8 -*-
"""Crop_disease.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1r9JCfluLeQC98Yog_ZhCdjhWGAYWBl2b

# **ArIES Project**

***Identifying plant disease by using images of leaves***

# Loading the Dataset
"""

!wget https://www.dropbox.com/s/r6zdqqtpo7qfetu/Crop%20Disease%20Dataset.zip?dl=0

"""# Unzipping the data"""

!unzip Crop\ Disease\ Dataset.zip\?dl\=0

!pylab inline
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
img = mpimg.imread('/content/Crop Disease Dataset/New Plant Diseases Dataset(Augmented)/New Plant Diseases Dataset(Augmented)/train/Healthy/0008f3d3-2f85-4973-be9a-1b520b8b59fc___JR_HL 4092_flipTB.JPG')
imgplot = plt.imshow(img)
plt.show()

img = mpimg.imread('/content/Crop Disease Dataset/New Plant Diseases Dataset(Augmented)/New Plant Diseases Dataset(Augmented)/train/Unhealthy/038464d1-47a9-4169-afb1-72c87e568a95___RS_GLSp 4480.JPG')
imgplot = plt.imshow(img)
plt.show()

"""# Importing libraries"""

from keras.models import Sequential
from keras.layers import BatchNormalization
from keras.layers.convolutional import Conv2D
from keras.layers.convolutional import MaxPooling2D
from keras.layers.core import Activation, Flatten, Dropout, Dense
from keras.preprocessing.image import ImageDataGenerator
from keras.preprocessing import image
from keras import backend as K
from tensorflow.keras.optimizers import Adam

"""# Initializing Constants"""

EPOCHS = 4
INITIAL_LR = 1e-4
BATCH_SIZE = 32
width = 256
height = 256
depth = 3

train_dir = '/content/Crop Disease Dataset/New Plant Diseases Dataset(Augmented)/New Plant Diseases Dataset(Augmented)/train'
validation_dir = '/content/Crop Disease Dataset/New Plant Diseases Dataset(Augmented)/New Plant Diseases Dataset(Augmented)/valid'

"""# Checking shape of image

"""

inputShape = (height, width, depth)
chanDim=-1
if K.image_data_format() == "channels_first":
    inputShape = (depth, height, width)
    chanDim = 1

"""# Image Data Generation"""

train_gen = ImageDataGenerator(rescale=1.0/255, shear_range=0.2, zoom_range=0.2, horizontal_flip=True)
test_gen = ImageDataGenerator(rescale=1.0/255)

train_generator = train_gen.flow_from_directory(train_dir, target_size=(width, height), batch_size=BATCH_SIZE, class_mode='binary', classes=['Healthy', 'Unhealthy'])
validation_generator = test_gen.flow_from_directory(validation_dir, target_size=(width, height), batch_size=BATCH_SIZE, class_mode='binary')

"""# Visual Representation of Image Data Generation"""

plt.figure(figsize=(12, 12))
for i in range(0, 15):
    plt.subplot(5, 3, i+1)
    for x_batch, y_batch in train_generator:
        img = x_batch[0]
        plt.imshow(img)
        break
plt.tight_layout()
plt.show()

"""# Modelling"""

model = Sequential()

model.add(Conv2D(32, (3, 3), activation="relu", padding="same", input_shape=inputShape))
model.add(Conv2D(32, (3, 3), activation="relu", padding="same"))
model.add(BatchNormalization(axis=chanDim))
model.add(MaxPooling2D(3, 3))
model.add(Dropout(0.25))

model.add(Conv2D(64, (3, 3), activation="relu", padding="same"))
model.add(BatchNormalization(axis=chanDim))
model.add(Conv2D(64, (3, 3), activation="relu", padding="same"))
model.add(BatchNormalization(axis=chanDim))
model.add(MaxPooling2D(3, 3))
model.add(Dropout(0.25))

model.add(Conv2D(128, (3, 3), activation="relu", padding="same"))
model.add(BatchNormalization(axis=chanDim))
model.add(Conv2D(128, (3, 3), activation="relu", padding="same"))
model.add(BatchNormalization(axis=chanDim))
model.add(MaxPooling2D(3, 3))
model.add(Dropout(0.25))

model.add(Flatten())

model.add(Dense(1568,activation="relu"))
model.add(Dropout(0.5))

model.add(Dense(2, activation="softmax"))

model.summary()

"""# Compiling the model"""

opt = Adam(learning_rate=INITIAL_LR, decay=INITIAL_LR/EPOCHS)
model.compile(optimizer=opt, loss="sparse_categorical_crossentropy", metrics=['accuracy'])
model.summary()

"""# Fitting the model"""

history = model.fit_generator(
    train_generator,
    validation_data=validation_generator,
    steps_per_epoch=len(train_generator),
    epochs=EPOCHS, verbose=1
    )

acc = history.history['accuracy']
val_acc = history.history['val_accuracy']
loss = history.history['loss']
val_loss = history.history['val_loss']
epochs = range(1, len(acc) + 1)
#Train and validation accuracy
plt.plot(epochs, acc, 'b', label='Training accurarcy')
plt.plot(epochs, val_acc, 'r', label='Validation accurarcy')
plt.title('Training and Validation accurarcy')
plt.legend()

plt.figure()
#Train and validation loss
plt.plot(epochs, loss, 'b', label='Training loss')
plt.plot(epochs, val_loss, 'r', label='Validation loss')
plt.title('Training and Validation loss')
plt.legend()
plt.show()

print("Train Accuracy  : {:.2f} %".format(acc[-1]*100))

"""# New Section"""

! pip install streamlit -q