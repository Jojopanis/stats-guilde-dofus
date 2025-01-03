from taipy.gui import Gui, notify, Icon
import pandas as pd
import plotly.express as px
from unity_classes import fig, possible_classes, fig_total, fig_max, max_craft, max_recolte

def dropdown_pressed(state):
    notify(state, 'info', f'{state.class_selected[0]}')
    state.class_layout['xaxis']['categoryorder'] = state.class_selected[0]

def button_pressed(state):
    print(state.options)
    state.prof_level = max(max(max_craft),max(max_recolte))
    update_radial_range(state,state.prof_level)

def slider_triggered(state):
    update_radial_range(state,state.prof_level)

def update_radial_range(state,upper_bound):
    state.prof_level_layout['polar2']['radialaxis']['range'] = [0,upper_bound]
    state.prof_level_layout['polar']['radialaxis']['range'] = [0,upper_bound]
    
orders = [
    ('array', 'Difficulté des classes'), 
    ('category ascending', 'Ordre alphabétique'),]
class_selected = orders[0]
class_layout = {'xaxis':{'categoryorder':orders[0]}}
prof_level_selected = True
prof_level = 100
prof_level_layout = dict(polar=dict(radialaxis=dict(range=[0,prof_level])),polar2=dict(radialaxis=dict(range=[0,prof_level])))
options = {'data':[dict(showlegend=True),dict(name="test")]}
page = """
# Stats de l'Assaut d'Omi sur Unity

<|layout|columns=1 10em|
<|chart|figure={fig}|layout={class_layout}|>

<|{class_selected}|selector|lov={orders}|mode=radio|on_change=dropdown_pressed|>
|>

<|layout|columns=1 1|
## Nombre de joueurs par métier

## Niveau max de métier dispo

<|chart|figure={fig_total}|>

<|chart|figure={fig_max}|layout={prof_level_layout}|options={options}|>
<|{prof_level}|slider|max=200|on_change=slider_triggered|>
<|Reset|button|on_action=button_pressed|>

|>
"""

if __name__ == '__main__':
    Gui(page).run(use_reloader=True, debug=True)