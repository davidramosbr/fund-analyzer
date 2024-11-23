import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import os
import numpy as np

# POSTERIORMENTE VOU TENTAR FAZER COM QUE O CODIGO USE A NN PARA
# VERIFICAR A QUALIDADE DO FUNDO ANTES DE FAZER A RECOMENDAÇÃO
# MAS AINDA ESTOU PENSANDO EM COMO IMPLEMENTAR ISSO

def build_model():
    model = tf.keras.Sequential([
        tf.keras.layers.Dense(64, activation='relu', input_shape=(8,)),
        tf.keras.layers.Dense(32, activation='relu'),
        tf.keras.layers.Dense(1, activation='sigmoid')
    ])
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    return model

def train_and_evaluate(data, labels):
    X_train, X_temp, y_train, y_temp = train_test_split(data, labels, test_size=0.3, random_state=42)
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_temp = scaler.transform(X_temp)
    model = build_model()
    model.fit(X_train, y_train, epochs=10, batch_size=32)
    accuracy = model.evaluate(X_temp, y_temp)
    print(f"Acurácia do modelo: {accuracy[1]}")
    return model

def load_or_create_model():
    model_save_path = 'model.h5'
    if os.path.exists(model_save_path):
        model = tf.keras.models.load_model(model_save_path)
        print(f"Modelo carregado de {model_save_path}")
    else:
        print("Nenhum modelo encontrado. Criando um novo modelo.")
        model = build_model()
    return model

def calculate_fund_scores(fund_data):
    pvp_scores = []
    price_return_scores = []
    yield_scores = []
    
    pvp_values = [fund[3] for fund in fund_data]
    min_pvp = min(pvp_values)
    max_pvp = max(pvp_values)
    
    if len(fund_data) == 1:
        pvp_scores = [50]
    elif max_pvp != min_pvp:
        for pvp in pvp_values:
            pvp_scores.append(50 + 50 * (pvp - min_pvp) / (max_pvp - min_pvp))
    else:
        pvp_scores = [50] * len(pvp_values)

    price_values = [fund[1] for fund in fund_data]
    last_return_values = [fund[6] for fund in fund_data]
    ratios = []
    
    for last_return, price in zip(last_return_values, price_values):
        if price != 0:
            ratios.append(last_return / price)
        else:
            ratios.append(0)
    
    if len(fund_data) > 1:
        max_ratio = max(ratios)
        min_ratio = min(ratios)
        for ratio in ratios:
            price_return_scores.append(50 + 50 * (ratio - min_ratio) / (max_ratio - min_ratio))
    else:
        price_return_scores = [50] * len(ratios)

    yield_values = [fund[8] for fund in fund_data] 
    price_values = [fund[1] for fund in fund_data]

    yield_ratios = []
    for yield_value, price in zip(yield_values, price_values):
        if price != 0:
            yield_ratios.append(yield_value / price)
        else:
            yield_ratios.append(0)

    if len(fund_data) > 1:
        max_yield_ratio = max(yield_ratios)
        min_yield_ratio = min(yield_ratios)
        for ratio in yield_ratios:
            yield_scores.append(100 + 100 * (ratio - min_yield_ratio) / (max_yield_ratio - min_yield_ratio))
    else:
        yield_scores = [100] * len(yield_ratios)

    # essa etapa vai verificar a quantidade desse mesmo fundo que já está disponível na carteira
    # caso já tenha muitas cotas desse fundo, o score diminui, caso tenha poucas, aumenta
    # fazendo assim o usuário ter uma variação da carteira
    
    wallet_score = 300

    total_scores = []
    for pvp_score, price_return_score, yield_score in zip(pvp_scores, price_return_scores, yield_scores):
        total_scores.append((pvp_score + price_return_score + yield_score, wallet_score) / 7)

    return total_scores

# teste falhou
def calculate_fund_scores_with_nn(fund_data):
    scaler = StandardScaler()
    fund_data_scaled = scaler.fit_transform(fund_data)
    model = load_or_create_model()
    predictions = model.predict(fund_data_scaled)
    return predictions.flatten()
