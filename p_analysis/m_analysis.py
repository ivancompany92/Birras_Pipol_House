import pandas as pd
import logging
import re
import numpy as np
import tensorflow as tf
from pathlib import Path
import matplotlib.pyplot as plt

# model machine learning
LOCAL_TRAIN = './beer_images/beers_train'
LOCAL_VAL = './beer_images/beers_validation'
INPUT_SIZE = (280, 280, 3)
BATCH_SIZE = 40


def local_beer(local):
    return f'./beer_images/supermarkets/{local}.jpg'


def get_data(directory, input_shape, batch_size, train=True):
    if train:
        datagen = tf.keras.preprocessing.image.ImageDataGenerator(rescale=1 / 255,
                                                                  rotation_range=60,
                                                                  width_shift_range=0.4,
                                                                  height_shift_range=0.4,
                                                                  shear_range=0.4,
                                                                  zoom_range=0.4,
                                                                  horizontal_flip=True,
                                                                  fill_mode='nearest')
    else:
        datagen = tf.keras.preprocessing.image.ImageDataGenerator(rescale=1 / 255)
    generator = datagen.flow_from_directory(directory,
                                            batch_size=batch_size,
                                            class_mode='categorical',
                                            target_size=(input_shape[0], input_shape[1]))
    return generator


def get_data_test(dataframe, input_shape, batch_size, x_col):
    datagen = tf.keras.preprocessing.image.ImageDataGenerator(rescale=1 / 255)
    generator = datagen.flow_from_dataframe(dataframe,
                                            x_col=x_col,
                                            y_col=None,
                                            batch_size=batch_size,
                                            shuffle=False,
                                            class_mode=None,
                                            target_size=(input_shape[0], input_shape[1]))
    return generator


def get_model(input_shape, pre_trained_layer):
    pre_trained = tf.keras.applications.InceptionV3(input_shape=input_shape,
                                                    include_top=False,
                                                    weights='imagenet')
    for layer in pre_trained.layers:
        layer.trainable = False
    last_layer = pre_trained.get_layer(pre_trained_layer)
    last_output = last_layer.output
    x = tf.keras.layers.Flatten()(last_output)
    x = tf.keras.layers.Dense(units=1024,
                              activation=tf.keras.activations.relu)(x)
    x = tf.keras.layers.Dropout(0.2)(x)
    x = tf.keras.layers.Dense(units=3, activation=tf.keras.activations.softmax)(x)
    model = tf.keras.Model(pre_trained.input, x)
    model.compile(optimizer=tf.keras.optimizers.RMSprop(lr=0.0001),
                  loss=tf.keras.losses.CategoricalCrossentropy(),
                  metrics=[tf.keras.metrics.CategoricalAccuracy(name='accuracy')])
    return model


class EnoughTrainingCallback(tf.keras.callbacks.Callback):
    def __init__(self, metric, threshold):
        super(EnoughTrainingCallback, self).__init__()
        self.metric = metric
        self.threshold = threshold
        self.logger = get_logger(__name__)

    def on_epoch_end(self, epoch, logs=None):
        if logs.get(self.metric) > self.threshold:
            self.logger.info(f'reached over {self.threshold} {self.metric}, stopping training...')
            self.model.stop_training = True


def get_logger(name):
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    return logger


logger = get_logger(__name__)


def plot_training(history, metrics: list = ('loss',), figsize: tuple = (12, 5), skip=0, val=True):
    """
    plots training selected metrics for every batch
    """
    epochs = range(1 + skip, len(history.history[metrics[0]]) + 1)
    fig, ax_arr = plt.subplots(1, len(metrics), figsize=figsize)
    if not isinstance(ax_arr, np.ndarray):
        ax_arr = np.array(ax_arr).reshape(1, )
    for i, metric in enumerate(metrics):
        ax_arr[i].plot(epochs, history.history[metric][skip:], color='k', linestyle='solid', label=metric, linewidth=2)
        if val:
            ax_arr[i].plot(epochs, history.history[f"val_{metric}"][skip:], color='r', linestyle='dotted',
                           label=f'validation {metric}')
        ax_arr[i].set_ylabel(metric)
        ax_arr[i].set_xlabel('epochs')
        ax_arr[i].grid()
        ax_arr[i].legend()
    plt.show()


def analyze(data_beer, model):
    if model == 'Y':
        brands_model = ['heineken', 'mahou 5 estrellas', 'estrella galicia']
        data_model = data_beer[data_beer.brand.isin(brands_model)]
        data_model.reset_index(inplace=True)

        data_beer_images = pd.DataFrame(columns=['local', 'brand'])
        data_beer_images['brand'] = data_model['brand']
        data_beer_images['local'] = data_model['id'].apply(local_beer)

        logger.info('starting training...')
        # data loading
        images_train = get_data(LOCAL_TRAIN, INPUT_SIZE, BATCH_SIZE, train=True)
        images_valid = get_data(LOCAL_VAL, INPUT_SIZE, BATCH_SIZE, train=False)
        # model training
        enough_training_callback = EnoughTrainingCallback(metric='accuracy', threshold=0.97)
        model = get_model(INPUT_SIZE, pre_trained_layer='mixed7')
        history = model.fit(images_train,
                            validation_data=images_valid,
                            epochs=10,
                            steps_per_epoch=len(images_train),
                            validation_steps=len(images_valid),
                            callbacks=[enough_training_callback])
        model.save('./saved_model/model_3_inceptionv3_280x280.h5')
        plot_training(history, metrics=['loss', 'accuracy'])
        # model testing
        images = get_data_test(data_beer_images, INPUT_SIZE, BATCH_SIZE, 'local')
        predicts = model.predict(images)
        predicted_class_indices=np.argmax(predicts,axis=1)
        labels = images_train.class_indices
        labels = dict((v, k) for k, v in labels.items())
        predictions = [labels[k] for k in predicted_class_indices]
        print(predictions)
        logger.info('done!')
        return predictions
    else:
        pass