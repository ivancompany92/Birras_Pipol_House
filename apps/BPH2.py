import streamlit as st
import os
import numpy as np
import pandas as pd
import tensorflow as tf
import requests

INPUT_SIZE = (280, 280, 3)
BATCH_SIZE = 1


def file_selector(folder_path='.'):
    filenames = os.listdir(folder_path)
    selected_filename = st.selectbox('Select a file', filenames)
    return os.path.join(folder_path, selected_filename)


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


def df_predict(path):
    data_test = pd.DataFrame(index=range(1), columns=['local', 'brand'])
    data_test.iloc[0, 0] = path
    data_test.iloc[0, 1] = 'unknown'
    return data_test


def load_model():
    model_weights = './saved_model/model_3_inceptionv3_280x280_full_weights.h5'
    model_json = './saved_model/model_3_inceptionv3_280x280_full.json'
    with open(model_json) as json_file:
        loaded_model = tf.keras.models.model_from_json(json_file.read())
    loaded_model.load_weights(model_weights)
    loaded_model.compile(optimizer=tf.keras.optimizers.RMSprop(lr=0.0001),
                         loss=tf.keras.losses.CategoricalCrossentropy(),
                         metrics=[tf.keras.metrics.CategoricalAccuracy(name='accuracy')])
    return loaded_model


def download_image(url, name):
    im_file = requests.get(url)
    open(f'./upload_image/{name}.jpg', 'wb').write(im_file.content)


def app():
    st.header('I do not know the brand ... which beer should I buy? \U0001f648')
    # Select a file
    if st.checkbox('Select a file in current directory'):
        folder_path = './upload_image/'
        if st.checkbox('Change directory'):
            folder_path = st.text_input('Enter folder path', '.')
        filename = file_selector(folder_path=folder_path)
        st.write('You selected `%s`' % filename)
        if st.button('predict the image...'):
            model = load_model()
            data_test = df_predict(filename)
            test_generator = get_data_test(data_test, INPUT_SIZE, BATCH_SIZE, 'local')
            predicts = model.predict(test_generator)
            predicted_class_indices = np.argmax(predicts, axis=1)
            labels = {0: 'estrella galicia', 1: 'heineken', 2: 'mahou 5 estrellas'}
            predictions = [labels[k] for k in predicted_class_indices]
            st.write(f'Your beer picture is the brand: `%s`' % predictions[0])
            st.image(filename)
    elif st.checkbox('if you have a url image:'):
        url = st.text_input('the url image')
        name = st.text_input('name image')
        if st.button('predict the image...'):
            download_image(url, name)
            filename = f'./upload_image/{name}.jpg'
            st.write('You download `%s`' % name)
            model = load_model()
            data_test = df_predict(filename)
            test_generator = get_data_test(data_test, INPUT_SIZE, BATCH_SIZE, 'local')
            predicts = model.predict(test_generator)
            predicted_class_indices = np.argmax(predicts, axis=1)
            labels = {0: 'estrella galicia', 1: 'heineken', 2: 'mahou 5 estrellas'}
            predictions = [labels[k] for k in predicted_class_indices]
            st.write(f'Your beer picture is the brand: `%s`' % predictions[0])
            st.image(filename, width=320)

