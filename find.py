def find_chem_element(v1, v2, v3, v4):
    """
    Поиск chem_element по 4 значениям (строгий матч всех значений).
    """

    try:
        values = [str(v1), str(v2), str(v3), str(v4)]

        with conn.cursor() as cur:

            # 1. находим property_for_element_id, которые совпали по ВСЕМ 4 значениям
            cur.execute("""
                SELECT vce.property_for_element_id
                FROM value_chem_element vce
                WHERE vce.value = ANY(%s)
                GROUP BY vce.property_for_element_id
                HAVING COUNT(DISTINCT vce.value) = %s;
            """, (values, len(values)))

            rows = cur.fetchall()

            if not rows:
                print("Совпадений не найдено")
                return None

            property_ids = [r[0] for r in rows]

            # 2. проверяем, что они принадлежат одному chem_element
            cur.execute("""
                SELECT DISTINCT chem_element_id
                FROM property_for_element
                WHERE property_for_element_id = ANY(%s);
            """, (property_ids,))

            chem_ids = [r[0] for r in cur.fetchall()]

            if len(set(chem_ids)) != 1:
                print("Ошибка: значения принадлежат разным chem_element")
                return None

            chem_element_id = chem_ids[0]

            # 3. получаем имя
            cur.execute("""
                SELECT name
                FROM chem_element
                WHERE chem_element_id = %s;
            """, (chem_element_id,))

            name = cur.fetchone()[0]

            print(f"Найден элемент: {name}")
            return chem_element_id, name

    except Exception as e:
        print("Ошибка:", e)
        return None