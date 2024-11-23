import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.dates as mdates

# Feladatok és időtartamok definiálása
tasks = [
    {"Task": "Projekt tervezés", "Start": "2024-11-01", "End": "2024-11-07"},
    {"Task": "Adatok letöltése és adattisztítás", "Start": "2024-11-03", "End": "2024-11-07"},
    {"Task": "Vizualizációk készítése", "Start": "2024-11-08", "End": "2024-11-14"},
    {"Task": "Regressziós modellek fejlesztése", "Start": "2024-11-15", "End": "2024-11-22"},
    {"Task": "Prezentáció és zárás", "Start": "2024-11-23", "End": "2024-11-30"}
]

# DataFrame létrehozása
df = pd.DataFrame(tasks)
df["Start"] = pd.to_datetime(df["Start"])
df["End"] = pd.to_datetime(df["End"])
df["Duration"] = (df["End"] - df["Start"]).dt.days

# Konvertálás matplotlib által kezelt dátumformátumba
df["Start_num"] = mdates.date2num(df["Start"])
df["End_num"] = mdates.date2num(df["End"])

# Gantt-diagram készítése
fig, ax = plt.subplots(figsize=(10, 6))

for i, task in df.iterrows():
    ax.barh(task["Task"], task["Duration"], left=task["Start_num"], color="skyblue")

# X-tengely beállításai
ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
ax.xaxis.set_major_locator(mdates.DayLocator(interval=5))
plt.xticks(rotation=45)
ax.invert_yaxis()
ax.set_title("Programozás alapjai beadandó", fontsize=14)
ax.set_xlabel("Dátumok")
ax.set_ylabel("Feladatok")
plt.grid(axis="x", linestyle="--", alpha=0.7)
plt.tight_layout()

# Gantt-diagram mentése PDF formátumban
plt.savefig("Projekt_Gantt_Diagram_2024.pdf", format="pdf")
plt.show()
