import pandas as pd
import tensorflow as tf
import matplotlib.pyplot as plt

# model machine learning
LOCAL_TRAIN = './beer_images/beers_train'
LOCAL_VAL = './beer_images/beers_validation'
INPUT_SIZE = (280, 280, 3)
BATCH_SIZE = 40


# function to get the local path of the supermarkets images:
def local_beer(local):
    return f'./beer_images/supermarkets/{local}.jpg'


# function to get the data for the model (train and validation generator):
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


# function to get the model:
def get_model(input_shape, num_cla, pre_trained_layer):
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
    x = tf.keras.layers.Dense(units=num_cla, activation=tf.keras.activations.softmax)(x)
    model = tf.keras.Model(pre_trained.input, x)
    model.compile(optimizer=tf.keras.optimizers.RMSprop(lr=0.0001),
                  loss=tf.keras.losses.CategoricalCrossentropy(),
                  metrics=[tf.keras.metrics.CategoricalAccuracy(name='accuracy')])
    return model


# function to plot the metrics of the model:
def plot_training(history):
    """
    plots training metrics
    """
    acc = history.history['accuracy']
    val_acc = history.history['val_accuracy']

    loss = history.history['loss']
    val_loss = history.history['val_loss']

    plt.figure(figsize=(8, 8))
    plt.subplot(2, 1, 1)
    plt.plot(acc, label='Training Accuracy')
    plt.plot(val_acc, label='Validation Accuracy')
    plt.legend(loc='lower right')
    plt.ylabel('Accuracy')
    plt.ylim([min(plt.ylim()), 1])
    plt.title('Training and Validation Accuracy')

    plt.subplot(2, 1, 2)
    plt.plot(loss, label='Training Loss')
    plt.plot(val_loss, label='Validation Loss')
    plt.legend(loc='upper right')
    plt.ylabel('Cross Entropy')
    plt.ylim([0, 1.0])
    plt.title('Training and Validation Loss')
    plt.xlabel('epoch')
    plt.show()


# function to save the model:
def save_model(model):
    model.save_weights('./saved_model/model_3_inceptionv3_280x280_full_weights.h5')
    model_json = model.to_json()
    with open("./saved_model/model_3_inceptionv3_280x280_full.json", 'w+') as json_file:
        json_file.write(model_json)


# main function, call all other functions for get the model of ML:
def analyze(model):
    if model == 'Y':
        brands_model = ['heineken', 'mahou 5 estrellas', 'estrella galicia', 'mahou clasica', 'san miguel']
        num_cla = len(brands_model)

        print('starting training...')
        # data loading
        images_train = get_data(LOCAL_TRAIN, INPUT_SIZE, BATCH_SIZE, train=True)
        images_valid = get_data(LOCAL_VAL, INPUT_SIZE, BATCH_SIZE, train=False)
        # model training
        callback = tf.keras.callbacks.EarlyStopping(monitor="accuracy", mode="max", patience=4)
        model = get_model(INPUT_SIZE, num_cla, pre_trained_layer='mixed7')
        history = model.fit(images_train,
                            validation_data=images_valid,
                            epochs=25,
                            steps_per_epoch=len(images_train),
                            validation_steps=len(images_valid),
                            callbacks=callback)
        print('training complete!')
        # save the model
        save_model(model)
        print('model save')
        # plot the loss and the accuracy of the model
        plot_training(history)
        print('done!')
    else:
        pass
