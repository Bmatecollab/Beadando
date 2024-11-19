import matplotlib.pyplot as plt


def go_max():
    """
    A plt.show() előtt meghívva maximalizálja a megnyíló grafikont.
    A matplotlibnek tobb grafikai backendje van, ezekben más-más módon lehet elérni a kívánt hatást.
    Ha az egyik backend megfelelő attribútuma hiányzik, átlép a következőre.
    :return:
    """
    fig_manager = plt.get_current_fig_manager()  # elkéri a figure managert

    try:
        # TkAgg backend
        fig_manager.window.state('zoomed')  # megpróbálja maximalizálni a megnyíló ablakot
    except AttributeError:
        try:
            # Qt backend
            fig_manager.window.showMaximized()  # megpróbálja másképp maximalizálni a megnyíló ablakot
        except AttributeError:
            pass  # ez nem jött be, marad az eredeti, majd a felhasználó megnyitja nagyban, ha szeretné


def set_diagram_labels(x_label="", y_label="", title="") -> None:
    """
    A label-ek és a title-k beállítása, ha meg vannak adva
    :param x_label: x tengely felirata
    :param y_label: y tengely felirata
    :param title: a diagram címsora
    """
    if title:
        plt.title(title)  # title beállítása, ha nem üres
    if x_label:
        plt.xlabel(x_label)  # x tengely feliratának beállítása, ha nem üres
    if y_label:
        plt.ylabel(y_label)  # y tengely feliratának beállítása, ha nem üres


def show_line_diagram(x_values, y_columns, colors=None, x_label="", y_label="", title="") -> None:
    """
    Vonaldiagram létrehozása és kirajzolása
    :param x_values: x tengely értékei (pl. 1991)
    :param y_columns: y tengely értékei, egyszerre több is (pl. 1991-ben hány diák volt, hány tanár volt, hány osztályterem volt)
    :param colors: opcionális lista a színek neveivel, ezek sorban használhatóak, ha a lista ki van töltve
    :param x_label: x tengely felirata
    :param y_label: y tengely felirata
    :param title: opcionálisan a diagram címsora
    """
    if colors is None:  # ha colors lista nincs kitöltve, akkor kap egy üres lista default értéket
        colors = []
    num_colors = len(colors)  # színek száma
    plt.figure(figsize=(10, 5))  # diagram létrehozása
    for idx, y_column_name in enumerate(
            y_columns):  # az y oszlopokon végigiterál és az indexeket és az oszlopneveket elkéri
        y_values = y_columns[y_column_name]  # y_values nevű változóba belerakja a tényleges értékeket
        if num_colors > 0:  # ha van színlista, akkor onnan veszi a következő színt
            plt.plot(x_values, y_values, marker='o', linestyle='-', color=colors[idx % num_colors],
                     label=y_column_name)  # kirajzolja a diagramot a következő megadott színnel
        else:
            plt.plot(x_values, y_values, marker='o', linestyle='-',
                     label=y_column_name)  # kirajzolja a diagramot a következő default színnel
    if not title and x_label and y_label:  # ha nincs megadva title, de az x és y label igen, akkor abból egy alapértelmezett title beállítása
        title = f'Vonaldiagram: {x_label} vs {y_label}'
    set_diagram_labels(x_label, y_label, title)  # label-ket beállító függvény meghívása
    plt.grid(True)  # hálós megjelenítés bekapcsolása
    plt.legend()  # jelmagyarázat beállítása, a ponthalmaz neve
    go_max()  # maximalizálja a megnyíló ablakot
    plt.show()  # megjeleníti a diagramot, és megállítja a program futását amíg az ablak bezárásra nem kerül


def show_multiline_diagram(x_values, y_columns, x_label="") -> None:
    """
    Több vonaldiagram létrehozása és kirajzolása egymás alá
    :param x_values: x tengely értékei (pl. 1991)
    :param y_columns: y tengely értékei, egyszerre több is (pl. 1991-ben hány diák volt, hány tanár volt, hány osztályterem volt)
    :param x_label: x tengely felirata
    :param y_label: y tengely felirata
    :param title: opcionálisan a diagram címsora
    """
    fig_row_count = y_columns.shape[1]  # a pandas oszlopainak (diagram sorainak és vonalainak) a száma
    fig, axs = plt.subplots(ncols=1, nrows=fig_row_count, figsize=(10, 5), layout='constrained')  # diagram létrehozása

    # az y oszlopokon végigiterál és az indexeket és az oszlopneveket elkéri
    for idx, y_column_name in enumerate(y_columns):
        current_axis = axs[idx]
        # y_values nevű változóba belerakja a tényleges értékeket
        y_values = y_columns[y_column_name]
        # kirajzolja a diagramot a következő default színnel
        current_axis.plot(x_values, y_values, marker='o', linestyle='-', label=y_column_name)
        y_label = y_column_name
        title = f'Vonaldiagram: {x_label} vs {y_label}'
        current_axis.set_xlabel(x_label)
        current_axis.set_ylabel(y_label)
        current_axis.set_title(title)
        current_axis.grid(True)  # hálós megjelenítés bekapcsolása
        current_axis.legend()  # jelmagyarázat beállítása, a ponthalmaz neve

    go_max()  # maximalizálja a megnyíló ablakot
    plt.show()  # megjeleníti a diagramot, és megállítja a program futását amíg az ablak bezárásra nem kerül


def show_scatter_diagram(x_values, y_values, x_label="", y_label="", title="", swap_x=False) -> None:
    """
    Pontdiagram létrehozása és kirajzolása
    :param x_values: x tengely értékei (pl. 1991)
    :param y_values: y tengely értékei (pl. 1991-ben 1124098 diák volt)
    :param x_label: x tengely felirata
    :param y_label: y tengely felirata
    :param title: opcionálisan a diagram címsora
    :param swap_x: x tengely számozásának tükrözése
    """
    fig = plt.figure(figsize=(10, 5))  # új diagram készítése 10 a mérete vízszintes és 5 a függőleges irányban

    # scatter plot készítése, az első két paraméter az x és a hozzá tartozó y, a marker x-ekkel jelöl, a label pedig megadja, hogy milyen címke tartozik az adott ponthalmazhoz
    plt.scatter(x_values, y_values, marker='x', label=y_label)

    if not title and x_label and y_label:  # ha nincs megadva title, de az x és y label igen, akkor abból egy alapértelmezett title beállítása
        title = f'Pontdiagram: {x_label} vs {y_label}'

    if swap_x:
        fig.get_axes()[0].invert_xaxis()  # x tengely megfordítása ha arra van szükség
    set_diagram_labels(x_label, y_label, title)  # label-ket beállító függvény meghívása
    plt.grid(True)  # hálós megjelenítés bekapcsolása
    plt.legend()  # jelmagyarázat beállítása, a ponthalmaz neve
    go_max()  # maximalizálja a megnyíló ablakot
    plt.show()  # megjeleníti a diagramot, és megállítja a program futását amíg az ablak bezárásra nem kerül


def show_mixed_diagram(x_values, y_columns, title, labels, colors) -> None:
    """
    A vonal- és pontdiagramot egyszerre rajzolja ki, de külön tengelyekkel a szemléltetés kedvéért
    :param x_values: x tengely értékei (pl. 1991)
    :param y_columns: y tengely értékei, egyszerre több is (pl. 1991-ben hány diák volt, hány tanár volt, hány osztályterem volt)
    :param title: a diagram címsora
    :param labels: tengelyek feliratának listája
    :param colors: lista a színek neveivel, ezek sorban használhatóak
    """
    num_colors = len(colors)  # színek száma
    fig, ax1 = plt.subplots()  # több diagram egy ábrán való megjelenítése
    ax2 = ax1.twinx()  # közös x tengely, külön y tengely
    axes = [ax1, ax2]  # egy listában az y tengelyek
    for ax, label, color in zip(axes, labels, colors[
                                              ::2]):  # a ciklus végigmegy a tengelyeken, a hozzá tartozó címkéken, és a színeken
        ax.set_ylabel(label, color=color)  # címke és szín beállítása, így a számok is színesek
        ax.tick_params(axis='y', labelcolor=color)  # a label színének a beállítása
    active_axis = ax1  # az aktív tengely megadása
    for idx, y_column_name in enumerate(
            y_columns):  # az y oszlopokon végig iterál és az indexeket és az oszlopneveket elkéri
        if idx >= y_columns.shape[1] // 2:  # a felénél tengelyt vált
            active_axis = ax2  # az új aktív tengely megadása
        y_values = y_columns[y_column_name]  # y_values nevű változóba belerakja a tényleges értékeket
        if idx % 2 == 0:  # a párosadik diagramok pontdiagramok
            active_axis.scatter(x_values, y_values, marker='x', color=colors[idx % num_colors],
                                label=y_column_name)  # az ábrához a pontdiagram hozzáadása
        else:  # a páratlanadik diagramok pedig a hozzájuk tartozó vonaldiagramok
            active_axis.plot(x_values, y_values, linestyle='-', color=colors[idx % num_colors],
                             label=y_column_name)  # az ábrához a vonaldiagram hozzáadása
        active_axis.set_label(y_column_name)
        active_axis.grid(True)  # hálós megjelenítés bekapcsolása

    ax1.legend(loc='lower left')  # jelmagyarázat beállítása a két sarokba
    ax2.legend(loc='upper right')

    plt.title(title)  # cím (title) beállítása
    go_max()  # maximalizálja a megnyíló ablakot
    plt.show()  # megjeleníti a diagramot, és megállítja a program futását amíg az ablak bezárásra nem kerül
