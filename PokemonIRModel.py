import pathlib
import matplotlib.pyplot as plt
import cv2 as cv
from PIL import Image
import tensorflow as tf
import numpy as np
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.models import Sequential
import os

def setUpModel():    
    data_dir =  'pokemon'
    data_dir = pathlib.Path(data_dir)

    train_ds = tf.keras.utils.image_dataset_from_directory(
        data_dir,
        validation_split=0.2,
        subset="training",
        seed=123,
        image_size=(50,50),
        batch_size=100)

    val_ds = tf.keras.utils.image_dataset_from_directory(
        data_dir,
        validation_split=0.2,
        subset="validation",
        seed=123,
        image_size=(50,50),
        batch_size=100) 

    class_names = train_ds.class_names

    num_classes = len(class_names)
    model = Sequential([
        layers.Rescaling(1./255, input_shape=(50,50,3)),
        layers.Conv2D(16,3,padding='same', activation='relu'),
        layers.MaxPooling2D(),
        layers.Conv2D(32,3,padding='same', activation='relu'),
        layers.MaxPooling2D(),
        layers.Conv2D(64,3,padding='same', activation='relu'),
        layers.MaxPooling2D(),
        layers.Flatten(),
        layers.Dense(128,activation='relu'),
        layers.Dense(num_classes)
    ])

    model.compile(optimizer='adam',
                loss=tf.keras.losses.SparseCategoricalCrossentropy(
                    from_logits=True),
                metrics=['accuracy'])

    epochs=1
    model.fit(
        train_ds,
        validation_data=val_ds,
        epochs=epochs
    )
    print(class_names)
    return model, class_names
    
    '''
    #Accuracy
    acc = history.history['accuracy']
    val_acc = history.history['val_accuracy']

    #Loss
    loss = history.history['loss']
    val_loss = history.history['val_loss']

    #epochs
    epochs_range = range(epochs)

    #Plotting graphs
    plt.figure(figsize=(8,8))
    plt.subplot(1,2,1)
    plt.plot(epochs_range, acc, label='Training Accuracy')
    plt.plot(epochs_range,val_acc,label='Validation Accuracy')
    plt.legend(loc='lower right')
    plt.title('Training and Validation Accuracy')

    plt.subplot(1,2,2)
    plt.plot(epochs_range, loss, label='Training Loss')
    plt.plot(epochs_range, val_loss, label='Validation Loss')
    plt.legend(loc='upper right')
    plt.title('Training and Validation Loss')
    plt.show()
    '''

def identifyPokemon(model, pokemontofind, class_names):
    pokemontofind = pathlib.Path(pokemontofind)
    #pokemontofind = list(pokemontofind.glob('*.*'))
    print(pokemontofind)
    img = tf.keras.preprocessing.image.load_img(pokemontofind, target_size=(50,50))
    img_array = tf.keras.utils.img_to_array(img)
    img_array = tf.expand_dims(img_array, 0)
    predictions = model.predict(img_array)
    score = tf.nn.softmax(predictions[0])
    print(class_names[np.argmax(score)])
    os.remove(pokemontofind)
    return class_names[np.argmax(score)]
