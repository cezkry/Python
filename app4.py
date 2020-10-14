from os.path import dirname, join

import pandas as pd

from bokeh.io import curdoc
from bokeh.plotting import figure
from bokeh.layouts import column, row
from bokeh.models import (Button, CustomJS, DataTable, ColumnDataSource,
                          NumberFormatter, RangeSlider, TableColumn)
from bokeh.models.widgets import CheckboxGroup


df = pd.read_csv('players_20_csv.csv')

source = ColumnDataSource(data=dict())


def update():
    narodowosc11 = [przycisk1.labels[i] for i in przycisk1.active]
    current0 = df.loc[df['nationality'].isin(narodowosc11)]
    current = current0[(current0['value_eur'] >= slider.value[0]) & (current0['value_eur'] <= slider.value[1])].dropna()
    current2 = current[(current['age'] >= slider2.value[0]) & (current['age'] <= slider2.value[1])].dropna()
    current3 = current2[(current2['height_cm'] >= slider3.value[0]) & (current['height_cm'] <= slider3.value[1])].dropna()
    current4 = current3[(current3['weight_kg'] >= slider4.value[0]) & (current['weight_kg'] <= slider4.value[1])].dropna()
    current5 = current4[(current4['overall'] >= slider5.value[0]) & (current['overall'] <= slider5.value[1])].dropna()
    current6 = current5[(current5['potential'] >= slider6.value[0]) & (current['potential'] <= slider6.value[1])].dropna()
    current7 = current6[(current6['wage_eur'] >= slider7.value[0]) & (current['wage_eur'] <= slider7.value[1])].dropna()
    current8 = current7[(current7['skill_moves'] >= slider8.value[0]) & (current['skill_moves'] <= slider8.value[1])].dropna()
    klub11 = [przycisk2.labels[i] for i in przycisk2.active]
    current9 = current8.loc[current8['club'].isin(klub11)]
    pozycja11 = [przycisk3.labels[i] for i in przycisk3.active]
    current10 = current9.loc[current9['player_positions'].isin(pozycja11)]
    noga11 = [przycisk4.labels[i] for i in przycisk4.active]
    current11 = current10.loc[current10['weak_foot'].isin(noga11)]

    source.data = {
        'short_name' : current11.short_name,
        'value_eur' : current11.value_eur,
        'age' : current11.age,
        'height_cm' : current11.height_cm,
        'weight_kg' : current11.weight_kg,
        'nationality' : current11.nationality,
        'club' : current11.club,
        'overall' : current11.overall,
        'potential' : current11.potential,
        'wage_eur' : current11.wage_eur,
        'player_positions' : current11.player_positions,
        'weak_foot' : current11.weak_foot,
        'skill_moves' : current11.skill_moves
    }


narodowosc1 = list(set(df['nationality']))
narodowosc1.sort()

klub1 = list(set(df['club']))
klub1.sort()

pozycja1 = list(set(df['player_positions']))
pozycja1.sort()

noga1 = list(set(df['weak_foot']))
noga1.sort()

slider = RangeSlider(title="Wartość w EURO", start=0, end=105500000, value=(15500000, 95500000), step=100000, format="0,0")
slider.on_change('value', lambda attr, old, new: update())
slider.on_change('value', lambda attr, old, new: update2())

slider2 = RangeSlider(title="Wiek", start=15, end=50, value=(20, 35), step=1, format="0,0")
slider2.on_change('value', lambda attr, old, new: update())

slider3 = RangeSlider(title="Wzrost", start=150, end=210, value=(165, 185), step=5, format="0,0")
slider3.on_change('value', lambda attr, old, new: update())

slider4 = RangeSlider(title="Waga", start=45, end=120, value=(65, 80), step=5, format="0,0")
slider4.on_change('value', lambda attr, old, new: update())

slider5 = RangeSlider(title="Umiejętności", start=40, end=100, value=(70, 90), step=5, format="0,0")
slider5.on_change('value', lambda attr, old, new: update())

slider6 = RangeSlider(title="Potencjał", start=40, end=100, value=(40, 100), step=5, format="0,0")
slider6.on_change('value', lambda attr, old, new: update())

slider7 = RangeSlider(title="Pensja w EURO", start=0, end=565000, value=(0, 565000), step=10000, format="0,0")
slider7.on_change('value', lambda attr, old, new: update())

slider8 = RangeSlider(title="Drybling", start=1, end=5, value=(1, 5), step=1, format="0,0")
slider8.on_change('value', lambda attr, old, new: update())

przycisk1 = CheckboxGroup(labels = narodowosc1, active = [0,1,2,3,4,5])
przycisk1.on_change('active',lambda attr, old, new: update())

wysw_wsz_club = []
for i in range(698):
    wysw_wsz_club.append(i)

przycisk2 = CheckboxGroup(labels = klub1, active = wysw_wsz_club)
przycisk2.on_change('active',lambda attr, old, new: update())


wysw_wsz_poz = []
for i in range(15):
    wysw_wsz_poz.append(i)

przycisk3 = CheckboxGroup(labels = pozycja1, active = wysw_wsz_poz)
przycisk3.on_change('active',lambda attr, old, new: update())

wysw_noga = []
for i in range(2):
    wysw_noga.append(i)

przycisk4 = CheckboxGroup(labels = noga1, active = wysw_noga)
przycisk4.on_change('active',lambda attr, old, new: update())



button = Button(label="Pobierz tabelę", button_type="success")
button.js_on_click(CustomJS(args=dict(source=source),code=open("download.js").read()))

columns = [
    TableColumn(field="short_name", title="Imie i Nazwisko zawodnika"),
    TableColumn(field="value_eur", title="Wartość w EURO", formatter=NumberFormatter(format="0,0.00")),
    TableColumn(field="age", title="Wiek"),
    TableColumn(field="height_cm", title="Wzrost"),
    TableColumn(field="weight_kg", title="Waga"),
    TableColumn(field="nationality", title="Narodowość"),
    TableColumn(field="club", title="Klub"),
    TableColumn(field="overall", title="Umiejętności"),
    TableColumn(field="potential", title="Potencjał"),
    TableColumn(field="wage_eur", title="Pensja w EURO", formatter=NumberFormatter(format="0,0.00")),
    TableColumn(field="player_positions", title="Pozycja"),
    TableColumn(field="weak_foot", title="Lepsza noga"),
    TableColumn(field="skill_moves", title="Drybling")

]


data_table = DataTable(source=source, columns=columns, width=1100, height=600)

wykres1 = figure(plot_width = 550, plot_height = 450,
                 title = 'Wiek/Wartość',
                 x_axis_label = "Wiek", y_axis_label = "Wartość w EURO")
wykres1.scatter("age","value_eur",size = 15,marker = '*', source = source)

wykres2 = figure(plot_width = 550, plot_height = 450,
                 title = "Wzrost/Waga",
                 x_axis_label = "Wzrost", y_axis_label ="Waga")
wykres2.scatter("height_cm","weight_kg",size = 15,marker = '*', source = source)

wykres3 = figure(plot_width = 550, plot_height = 450,
                 title = "Wzrost/Wartość",
                 x_axis_label = "Wzrost", y_axis_label ="Wartość w EURO")
wykres3.scatter("height_cm","value_eur",size = 15,marker = '*', source = source)

wykres4 = figure(plot_width = 550, plot_height = 450,
                 title = "Umiejętności/Wartość",
                 x_axis_label = "Umiejętności", y_axis_label ="Wartość w EURO")
wykres4.scatter("overall","value_eur",size = 15,marker = '*', source = source)

wykres5 = figure(plot_width = 550, plot_height = 450,
                 title = "Wiek/Umiejętności",
                 x_axis_label = "Wiek", y_axis_label ="Umiejętności")
wykres5.scatter("age","overall",size = 15,marker = '*', source = source)

wykres6 = figure(plot_width = 550, plot_height = 450,
                 title = "Umiejętności/Pensja",
                 x_axis_label = "Umiejętności", y_axis_label ="Pensja")
wykres6.scatter("overall","wage_eur",size = 15,marker = '*', source = source)




curdoc().add_root(row(column(data_table, row(wykres1, wykres2), row(wykres3, wykres4), row(wykres5, wykres6)), column(slider, slider2,slider3,slider4,slider5,slider6,slider7,slider8, button, przycisk4, przycisk3), przycisk1, przycisk2))
curdoc().title = "Export CSV"

update()
