from typing import Any
import requests
import pandas as pd
import pickle
import os

# Pandas warningok letiltása oszlopműveletek eredményének visszaírásakor
pd.options.mode.copy_on_write = True


def download_csv_content(url: str) -> str:
    """
    File letöltése, hiba esetén kivételt dob
    :param url: stringként kell megadni az URL-t
    :return: stringként visszaadja az ott talált tartalmat
    """
    request_result = requests.get(url)
    status_code = request_result.status_code
    if status_code != 200:  # HTTP 200 OK
        raise FileNotFoundError(f"Hiba, a URL-ről nem elérhető az adat. Hibakód: {status_code}.")
    return request_result.text


def convert_column_to_number(df: pd.DataFrame, column_name: str) -> pd.DataFrame:
    """
    A Pandas DataFrame megadott oszlopának számmá alakítása
    :param df: Pandas DataFrame, amit át kell alakítani ezzel a függénnyel
    :param column_name: Oszlopnév, aminek az adatait számmá kell alakítani
    :return: Pandas DataFrame az átalakított adatokkal
    """
    df[column_name] = df[column_name].str.replace('\\s+', '', regex=True)  # space-ek eltávolítása
    df[column_name] = df[column_name].str.replace(',', '.')  # vessző pontra cserélése a számokban
    try:
        df[column_name] = df[column_name].astype('int64')  # integerré konvertálás megkísérlése
    except ValueError:
        df[column_name] = df[column_name].astype(
            'float64')  # ha az integerré alakítás nem sikerül, mert . volt benne, floattá alakítás
    # más típusú kivételek nincsenek lekezelve
    return df


def cleanup(df: pd.DataFrame) -> pd.DataFrame:
    """
    Projektfüggő adattisztítás
    :param df: eredeti DataFrame
    :return: tisztított DataFrame
    """
    df = df.iloc[:, :5]  # az első 5 oszlop megtartása, a többi törlése
    df.columns = ["school_year", "school_number", "classroom_number", "number_of_teachers",
                  "number_of_students"]  # az öt oszlop elnevezésének beállítása

    # a DataFrame első oszlopának eredeti adata "1990/1991" szerkezetű, ezért a / jelnél szétvágásra kerül
    # és két új oszlopba kerül year_start és year_end néven a DataFrame végére
    df[["year_start", "year_end"]] = df["school_year"].str.split("/", expand=True)

    for column_name in df.columns[1:]:  # az első oszlop kivételével, ami már nem szükséges, végigmegy az oszlopokon
        df = convert_column_to_number(df, column_name)  # és számmá konvertálja az adatokat

    return df


def get_full_file_name(name, extension, dirname="") -> str:
    """
    A megadott név és kiterjesztés összefűzése
    :param name: A file neve, kiterjesztés nélkül
    :param extension: A file kiterjesztése
    :param dirname: Opcionális könyvtárnév
    :return: Az elkészült név
    """
    full_name = f"{name}.{extension}"  # a megadott filenév-részletek összefűzése
    if dirname:
        full_name = os.path.join(dirname, full_name)  # ha meg van adva a könyvtárnév, eléírja
    return full_name


def save_content_as_csv(df: pd.DataFrame, name: str, extension: str = "csv") -> None:
    """
    A megadott DataFrame egy megadott file-ba kimentése csv formátumban
    :param df: A mentendő DataFrame
    :param name: A file neve, kiterjesztés nélkül
    :param extension: A file kiterjesztése
    """
    full_name = get_full_file_name(name, extension)  # a filenév összeállítása
    df.to_csv(full_name, index=False)  # a tartalom kimentése sorszámok nélkül


def save_content_as_pickle(data: Any, name: str, extension: str = "pickle") -> None:
    """
    A megadott objektum kimentése pickle formátumban.
    Tuple, lista, dictionary és más, összetett adattípusokkal egy file-ba egyszerre több objektum is menthető.
    Működne a DataFrame to_pickle metódusa is, de így általánosabb, nem csak DataFrame lehet a mentett objektum.
    :param data: Tetszőleges, mentendő objektum
    :param name: A file neve, kiterjesztés nélkül
    :param extension: A file kiterjesztése
    """
    full_name = get_full_file_name(name, extension)  # a filenév összeállítása
    with open(full_name, "wb") as f:  # file megnyitása írásra
        pickle.dump(data, f)  # tartalom kimentése


def load_pickle(name: str, extension: str = "pickle") -> Any:
    """
    Betölt egy eltárolt objektumot.
    Több objektum esetén szétvágható a visszaadott, összetett objektum értéke:
    save_content_as_pickle(("str1", "str2"), "filename")
    first_object, second_object = load_pickle("filename")
    # first_object == "str1"
    # second_object == "str2"
    Amennyiben a file nem található, None-nal tér vissza a függvény
    :param name: A file neve, kiterjesztés nélkül
    :param extension: A file kiterjesztése
    :return: A visszaolvasott objektum vagy None
    """
    full_name = get_full_file_name(name, extension)  # a filenév összeállítása
    try:
        with open(full_name, "rb") as f:  # a file megnyitása olvasásra
            return pickle.load(f)  # a tartalom visszaolvasása és visszatérés a tartalommal
    except FileNotFoundError as e:  # nincs ilyen file
        return None


def load_csv(name: str, extension: str = "csv") -> pd.DataFrame | None:
    """
    A megadott csv file tartalmának visszaadása Pandas DataFrame-ként.
    Amennyiben nem létezik a file, a visszatérési érték None lesz.
    :param name: A file neve, kiterjesztés nélkül
    :param extension: A file kiterjesztése
    :return: A visszaolvasott DataFrame vagy None
    """
    full_name = get_full_file_name(name, extension)  # a filenév összeállítása
    try:
        return pd.read_csv(full_name)  # visszatérés a beolvasott táblázattal
    except FileNotFoundError as e:  # ha nem létezik
        return None  # jelezzük None-nal
