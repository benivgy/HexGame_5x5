from tensorflow.keras import layers
from tensorflow import keras
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
import pandas as pd
import numpy as np
import tensorflow as tf  # Import TensorFlow module


def ann():
    print("loading")
    df = pd.read_csv('nl_data_cleaned.csv')
    print("loaded")
    X = df.drop(df.columns[25], axis=1).to_numpy()
    y = df.iloc[:, 25].to_numpy()
    print("finished")
    print("training")

    # Set train and test- 20% for test and 80% for train
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size =0.25 )
    print("train: ", X_train.shape, y_train.shape)
    print("test: ", X_test.shape, y_test.shape)

    model = keras.Sequential(
        [
            layers.Dense(256, activation='relu', input_dim=25),
            layers.Dense(128, activation='relu'),#
            layers.Dense(64, activation='relu'),
            layers.Dense(32, activation='relu'),#
            layers.Dense(16, activation='relu'),
            layers.Dense(8, activation='relu'),#
            layers.Dense(4, activation='relu'),
            layers.Dense(2, activation='relu'),#
            layers.Dense(1, activation='linear'),
        ]
    )
    model.summary()

    adam = keras.optimizers.Adam(learning_rate=0.0001)
    model.compile(loss="mean_squared_error", optimizer=adam)

    history = model.fit(
        x=X_train,
        y=y_train,
        validation_data=(X_test, y_test),  # Specify validation data here
        epochs=15,  # adjust epochs as needed
        shuffle=True
    )

    score = model.evaluate(X_test, y_test, verbose=0)
    print("test loss: ", score)

    plt.title('Learning Curves')
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.plot(history.history['loss'], label='Training Loss')
    plt.plot(history.history['val_loss'], label='Validation Loss')
    plt.legend()
    plt.show()

    model.save('my_model.h5')

def grade(boardTOpredict): #Returns the grade from the neural network
    data_array = np.array(list(map(int, boardTOpredict.split(','))))
    model = keras.models.load_model('my_model.h5')
    return model.predict(data_array.reshape(1, -1))[0][0]

if __name__=="__main__":
    print(grade('0,0,2,1,0,0,1,0,0,0,0,0,0,2,0,0,0,0,1,0,2,0,1,0,2'))
