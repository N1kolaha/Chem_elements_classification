import pandas as pd
import joblib
import numpy as np 

data = joblib.load('element_predictor_model.pkl')      
model = data['model']
le_name = data['le_name']


def predict_element(atomic_mass, atomic_radius, density, category, top_n=3):
    cat_map = {"металл": 0, "неметалл": 1, "полуметалл": 2}
    cat_norm = str(category).strip()
    
    if cat_norm not in cat_map:
        return "Ошибка типа", 0.0, []
    
    input_df = pd.DataFrame([[atomic_mass,  atomic_radius, density,  cat_map[cat_norm]]],
                            columns=["Атомная масса", "Атомный радиус", "Плотность", "Тип"])
    
    probabilities = model.predict_proba(input_df)[0]
    top_indices = np.argsort(probabilities)[::-1][:top_n]
    
    results = []
    for idx in top_indices:
        name = le_name.inverse_transform([idx])[0]
        prob = probabilities[idx] * 100
        results.append((name, round(prob, 1)))
    
    return results[0][0], results[0][1], results


if __name__ == "__main__":
    name, conf, top3 = predict_element(12.01, 170, 2.27,  "неметалл")
    print(f"Предсказание: {name} ({conf}%)")
    print(top3)
    