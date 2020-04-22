import tkinter as tk
import tkinter.filedialog
from tkinter import *
from scipy import stats
import numpy as np
import pandas as pd
import pickle
import matplotlib.pyplot as plt
import seaborn as sns
from tkinter import simpledialog
sns.set()


root = tk.Tk()
root.geometry('500x500')
root.configure(bg='blue')

canvas = Label(root, text="Welcome to testing out your IMU")
canvas.pack()

data = ""
walking_dict = {
    1:'Your walking is near a normal person walking. Keep up the effort!',
    2:'Your walking is good but there is room for improvement. Keep walking as excercise',
    3:'Your walking is becoming worse. Regularly walk to maintain a habit',
    4:'Your walking has become very bad. It is recommended to get your leg checked out by a doctor',
    5:'You may have a problem with your joints and you should immediately consult a doctor'
}

def ml_pred():
    filename = filedialog.askopenfilename()
    data = filename
    predict(data)

def predict(data):
    loaded_model = pickle.load(open('thigh_model.sav', 'rb'))
    # df_motion = pd.read_csv(data,  names=['Time', 'Acceleration(x)', 'Acceleration(y)', 'Acceleration(z)',
    #                     'Magnetometer(x)', 'Magnetometer(y)', 'Magnetometer(z)',
    #                                           'Gyroscope(x)', 'Gyroscope(y)', 'Gyroscope(z)']).drop(columns=['Time'])
    df_motion = pd.read_csv(data,  names=[ 'Acceleration(x)', 'Acceleration(y)', 'Acceleration(z)',
                                            'Magnetometer(x)', 'Magnetometer(y)', 'Magnetometer(z)',
                                              'Gyroscope(x)', 'Gyroscope(y)', 'Gyroscope(z)'])
    result = loaded_model.predict(df_motion)
    result = np.asanyarray(result)
    walking_class = stats.mode(result)[0][0]

    canvas.config(text=walking_dict[walking_class])

def analyze_data():
    df = read_data()
    # title = 'Acceleration'
    title = simpledialog.askstring(title='Analyze with Data', prompt="Would you like to view Acceleration, Gyroscope, Magnetometer data?")
    times = df['Times']

    fig, axs = plt.subplots(3, figsize=(10,8))
    fig.suptitle('time vs. '+title)
    axs[0].plot(times, df[title+'(x)'], 'r')
    axs[1].plot(times, df[title+'(y)'], 'b')
    axs[2].plot(times, df[title+'(z)'], 'g')
    
    plt.xlabel('Time')
    plt.ylabel(title)
    plt.legend(['x dim', 'y dim', 'z dim'])
    plt.show()

    # canvas.config(text=max(df['Acceleration(x)']))
    # canvas.config(text=max(df['Acceleration(y)']))
    # canvas.config(text=max(df['Acceleration(z)']))
    return 0 

def read_data():
    filename = filedialog.askopenfilename()
    df = pd.read_csv(filename,  names=['Times', 'Acceleration(x)', 'Acceleration(y)', 'Acceleration(z)',
                                              'Magnetometer(x)', 'Magnetometer(y)', 'Magnetometer(z)',
                                              'Gyroscope(x)', 'Gyroscope(y)', 'Gyroscope(z)'])
    return df


thigh = Button(root, text="Analyze Thigh/Shin", command=analyze_data)
thigh.pack()


analyze = Button(root, text="Machine Learning Prediction", command=ml_pred)
analyze.pack()


root.mainloop()
