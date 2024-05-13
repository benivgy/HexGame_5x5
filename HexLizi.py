import numpy as np
from tensorflow.keras import layers
from tensorflow import keras
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
import pandas as pd
import json
import os


class NeuralNetwork:
    def __init__(self):
        self.dicList = []
        self.move_ranges = [(1, 5), (6, 10), (11, 15), (16, 20), (21, 25)]

    def loadDics(self):
        self.dicList.append(json.load(open('liziFiles/json_files/Hex_board_scores_1-5.json')))
        self.dicList.append(json.load(open('liziFiles/json_files/Hex_board_scores_6-10.json')))
        self.dicList.append(json.load(open('liziFiles/json_files/Hex_board_scores_11-15.json')))
        self.dicList.append(json.load(open('liziFiles/json_files/Hex_board_scores_16-20.json')))
        self.dicList.append(json.load(open('liziFiles/json_files/Hex_board_scores_21-25.json')))

    def convertTOcsv(self):
        with open('liziFiles/data.csv', 'w') as output_file:
            for dic in self.dicList:
                for key in dic:
                    k = [*key]
                    str1 = ''
                    for x in k:
                        str1 = str1 + x + ','
                    output_file.write("%s,%s\n" % (str1[:-1], dic[key][0]))
        output_file.close()


    def ann(self):
        print("loading")
        df = pd.read_csv('liziFiles/data.csv')
        print("loaded")
        X = df.drop(df.columns[25], axis=1).to_numpy()
        y = df.iloc[:, 25].to_numpy()

        # Set train and test- 20% for test and 80% for train
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25)
        print("train: ", X_train.shape, y_train.shape)
        print("test: ", X_test.shape, y_test.shape)

        model = keras.Sequential(
            [
                layers.Dense(256, activation='relu', input_dim=25),
                layers.Dense(64, activation='relu'),
                layers.Dense(16, activation='relu'),
                layers.Dense(4, activation='relu'),
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

        model.save('liziFiles/lizi_model.h5')

    def grade(self,boardTOpredict):  # Returns the grade from the neural network
        data_array = np.array(list(map(int, boardTOpredict.split(','))))
        model = keras.models.load_model('liziFiles/lizi_model.h5')
        return model.predict(data_array.reshape(1, -1))[0][0]


def main():
    nn = NeuralNetwork()
    nn.loadDics()
    print(nn.dicList)
    nn.convertTOcsv()
    nn.ann()
    print(nn.grade('2,1,2,1,0,1,2,2,2,0,2,1,1,1,1,1,2,0,2,2,2,0,1,1,1'))


if __name__ == "__main__":
    main()