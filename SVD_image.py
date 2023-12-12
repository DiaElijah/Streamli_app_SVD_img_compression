import streamlit as st
from skimage import io
import matplotlib.pyplot as plt
import numpy as np

st.write("""
# Приложение для cингулярного разложения изображений
""")

st.sidebar.header('Пользовательская настройка')

uploaded_img = st.sidebar.file_uploader('Добавь свое изображение', type=['jpeg'])
if uploaded_img is not None:
    input_img = io.imread(uploaded_img)
else:
    input_img = io.imread('https://icdn.lenta.ru/images/2018/05/29/18/20180529181500390/detail_746edc1ca2cc9be68f9d467738fb1c50.jpg')
    
st.sidebar.header('Выбери цветовой канал')
channel = st.sidebar.selectbox('Цветовой канал',('R','G','B','RGB'))

st.sidebar.header('Выбери длину ряда сингулярных чисел')
k = st.sidebar.slider('Количество сингулярных чисел', 1,input_img.shape[1],5)

def SVD_image(image, k):
    U, sing_values, V = np.linalg.svd(image)
    sigma = np.zeros(shape = image.shape)
    np.fill_diagonal(sigma, sing_values)
    trunc_U = U[:, :k]
    trunc_sigma = sigma[:k, :k]
    trunc_V = V[:k, :]
    return(trunc_U@trunc_sigma@trunc_V)

match channel:
        case 'R':
            IMG = input_img.copy()
            IMG[:, :, [1,2]] = 0
            IMG[:, :, 0] = SVD_image(IMG[:, :, 0], k)
        case 'G':
            IMG = input_img.copy()
            IMG[:, :, [0,2]] = 0
            IMG[:, :, 1] = SVD_image(IMG[:, :, 1], k)
        case 'B':
            IMG = input_img.copy()
            IMG[:, :, [0,1]] = 0
            IMG[:, :, 2] = SVD_image(IMG[:, :, 2], k)
        case 'RGB':
            IMG = input_img.copy()
            IMG[:, :, 0] = SVD_image(IMG[:, :, 0], k)
            IMG[:, :, 1] = SVD_image(IMG[:, :, 1], k)
            IMG[:, :, 2] = SVD_image(IMG[:, :, 2], k)

st.subheader('Что же получается')
# st.image(IMG, caption='SVD Image', use_column_width=True)
plt.imshow(IMG)
st.pyplot(plt.gcf())
