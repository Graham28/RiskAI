from Country import Country
from Map import Map
from Map import build_simple_map, build_simple_six_map, build_full_map
from Player import Player
import random
import functions
import tensorflow as tf
import numpy as np

def full_train():
    model = tf.keras.models.Sequential()
    model.add(tf.keras.Input(shape=(294)))  
    model.add(tf.keras.layers.Dense(2048, activation='relu'))
    model.add(tf.keras.layers.Dense(2048, activation='relu'))
    model.add(tf.keras.layers.Dropout(0.2))
    model.add(tf.keras.layers.Dense(2048, activation='relu'))
    model.add(tf.keras.layers.Dropout(0.2))
    model.add(tf.keras.layers.Dense(2048, activation='relu'))
    model.add(tf.keras.layers.Dropout(0.2))
    model.add(tf.keras.layers.Dense(2048, activation='relu'))
    model.add(tf.keras.layers.Dense(2048, activation='relu'))
    model.add(tf.keras.layers.Dropout(0.2))
    model.add(tf.keras.layers.Dense(2048, activation='relu'))
    model.add(tf.keras.layers.Dropout(0.2))
    model.add(tf.keras.layers.Dense(2048, activation='relu'))
    model.add(tf.keras.layers.Dropout(0.2))
    model.add(tf.keras.layers.Dense(158, activation='linear'))

    model.compile(optimizer='adam',loss='mean_squared_error',metrics=['accuracy'])

    fortify_model = tf.keras.models.Sequential()
    fortify_model.add(tf.keras.Input(shape=(294)))  
    fortify_model.add(tf.keras.layers.Dense(2048, activation='relu'))
    fortify_model.add(tf.keras.layers.Dense(2048, activation='relu'))
    fortify_model.add(tf.keras.layers.Dropout(0.2))
    fortify_model.add(tf.keras.layers.Dense(4096, activation='relu'))
    fortify_model.add(tf.keras.layers.Dropout(0.2))
    fortify_model.add(tf.keras.layers.Dense(2048, activation='relu'))
    fortify_model.add(tf.keras.layers.Dense(2048, activation='relu'))
    fortify_model.add(tf.keras.layers.Dropout(0.2))
    fortify_model.add(tf.keras.layers.Dense(4096, activation='relu'))
    fortify_model.add(tf.keras.layers.Dropout(0.2))
    fortify_model.add(tf.keras.layers.Dense(1722, activation='linear'))

    fortify_model.compile(optimizer='adam',loss='mean_squared_error',metrics=['accuracy'])

    draft_model = tf.keras.models.Sequential()
    draft_model.add(tf.keras.Input(shape=(294)))  
    draft_model.add(tf.keras.layers.Dense(2048, activation='relu'))
    draft_model.add(tf.keras.layers.Dense(2048, activation='relu'))
    draft_model.add(tf.keras.layers.Dropout(0.2))
    draft_model.add(tf.keras.layers.Dense(2048, activation='relu'))
    draft_model.add(tf.keras.layers.Dropout(0.2))
    draft_model.add(tf.keras.layers.Dense(2048, activation='relu'))
    draft_model.add(tf.keras.layers.Dense(2048, activation='relu'))
    draft_model.add(tf.keras.layers.Dropout(0.2))
    draft_model.add(tf.keras.layers.Dense(1024, activation='relu'))
    draft_model.add(tf.keras.layers.Dropout(0.2))
    draft_model.add(tf.keras.layers.Dense(42, activation='linear'))

    draft_model.compile(optimizer='adam',loss='mean_squared_error',metrics=['accuracy'])

    for i in range(5):
        data = None
        while data == None:
            my_map = build_full_map()
        
            data = my_map.playTrainingGame3(model,fortify_model,draft_model)
        
        x_train = np.asarray(data[0])
        y_train = np.asarray(data[1])
        f_x_train = np.asarray(data[2])
        f_y_train = np.asarray(data[3])
        d_x_train = np.asarray(data[4])
        d_y_train = np.asarray(data[5])

        for j in range(100):
            if j%10 == 0:
                print(str(j) + '%')
            my_map = build_full_map()
            data = my_map.playTrainingGame3(model, fortify_model,draft_model)
            if data != None:
            #x_train.append(data[0][:-3])
                x_train = np.concatenate((x_train,np.asarray(data[0])),axis=0)
                y_train = np.concatenate((y_train,np.asarray(data[1])),axis=0)
                f_x_train = np.concatenate((f_x_train,np.asarray(data[2])),axis=0)
                f_y_train = np.concatenate((f_y_train,np.asarray(data[3])),axis=0)
                d_x_train = np.concatenate((d_x_train,np.asarray(data[4])),axis=0)
                d_y_train = np.concatenate((d_y_train,np.asarray(data[5])),axis=0)
    


        model.fit(x_train, y_train, epochs=3)
            
        fortify_model.fit(f_x_train, f_y_train, epochs=3)
        
        draft_model.fit(d_x_train, d_y_train, epochs=3)
    
    return [model,fortify_model,draft_model]
    