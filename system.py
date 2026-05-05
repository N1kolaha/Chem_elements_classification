import ml,database

database.start()
print("\n\nОтвет системы основанной на знаниях:")
result = database.find_chem_element("26.98","184","2.70","металл")
name, conf, top3 = ml.predict_element(26.96, 184, 2.68, "металл")
print("\nОтвет модели классификации:")
print(f"Элемент: {name} ({conf}%)\n\n")


if result:
    chem_id, name = result
    database.explain_excluded_elements(chem_id)
database.stop()
#Исправить объяснение, если не совпдадает один пункт убрать сравнение по другим полям