import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Activation
from keras.layers.recurrent import LSTM
from keras import backend as K
from keras.callbacks import EarlyStopping


maxlen = 25     #さかのぼる過去の数
'''
入力データ
'''
with open('./Data/どうせなら幸せになろうと思います.txt', 'rt') as file:
    words = file.read()

wordsplit = words.split('\n')
X = np.array( [] )

'''
モデル設定
'''
# 基本設定値

n_in = 5        #入力層のニューロン数
n_hidden = 20   #中間層のニューロン数
n_out = 20      #出力層のニューロン数

def weight_variable(shape):
    return K.truncated_normal(shape, stddev=0.01)

# モデル構造
model = Sequential()
model.add(LSTM(n_hidden,
               init=weight_variable,
               input_shape=(maxlen, n_out))
model.add(Dense(n_out, init=weight_variable))
model.add(Activation('linear'))

optimizer = Adam(lr=0.001, beta_1=0.9, beta_2=0.999)
model.compile(loss='mean_squared_error', optimizer=optimizer)

'''
モデル学習
'''
epochs = 500    # 学習回数
batch_size = 10 # バッチサイズ
early_stopping = EarlyStopping(monitor='val_loss', patience=500, verbose=1)

hist = model.fit(X_train, Y_train, batch_size=batch_size,
                 epochs=epochs,
                 validation_data=(X_validation, Y_validation),
                 callbacks=[early_stopping])

