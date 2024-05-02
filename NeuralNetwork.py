import numpy as np
from tensorflow.keras import layers
from tensorflow import keras
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from tensorflow.keras.utils import plot_model
from keras import backend as K
import pandas as pd



#clean the csv file:
def clean():
    #Removing the last column
    print("reading")
    df=pd.read_csv('nl_data.csv')
    print("finished")
    column_to_delete = df.columns[26]
    df=df.drop(column_to_delete, axis=1)
    df.to_csv('nl_data_cleaned.csv', index=False) #no index column

def ann():
    df = pd.read_csv('mini.csv')
    X = df.drop(df.columns[25], axis=1).to_numpy()
    y = df.iloc[:, 25].to_numpy()

    # Set train and test- 20% for test and 80% for train
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size =0.25 )
    print("train: ", X_train.shape, y_train.shape)
    print("test: ", X_test.shape, y_test.shape)

    model = keras.Sequential(
        [
            layers.Dense(256, activation='relu', input_dim=25),
            layers.Dense(128, activation='relu'),
            layers.Dense(64, activation='relu'),
            layers.Dense(32, activation='relu'),
            layers.Dense(16, activation='relu'),
            layers.Dense(8, activation='relu'),
            layers.Dense(4, activation='relu'),
            layers.Dense(2, activation='relu'),
            layers.Dense(1, activation='linear'),
        ]
    )
    model.summary()

    # plot_model(model, 'model.png', show_shapes=True)
    adam = keras.optimizers.Adam(learning_rate=0.001)
    model.compile(loss="mean_squared_error", optimizer="adam", metrics=keras.metrics.mean_squared_error)
    history = model.fit(X_train, y_train, batch_size=2048, epochs=50, validation_split = .2)

    score = model.evaluate(X_test, y_test, verbose=0)
    print("test loss: ", score[0])
    print("test accuracy: ", score[1])

    plt.title('learning curves')
    plt.xlabel('epoch')
    plt.ylabel('MSE accuracy')
    plt.plot(history.history['mean_squared_error'])  # Orange
    plt.plot(history.history['val_mean_squared_error'])  # Blue
    plt.legend()

    model.predict([[1,2,0,0,2,0,2,0,0,0,0,1,0,0,0,0,1,2,0,0,1,0,0,1,0]])



if __name__=="__main__":
    ann()




# class NeuralNetwork:
#     def __init__(self):
#         self.df=pd.read_csv('nl_data.csv')
#         column_to_delete = self.df.columns[25]
#         self.df.drop(column_to_delete, axis=1, inplace=True)
#



