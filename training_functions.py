from Country import Country
from Map import Map
from Map import build_simple_map, build_simple_six_map, build_full_map
from Player import Player
import random
import functions
import tensorflow as tf
import numpy as np

def full_train(full_map):

    games_played = 0

    model = tf.keras.models.Sequential()
    model.add(tf.keras.Input(shape=(300)))  
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
    model.add(tf.keras.layers.Dense(159, activation='linear'))

    model.compile(optimizer='adam',loss='mean_squared_error',metrics=['accuracy'])

    fortify_model = tf.keras.models.Sequential()
    fortify_model.add(tf.keras.Input(shape=(300)))  
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
    fortify_model.add(tf.keras.layers.Dense(1723, activation='linear'))

    fortify_model.compile(optimizer='adam',loss='mean_squared_error',metrics=['accuracy'])

    draft_model = tf.keras.models.Sequential()
    draft_model.add(tf.keras.Input(shape=(300)))  
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

    for i in range(10):
        """
        randomess = 100 - (i*20)
        if randomess < 10:
            randomess = 10
        """
        if i > 2:
            randomess = 0
            self_play = True
        else:
            randomess = 100
            self_play = False

        data = None
        while data == None:
            if full_map:
                my_map = build_full_map(randomess)
            else:
                my_map = build_simple_map(randomess)
        
            data = my_map.playTrainingGame(model,fortify_model,draft_model,self_play)
            games_played += 1

        x_train = np.asarray(data[0])
        y_train = np.asarray(data[1])
        f_x_train = np.asarray(data[2])
        f_y_train = np.asarray(data[3])
        d_x_train = np.asarray(data[4])
        d_y_train = np.asarray(data[5])

        for j in range(100):
            if j%10 == 0:
                print(str(j) + '%')
            
            if full_map:
                my_map = build_full_map(randomess)
            else:
                my_map = build_simple_map()

            data = my_map.playTrainingGame(model, fortify_model,draft_model,self_play)
            games_played += 1
            if data != None:
            #x_train.append(data[0][:-3])
                #print('data[2]: \n')
                #print(data[2])
                #print('\n f_x_train: \n')
                #print(f_x_train)
                x_train = np.concatenate((x_train,np.asarray(data[0])),axis=0)
                y_train = np.concatenate((y_train,np.asarray(data[1])),axis=0)
                if len(data[2]) != 0:
                    f_x_train = np.concatenate((f_x_train,np.asarray(data[2])),axis=0)
                if len(data[3]) != 0:
                    f_y_train = np.concatenate((f_y_train,np.asarray(data[3])),axis=0)
                d_x_train = np.concatenate((d_x_train,np.asarray(data[4])),axis=0)
                d_y_train = np.concatenate((d_y_train,np.asarray(data[5])),axis=0)
        
        
        

    


        model.fit(x_train, y_train, epochs=1)
            
        fortify_model.fit(f_x_train, f_y_train, epochs=1)
        
        draft_model.fit(d_x_train, d_y_train, epochs=1)

        performance_checker(model,fortify_model,draft_model,full_map,False,3)
    
    pause = input("Enter anything to continue: ") 

    performance_checker(model,fortify_model,draft_model,full_map,True,1)
    
    return [model,fortify_model,draft_model]
    


def performance_checker(attack_model,fortify_model,draft_model,full_map,display = False, reps = 10):
    count = 0
    ai_name = 'ai_player'
    
    for i in range(reps):
        if full_map:
            test_map = build_full_map(0)
        else:
            test_map = build_simple_map()
        for player in test_map.getPlayerList():
            if player.getName() == ai_name:
                ai_player = player
     
        if test_map.playAiGame(attack_model,fortify_model,ai_player,draft_model,display,full_map) == ai_name:
            count += 1
    f = open("performance.txt", "a")
    f.write('\n' + str((count*6)/reps))
    f.close()