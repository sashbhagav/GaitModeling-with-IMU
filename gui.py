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
root.configure(bg='grey')

canvas = Label(root, text="Welcome to testing out your IMU")
canvas.pack()


data = ""
walking_dict = {
    1:'Class 1: Your walking is near a normal person walking. Keep up the effort!',
    2:'Class 2: Your walking is good but there is room for improvement. Keep walking as excercise',
    3:'Class 3: Your walking is becoming worse. Regularly walk to maintain a habit',
    4:'Class 4: Your walking has become very bad. It is recommended to get your leg checked out by a doctor',
    5:'Class 5: You may have a problem with your joints and you should immediately consult a doctor'
}

pressure_dict = {
    1: 'You are applying more pressure on your toe when walking',
    2: 'You are applying more pressure on your heel when walking'
}

def ml_pred(prompt):
    filename = filedialog.askopenfilename(title=prompt)
    return filename

def predict():
    thigh_model = pickle.load(open('thigh_model.sav', 'rb'))
    shin_model = pickle.load(open('shin_model.sav', 'rb'))
    df_thigh = pd.read_csv(ml_pred('Enter your Thigh Data File'),  names=['Time', 'Acceleration(x)', 'Acceleration(y)', 'Acceleration(z)',
                        'Magnetometer(x)', 'Magnetometer(y)', 'Magnetometer(z)',
                                              'Gyroscope(x)', 'Gyroscope(y)', 'Gyroscope(z)']).drop(columns=['Time'])

    df_shin = pd.read_csv(ml_pred('Enter your Shin Data File'),  names=['Time', 'Acceleration(x)', 'Acceleration(y)', 'Acceleration(z)',
                        'Magnetometer(x)', 'Magnetometer(y)', 'Magnetometer(z)',
                                              'Gyroscope(x)', 'Gyroscope(y)', 'Gyroscope(z)']).drop(columns=['Time'])

    result_thigh = thigh_model.predict(df_thigh)
    result_shin = shin_model.predict(df_shin)

    result_thigh = np.asanyarray(result_thigh)
    result_shin = np.asanyarray(result_shin)

    walking_class_thigh = stats.mode(result_thigh)[0][0]
    walking_class_shin = stats.mode(result_shin)[0][0]

    text1 = tk.Text(root, height = 10, width = 100)
    text1.insert(tk.INSERT, 'Your thigh data indicates:: ' + walking_dict[walking_class_thigh]+ '\n')

    text2 = tk.Text(root, height = 10, width = 100)
    text1.insert(tk.INSERT, 'Your shin data indicates:: ' + walking_dict[walking_class_shin] )
    text1.pack()
    text2.pack()

def analyze_data():
    df = read_data()
    # title = 'Acceleration'
    title = simpledialog.askstring(title='Analyze with Data', prompt="Would you like to view Acceleration, Gyroscope, Magnetometer data?")
    times = df['Times']

    fig, axs = plt.subplots(3, figsize=(10,8))
    fig.suptitle('time vs. '+title)
    axs[0].plot(times, df[title+'(x)'], 'r')
    axs[0].legend(['x dim'])
    axs[1].plot(times, df[title+'(y)'], 'b')
    axs[1].legend(['y dim'])
    axs[2].plot(times, df[title+'(z)'], 'g')
    axs[2].legend(['z dim'])
    
    plt.xlabel('Time')
    plt.ylabel(title)
    # plt.legend(['x dim', 'y dim', 'z dim'])
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

def analyze_foot():
    filename = filedialog.askopenfilename()
    foot = pd.read_csv(filename, names=['InsideToePressure', 'OutsideToePressure', 'HeelPressure']).drop(columns='Times')
    model = pickle.load(open('toe_heel_model.sav', 'rb'))
    preds = model.predict(foot)
    classification = stats.mode(preds)[0][0]
    text2 = tk.Text(root, height = 4, width = 100)
    text2.insert(tk.INSERT, 'Your foot pressure data indicates:: ' + pressure_dict[classification] )
    text2.pack()
    return


thigh = Button(root, text="Analyze Thigh/Shin", command=analyze_data)
thigh.pack()

thigh = Button(root, text="Analyze Foot Pressures", command=analyze_foot)
thigh.pack()

analyze = Button(root, text="Machine Learning Prediction", command=predict)
analyze.pack()


root.mainloop()
