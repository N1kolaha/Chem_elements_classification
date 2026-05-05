import psycopg2
from psycopg2 import Error
from psycopg2 import sql
import traceback
from decimal import Decimal


DB_CONFIG = {
    "dbname": "kursdb",      
    "user": "postgres",
    "password": "admin",
    "host": "127.0.0.1",         
    "port": 5432
}


def printTable(rows, column_names): 
    print(f"Найдено строк в таблице: {len(rows)}\n")
    #print(rows[0][1])
    if rows:
        
        print(" | ".join(column_names))
        print("-" * 80)

        for row in rows:
            print(" | ".join(str(value) for value in row))
    else:
        print("Таблица property пуста.")

conn = None
cur = None

def start():
    global conn, cur
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        print("Подключение успешно")
    except Exception as e:
        print("Ошибка подключения:")
        traceback.print_exc()
        exit(1)

def fetch_table(table_name):
    with conn.cursor() as cur:
        query = sql.SQL("SELECT * FROM {}").format(sql.Identifier(table_name))
        cur.execute(query)
        rows = cur.fetchall()
        column_names = [desc[0] for desc in cur.description]
        return rows, column_names

def count_chem_elements():
    with conn.cursor() as cur:
        cur.execute("SELECT COUNT(*) FROM chem_element")
        return cur.fetchone()[0]

def count_property():
    with conn.cursor() as cur:
        cur.execute("SELECT COUNT(*) FROM property")
        return cur.fetchone()[0]

def add_chem_element(name):
    """
    Добавляет новый химический элемент в таблицу chem_element.

    """
    try:
        with conn.cursor() as cur:
            query = """
                INSERT INTO chem_element (name)
                VALUES (%s)
                ON CONFLICT (name) DO NOTHING
                RETURNING chem_element_id;
                """
            cur.execute(query, (name,))
            
            result = cur.fetchone()
            conn.commit()

            if result:
                new_id = result[0]
                print(f"Добавлен элемент '{name}' с id = {new_id}")
                return new_id
            else:
                print(f"Элемент '{name}' уже существует")
                return None

    except Exception as e:
        print("Ошибка при добавлении элемента:", e)
        conn.rollback()

def delete_chem_element(element_id):
    """
    Удаляет химический элемент из таблицы chem_element по его id.

    """
    try:
        with conn.cursor() as cur:
            query = "DELETE FROM chem_element WHERE chem_element_id = %s;"
            cur.execute(query, (element_id,))
            conn.commit()
            print(f"Элемент с id = {element_id} удалён")
    except Exception as e:
        print("Ошибка при удалении элемента:", e)
        conn.rollback()

def add_property(name):
    """
    Добавляет новое свойство в таблицу property.

    """
    try:
        with conn.cursor() as cur:
            query = "INSERT INTO property (name) VALUES (%s) RETURNING property_id;"
            cur.execute(query, (name,))
            
            result = cur.fetchone()
            conn.commit()

            if result:
                new_id = result[0]
                print(f"Добавлено свойство '{name}' с id = {new_id}")
                return new_id
            else:
                print(f"Свойство '{name}' уже существует")
                return None

    except Exception as e:
        print("Ошибка при добавлении свойства:", e)
        conn.rollback()

def delete_property(property_id):
    """
    Удаляет свойство из таблицы property по его id.

    """
    try:
        with conn.cursor() as cur:
            query = "DELETE FROM property WHERE property_id = %s;"
            cur.execute(query, (property_id,))
            conn.commit()
            print(f"Свойство с id = {property_id} удалено")
    except Exception as e:
        print("Ошибка при удалении свойства:", e)
        conn.rollback()

def add_property_for_element(chem_element_id, property_id):
    """
    Добавляет связь между химическим элементом и свойством.
    """
    try:
        with conn.cursor() as cur:
            query = """
                INSERT INTO property_for_element (chem_element_id, property_id)
                VALUES (%s, %s)
                ON CONFLICT (chem_element_id, property_id) DO NOTHING
                RETURNING property_for_element_id;
            """
            cur.execute(query, (chem_element_id, property_id))
            
            result = cur.fetchone()
            
            conn.commit()

            if result:
                new_id = result[0]
                print(f"Связь добавлена, id={new_id}")
                return new_id
            else:
                print("Такая связь уже существует")
                return None

    except Exception as e:
        print("Ошибка при добавлении связи:", e)
        conn.rollback()

def delete_property_for_element(property_for_element_id):
    """
    Удаляет связь из таблицы property_for_element по её id.
    """
    try:
        with conn.cursor() as cur:
            query = """
                DELETE FROM property_for_element
                WHERE property_for_element_id = %s;
            """
            cur.execute(query, (property_for_element_id,))
            
            conn.commit()
            print(f"Связь с id = {property_for_element_id} удалена")

    except Exception as e:
        print("Ошибка при удалении связи:", e)
        conn.rollback()

def get_elements_properties():
    """
    Возвращает все записи из property_for_element
    + название свойства в последнем столбце.
    """

    try:
        with conn.cursor() as cur:

            query = """
                SELECT 
                    pf.property_for_element_id,
                    pf.chem_element_id,
                    pf.property_id,
                    p.name AS property_name
                FROM property_for_element pf
                JOIN property p 
                  ON pf.property_id = p.property_id
                ORDER BY pf.property_for_element_id;
            """

            cur.execute(query)
            rows = cur.fetchall()

            column_names = [
                "property_for_element_id",
                "chem_element_id",
                "property_id",
                "property_name"
            ]

            return rows, column_names

    except Exception as e:
        print("Ошибка в get_elements_properties:", e)
        return [], []

def add_possible_value(property_id, value):
    """
    Добавляет возможное значение для свойства.
    Если уже существует — возвращает None.
    """

    try:
        with conn.cursor() as cur:

            if isinstance(value, str):
                value_str = value

            elif isinstance(value, (list, tuple)) and len(value) == 2:
                v1, v2 = value

                if not isinstance(v1, (int, float, Decimal)) or not isinstance(v2, (int, float, Decimal)):
                    raise ValueError("Оба значения должны быть числами")

                if v1 >= v2:
                    raise ValueError("Первое число должно быть меньше второго")

                value_str = f"{v1}-{v2}"

            else:
                raise ValueError("value должен быть строкой или парой чисел (min, max)")

            query = """
                INSERT INTO possible_value (property_id, value)
                VALUES (%s, %s)
                ON CONFLICT (property_id, value) DO NOTHING
                RETURNING possible_value_id;
            """

            cur.execute(query, (property_id, value_str))
            result = cur.fetchone()

            conn.commit()

            if result is None:
                print(f"Уже существует: property_id={property_id}, value='{value_str}'")
                return None

            new_id = result[0]

            print(f"Добавлено possible_value: property_id={property_id}, value='{value_str}', id={new_id}")
            return new_id

    except Exception as e:
        print("Ошибка при добавлении possible_value:", e)
        conn.rollback()
        return None

def delete_possible_value(possible_value_id):
    """
    Удаляет значение из таблицы possible_value по его id.
    """
    try:
        with conn.cursor() as cur:
            query = """
                DELETE FROM possible_value
                WHERE possible_value_id = %s;
            """
            cur.execute(query, (possible_value_id,))
            
            conn.commit()

            print(f"Possible value с id = {possible_value_id} удалён")

    except Exception as e:
        print("Ошибка при удалении possible_value:", e)
        conn.rollback()

def add_value_chem_element(property_for_element_id, value):
    """
    Добавляет значение для связки property_for_element
    с проверкой по possible_value.
    """

    try:
        with conn.cursor() as cur:

            cur.execute("""
                SELECT property_id
                FROM property_for_element
                WHERE property_for_element_id = %s;
            """, (property_for_element_id,))

            row = cur.fetchone()
            if not row:
                raise ValueError("property_for_element_id не найден")

            property_id = row[0]

            cur.execute("""
                SELECT value
                FROM possible_value
                WHERE property_id = %s;
            """, (property_id,))

            possible_values = cur.fetchall()

            if not possible_values:
                raise ValueError("Нет possible_value для этого property_id")

            valid = False

            for (pv,) in possible_values:

                if "-" in pv:
                    try:
                        left, right = pv.split("-")
                        if left.isdigit():
                            left = int(left)
                        else:
                            left = Decimal(left)
                        if right.isdigit():
                            right = int(right)
                        else:
                            right = Decimal(right)

                        value_str = str(value)
                        v = Decimal(value)
                        is_int_input = "." not in value_str

                        if isinstance(left, int) and isinstance(right, int) and not is_int_input:
                            print("поймал float")
                            continue

                        if (isinstance(left, Decimal) and isinstance(right, Decimal)) and is_int_input:
                            print("поймал int")
                            continue

                        if left <= v <= right:
                            valid = True
                            break
                    except:
                        continue

                else:
                    if str(value) == pv:
                        valid = True
                        break

            if not valid:
                #raise ValueError(f"Значение '{value}' не входит в допустимые значения")
                return(f"Значение '{value}' не входит в допустимые значения")

            cur.execute("""
                INSERT INTO value_chem_element (property_for_element_id, value)
                VALUES (%s, %s)
                RETURNING value_chem_element_id;
            """, (property_for_element_id, str(value)))

            new_id = cur.fetchone()[0]
            conn.commit()

            print(f"Добавлено value_chem_element id={new_id}")
            return new_id

    except Exception as e:
        print("Ошибка при добавлении value_chem_element:", e)
        conn.rollback()

def patch_value_chem_element(property_for_element_id, value):
    """
    Обновляет значение для связки property_for_element
    с проверкой по possible_value.
    Если записи нет — создаёт новую.
    """

    try:
        with conn.cursor() as cur:

            cur.execute("""
                SELECT property_id
                FROM property_for_element
                WHERE property_for_element_id = %s;
            """, (property_for_element_id,))

            row = cur.fetchone()
            if not row:
                raise ValueError("property_for_element_id не найден")

            property_id = row[0]

            cur.execute("""
                SELECT value
                FROM possible_value
                WHERE property_id = %s;
            """, (property_id,))

            possible_values = cur.fetchall()

            if not possible_values:
                raise ValueError("Нет possible_value для этого property_id")

            valid = False

            for (pv,) in possible_values:

                if "-" in pv:
                    try:
                        left, right = pv.split("-")
                        if left.isdigit():
                            left = int(left)
                        else:
                            left = Decimal(left)
                        if right.isdigit():
                            right = int(right)
                        else:
                            right = Decimal(right)

                        value_str = str(value)
                        v = Decimal(value)
                        is_int_input = "." not in value_str

                        if isinstance(left, int) and isinstance(right, int) and not is_int_input:
                            print("поймал float")
                            continue

                        if (isinstance(left, Decimal) and isinstance(right, Decimal)) and is_int_input:
                            print("поймал int")
                            continue

                        if left <= v <= right:
                            valid = True
                            break
                    except:
                        continue

                else:
                    if str(value) == pv:
                        valid = True
                        break

            if not valid:
                return f"Значение '{value}' не входит в допустимые значения"

            cur.execute("""
                SELECT value_chem_element_id
                FROM value_chem_element
                WHERE property_for_element_id = %s;
            """, (property_for_element_id,))

            existing = cur.fetchone()

            if existing:
                cur.execute("""
                    UPDATE value_chem_element
                    SET value = %s
                    WHERE property_for_element_id = %s
                    RETURNING value_chem_element_id;
                """, (str(value), property_for_element_id))
                
                updated_id = cur.fetchone()[0]
                conn.commit()
                print(f"Обновлено value_chem_element id={updated_id}")
                return updated_id
            else:
                cur.execute("""
                    INSERT INTO value_chem_element (property_for_element_id, value)
                    VALUES (%s, %s)
                    RETURNING value_chem_element_id;
                """, (property_for_element_id, str(value)))

                new_id = cur.fetchone()[0]
                conn.commit()
                print(f"Добавлено value_chem_element id={new_id}")
                return new_id

    except Exception as e:
        print("Ошибка при обновлении value_chem_element:", e)
        conn.rollback()
        return None

def get_value_chem_property_id(property_for_element_id):
    """
    Возвращает значение value из value_chem_element
    по property_for_element_id.
    
    Если значения нет — возвращает None.
    """

    try:
        with conn.cursor() as cur:

            query = """
                SELECT value
                FROM value_chem_element
                WHERE property_for_element_id = %s;
            """

            cur.execute(query, (property_for_element_id,))
            result = cur.fetchone()

            if not result:
                return None

            return result[0]

    except Exception as e:
        print("Ошибка в get_value_chem_property_id:", e)
        return None

def delete_value_chem_element(value_chem_element_id):
    """
    Удаляет запись из value_chem_element по id.
    """
    try:
        with conn.cursor() as cur:
            query = """
                DELETE FROM value_chem_element
                WHERE value_chem_element_id = %s;
            """
            cur.execute(query, (value_chem_element_id,))
            
            conn.commit()

            print(f"value_chem_element с id = {value_chem_element_id} удалён")

    except Exception as e:
        print("Ошибка при удалении value_chem_element:", e)
        conn.rollback()

def find_chem_element(data: dict):
    try:
        if not data:
            print("Пустой словарь")
            return None

        REQUIRED_PROPS = {
            "атомная масса",
            "плотность",
            "радиус атома",
            "тип"
        }

        with conn.cursor() as cur:

            cur.execute("""
                SELECT chem_element_id, name
                FROM chem_element;
            """)
            elements = cur.fetchall()

            valid_elements = []

            for chem_id, name in elements:

                cur.execute("""
                    SELECT p.name, v.value
                    FROM property_for_element pf
                    JOIN property p ON pf.property_id = p.property_id
                    JOIN value_chem_element v 
                      ON pf.property_for_element_id = v.property_for_element_id
                    WHERE pf.chem_element_id = %s;
                """, (chem_id,))

                rows = cur.fetchall()

                element_props = {
                    prop_name.lower(): value for prop_name, value in rows
                }

                valid = True

                for prop_name, input_value in data.items():

                    if input_value is None:
                        continue

                    prop_key = prop_name.lower()

                    if prop_key not in REQUIRED_PROPS:
                        continue

                    if prop_key not in element_props:
                        valid = False
                        break

                    db_value = element_props[prop_key]

                    if str(input_value).replace('.', '', 1).isdigit():
                        try:
                            if abs(float(db_value) - float(input_value)) > 0.01:
                                valid = False
                                break
                        except:
                            valid = False
                            break
                    else:
                        if str(db_value).lower() != str(input_value).lower():
                            valid = False
                            break

                if valid:
                    valid_elements.append((chem_id, name, element_props))

            if not valid_elements:
                print("Совпадений нет")
                return None

            if len(valid_elements) == 1:
                chem_id, name, _ = valid_elements[0]
                print(f"Элемент: {name}")
                return chem_id, name

            scores = []

            for chem_id, name, element_props in valid_elements:

                match_count = 0
                valid = True

                for prop_name, input_value in data.items():

                    if input_value is None:
                        continue

                    prop_key = prop_name.lower()

                    if prop_key not in element_props:
                        continue

                    db_value = element_props[prop_key]

                    if str(input_value).replace('.', '', 1).isdigit():
                        try:
                            if abs(float(db_value) - float(input_value)) <= 0.01:
                                match_count += 1
                            else:
                                valid = False
                        except:
                            valid = False

                    else:
                        if str(db_value).lower() == str(input_value).lower():
                            match_count += 1
                        else:
                            valid = False

                for req in ["атомная масса", "плотность", "радиус атома", "тип"]:
                    if req in data:
                        if req not in element_props:
                            valid = False

                if valid:
                    scores.append((chem_id, name, match_count))

            if not scores:
                print("После уточнения совпадений нет")
                return None

            scores.sort(key=lambda x: x[2], reverse=True)

            best_score = scores[0][2]
            best = [x for x in scores if x[2] == best_score]

            if len(best) != 1:
                print(f"Все еще несколько элементов: {[(b[0], b[1]) for b in best]}")
                return None

            chem_id, name, _ = best[0]

            print(f"Элемент: {name}")
            return chem_id, name

    except Exception as e:
        print("Ошибка:", e)
        return None

def explain_excluded_elements(found_id):
    """
    Объясняет исключения с приоритетом свойства 'Тип'
    и возвращает весь текст результата.
    """

    try:
        output_lines = []  

        with conn.cursor() as cur:

            # свойства найденного элемента
            cur.execute("""
                SELECT p.name, v.value, p.property_id
                FROM property_for_element pf
                JOIN property p ON pf.property_id = p.property_id
                JOIN value_chem_element v 
                  ON pf.property_for_element_id = v.property_for_element_id
                WHERE pf.chem_element_id = %s;
            """, (found_id,))

            found_rows = cur.fetchall()

            if not found_rows:
                msg = "Найденный элемент не имеет свойств"
                print(msg)
                return msg

            found_props = {}
            for prop_name, value, prop_id in found_rows:
                found_props[prop_id] = (prop_name, value)

            # имя найденного элемента
            cur.execute("""
                SELECT name FROM chem_element WHERE chem_element_id = %s;
            """, (found_id,))
            found_name = cur.fetchone()[0]

            # остальные элементы
            cur.execute("""
                SELECT chem_element_id, name
                FROM chem_element
                WHERE chem_element_id != %s;
            """, (found_id,))

            others = cur.fetchall()

            for other_id, other_name in others:

                cur.execute("""
                    SELECT p.property_id, p.name, v.value
                    FROM property_for_element pf
                    JOIN property p ON pf.property_id = p.property_id
                    JOIN value_chem_element v 
                      ON pf.property_for_element_id = v.property_for_element_id
                    WHERE pf.chem_element_id = %s;
                """, (other_id,))

                other_rows = cur.fetchall()

                other_map = {}
                for prop_id, prop_name, value in other_rows:
                    other_map[prop_id] = (prop_name, value)

                # тип первый
                sorted_props = sorted(
                    found_props.items(),
                    key=lambda x: 0 if x[1][0].lower() == "тип" else 1
                )

                for prop_id, (prop_name, found_value) in sorted_props:

                    # нет свойства
                    if prop_id not in other_map:
                        msg = f'Класс <{other_name}> исключен, так как отсутствует свойство <{prop_name}>'
                        print(msg)
                        output_lines.append(msg)
                        break

                    other_value = other_map[prop_id][1]

                    # числовые
                    if str(found_value).replace('.', '', 1).isdigit():
                        try:
                            f1 = float(found_value)
                            f2 = float(other_value)

                            if abs(f1 - f2) > 0.01:
                                msg = (
                                    f'Класс <{other_name}> исключен, так как значение свойства '
                                    f'<{prop_name}> "{other_value}" ≠ “{found_value}”'
                                )
                                print(msg)
                                output_lines.append(msg)
                                break
                        except:
                            continue

                    # строковые
                    else:
                        if str(found_value).lower() != str(other_value).lower():
                            msg = (
                                f'Класс <{other_name}> исключен, так как значение свойства '
                                f'<{prop_name}> "{other_value}" ≠ “{found_value}”'
                            )
                            print(msg)
                            output_lines.append(msg)
                            break

        #итого
        return "\n".join(output_lines)

    except Exception as e:
        print("Ошибка:", e)
        return str(e)

def get_properties_value(chem_element_id):
    """
    Возвращает все свойства и значения химического элемента по его id.
    """

    try:
        with conn.cursor() as cur:

            query = """
                SELECT p.name, v.value
                FROM property_for_element pf
                JOIN property p ON pf.property_id = p.property_id
                JOIN value_chem_element v 
                  ON pf.property_for_element_id = v.property_for_element_id
                WHERE pf.chem_element_id = %s;
            """

            cur.execute(query, (chem_element_id,))
            rows = cur.fetchall()

            if not rows:
                print(f"У элемента id={chem_element_id} нет свойств")
                return {}

            result = {}

            for prop_name, value in rows:
                result[prop_name] = value

            return result

    except Exception as e:
        print("Ошибка в get_properties_value:", e)
        return {}

def get_properties():
    """
    Возвращает словарь:
    property_name -> "Качественный" / "Вещественный"
    """

    try:
        with conn.cursor() as cur:

            cur.execute("""
                SELECT p.property_id, p.name, pv.value
                FROM property p
                LEFT JOIN possible_value pv
                  ON p.property_id = pv.property_id;
            """)

            rows = cur.fetchall()

            if not rows:
                return {}

            result = {}

            # группировка по property
            temp = {}

            for prop_id, prop_name, value in rows:

                if prop_name not in temp:
                    temp[prop_name] = []

                if value is not None:
                    temp[prop_name].append(value)

            for prop_name, values in temp.items():

                is_numeric_range = False
                if not values:
                    result[prop_name] = "Не определён"
                    continue
                for v in values:
                    if isinstance(v, str) and "-" in v:
                        is_numeric_range = True
                        break

                if is_numeric_range:
                    result[prop_name] = "Вещественный"
                else:
                    result[prop_name] = "Качественный"

            return result

    except Exception as e:
        print("Ошибка в get_properties:", e)
        return {}

def get_property_possible(property_id):
    """
    Возвращает все возможные значения свойства по property_id.
    """

    try:
        with conn.cursor() as cur:

            query = """
                SELECT value
                FROM possible_value
                WHERE property_id = %s;
            """

            cur.execute(query, (property_id,))
            rows = cur.fetchall()

            if not rows:
                print(f"Для property_id={property_id} нет возможных значений")
                return []

            result = [value for (value,) in rows]

            return result

    except Exception as e:
        print("Ошибка в get_property_possible:", e)
        return []

def get_chem_element_name(chem_element_id):
    """
    Возвращает название химического элемента по его id.
    Если элемент не найден — возвращает None.
    """

    try:
        with conn.cursor() as cur:

            query = """
                SELECT name
                FROM chem_element
                WHERE chem_element_id = %s;
            """

            cur.execute(query, (chem_element_id,))
            result = cur.fetchone()

            if not result:
                return None

            return result[0]

    except Exception as e:
        print("Ошибка в get_chem_element_name:", e)
        return None

def get_property_name(property_id):
    """
    Возвращает название свойства по property_id.
    """

    try:
        with conn.cursor() as cur:

            query = """
                SELECT name
                FROM property
                WHERE property_id = %s;
            """

            cur.execute(query, (property_id,))
            result = cur.fetchone()

            if not result:
                print(f"Свойство с id={property_id} не найдено")
                return None

            return result[0]

    except Exception as e:
        print("Ошибка в get_property_name:", e)
        return None

def get_unvalued_property_for_element():
    """
    Возвращает все строки из property_for_element,
    для которых НЕТ записей в value_chem_element.
    """

    try:
        with conn.cursor() as cur:

            query = """
                SELECT pf.property_for_element_id,
                       pf.chem_element_id,
                       pf.property_id
                FROM property_for_element pf
                LEFT JOIN value_chem_element v
                  ON pf.property_for_element_id = v.property_for_element_id
                WHERE v.property_for_element_id IS NULL
                ORDER BY pf.property_for_element_id;
            """

            cur.execute(query)
            rows = cur.fetchall()

            column_names = [
                "property_for_element_id",
                "chem_element_id",
                "property_id"
            ]

            return rows, column_names

    except Exception as e:
        print("Ошибка в get_unvalued_property_for_element:", e)
        return [], []

def stop():
    cur.close()
    conn.close()


if __name__ == "__main__":
    start()
   
    print(get_properties())
    #add_property("Цвет")
    print(get_properties())
    #add_value_chem_element(1,40)
    #delete_value_chem_element(104)
    printTable(*fetch_table("property_for_element"))
    printTable(*fetch_table("value_chem_element"))
    rows, cols = get_unvalued_property_for_element()
    print(rows, cols)
    printTable(*fetch_table("possible_value"))
   # printTable(*fetch_table("property"))
    
    stop()

