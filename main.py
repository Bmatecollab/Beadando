# importok
from io import StringIO
import pandas as pd

import diagrams
import ksh_data
import models

# Menü jobb felső sarkából
# forrás: https://www.ksh.hu/stadat_files/okt/hu/okt0008.html
URL = "https://www.ksh.hu/stadat_files/okt/hu/okt0008.csv"
FUTURE_YEARS = 10  # konstans a lineáris modellhez, az exrapolált évek száma
SAVE_FILE_NAME = "school"


def load_data() -> pd.DataFrame:
    """
    Korábbról elmentett, tisztított adat betöltése. Ennek hiányában nyers adatok letöltése és tisztítása.
    :return: A tisztított DataFrame
    """
    df = ksh_data.load_csv(SAVE_FILE_NAME)
    if df is None:
        str_content = ""  # a változó inicializálása
        try:
            str_content = ksh_data.download_csv_content(URL)  # az adat letöltése és az str_contentbe való lementése
        except FileNotFoundError as e:  # hibakezelés
            print("Error: ", e)
            exit(1)

        # string átkonvertálása fájllá, a separator beállítása ;-re, és mivel a csv első sora nem a headert tartalmazza,
        # egy sort át kell ugrani, így a második sor lesz a header
        df = pd.read_csv(StringIO(str_content), sep=";", header=1)
        df = ksh_data.cleanup(df)  # az adattisztító függvény, azaz a cleanup() meghívása
        ksh_data.save_content_as_csv(df, SAVE_FILE_NAME)  # adat kimentése a következő futáshoz
    return df.reset_index(drop=True)  # adatok visszaadása, friss sorszámokkal


if __name__ == '__main__':
    data = load_data()

    print(data.head(15))  # első 15 sor kiírása, hogy látszódjon, hogy milyen adatok vannak a DataFrameben
    columns_needed = ["number_of_students", "number_of_teachers", "school_number",
                      "classroom_number"]  # oszlopok kiválasztása a vonaldiagramhoz
    print(data[
              columns_needed].describe())  # statisztika készítése a kiválasztott oszlopokról (átlag, min, max, medián, 25 és 75%-os percentilis), szórás
    diagrams.show_line_diagram(data["year_start"], data[columns_needed], x_label="Tanév kezdete",
                               y_label="Értékek")  # vonaldiagram megjelenítése
    diagrams.show_multiline_diagram(data["year_start"], data[columns_needed],
                                    x_label="Tanév kezdete")  # vonaldiagram megjelenítése
    # összefüggés a diákok és a tanárok száma között pontdiagramon
    diagrams.show_scatter_diagram(data["number_of_students"], data["number_of_teachers"], "Diákok", "Tanárok")
    # összefüggés a diákok és a tanárok száma között pontdiagramon, valamiért megfordítva
    diagrams.show_scatter_diagram(data["number_of_students"], data["number_of_teachers"], "Diákok",
                                  "Tanárok", swap_x=True)
    diagrams.show_scatter_diagram(data["school_number"], data["number_of_teachers"], "Iskolák",
                                  "Tanárok")  # összefüggés az iskolák és a tanárok száma között pontdiagramon
    diagrams.show_scatter_diagram(data["school_number"], data["number_of_students"], "Iskolák",
                                  "Diákok")  # összefüggés az iskolák és a diákok száma között pontdiagramon

    all_years_with_future = list(range(min(data["year_start"]), max(
        data["year_start"]) + FUTURE_YEARS))  # a múltra és a jövőre vonatkozó évek listája

    student_model = models.create_linear_model(data, "year_start",
                                               "number_of_students")  # egy egyenes illesztése arra, hogy melyik évben hány diák tanult
    student_predicted = student_model.predict(
        [[xx] for xx in all_years_with_future])  # a modell szerint melyik évben hány diák tanult
    student_real_and_predicted = list(data["number_of_students"])  # múltbeli valós adatok változóba mentése
    student_real_and_predicted += list(student_predicted[
                                       len(student_real_and_predicted):])  # összefűzi a múltbeli valós adatokat a jövőre vonatkozó prediktált adatokkal

    teacher_model = models.create_linear_model(data, "year_start",
                                               "number_of_teachers")  # egy egyenes illesztése arra, hogy melyik évben hány tanár tanított
    teacher_predicted = teacher_model.predict(
        [[xx] for xx in all_years_with_future])  # a modell szerint melyik évben hány tanár tanított
    teacher_real_and_predicted = list(data["number_of_teachers"])  # múltbeli valós adatok változóba mentése
    teacher_real_and_predicted += list(teacher_predicted[
                                       len(teacher_real_and_predicted):])  # összefűzi a múltbeli valós adatokat a jövőre vonatkozó prediktált adatokkal

    diagrams.show_scatter_diagram(data["year_start"], data["number_of_students"], "Év",
                                  "Diákok")  # összefüggés az év és a diákok száma között pontdiagramon
    diagrams.show_scatter_diagram(data["year_start"], data["number_of_teachers"], "Év",
                                  "Tanárok")  # összefüggés az év és a tanárok száma között pontdiagramon

    # új DataFrame létrehozása, amiben benne vannak a már eltelt és a közeljövő évszámai, a lineáris modellek, és a valós adatok
    data_pred = pd.DataFrame({"year_start": all_years_with_future,  # évszámok
                              "student_predicted": student_predicted,
                              # diákok számára vonatkozó lineáris modell értékei
                              "student_real_and_predicted": student_real_and_predicted,
                              # diákok valós száma, kiegészítve a jövőre vonatkozó modell adataival
                              "teacher_predicted": teacher_predicted,
                              # tanárok számára vonatkozó lineáris modell értékei
                              "teacher_real_and_predicted": teacher_real_and_predicted})  # tanárok valós száma, kiegészítve a jövőre vonatkozó modell adataival

    # kevert diagram megjelenítése az új DataFrame-mel
    # a diákok száma jelentősen meghaladja a tanárokét, emiatt a kéttengelyes megjelenítés sokkal szemléletesebb
    # a diákok adatai a kék, bal tengelyhez tartoznak, a valós számuk kék X, a lineáris pedig világoskék vonal
    # a tanárok a piros, jobb tengelyhez tartoznak, valós számuk piros X, a lineáris modell narancssárga vonal
    diagrams.show_mixed_diagram(data_pred["year_start"], data_pred[[
        "student_real_and_predicted", "student_predicted",
        "teacher_real_and_predicted", "teacher_predicted"
    ]], "Diákok és tanárok száma", ["diákok", "tanárok"], colors=["blue", "lightblue", "red", "orange"])

    seed_1_error = models.calculate_linear_accuracy(data, "year_start", "number_of_teachers", 1)
    print(f"Tanulók adatán 1-es seednél a lineáris modell hibája {seed_1_error: .2f}")
    average_error = models.calculate_multiple_models(data, "year_start", "number_of_teachers")
    print(f"Tanulók adatán sok seednél a lineáris modellek átlagos hibája {average_error: .2f}")
