import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go

data = pd.read_csv('https://docs.google.com/spreadsheets/d/15Y-wZ5ouRcSgHGe8-rls_djYtITZxr2mG6NLnagxBzQ/export?gid=1084524964&format=csv')

possible_classes = ['Iop','Cra','Sacrieur','Eniripsa','Sram','Ouginak','Forgelance','Osamodas','Enutrof','Ecaflip','Steamer','Feca','Huppermage','Zobal','Pandawa','Eliotrope','Sadida','Roublard','Xelor']
class_values = data['Classe'].value_counts()
full_classes = pd.DataFrame({
    'Classe': possible_classes,
    'Total': [class_values.get(classe, 0) for classe in possible_classes]
})

full_classes['Qui?'] = full_classes['Classe'].apply(
    lambda x: data[data['Classe'] == x]['Joueur'].to_list()
)

fig = px.bar(full_classes, x='Classe', y='Total',hover_data={'Classe':False,'Total':False,'Qui?':True}, color = 'Classe')
fig.update_layout(yaxis=dict(nticks=int(full_classes['Total'].max())+1), showlegend=False)

totals = data.count(numeric_only=True)
maximums = data.max(numeric_only=True)
totals.name = 'Total'
maximums.name = 'Maximum'
data_total = pd.concat([data.drop(columns=['Joueur','Classe','Rythme']), totals.to_frame().T])
data_total = pd.concat([data_total, maximums.to_frame().T]).fillna(0)
recolte = ['Paysan','Alchimiste','Bucheron','Mineur','Pecheur']
data_recolte = data_total[data_total.columns.intersection(recolte)]
data_craft = data_total[data_total.columns.difference(recolte)]
labels_recolte = data_recolte.columns.tolist()
count_recolte = [int(x) for x in data_recolte.loc['Total'].values.tolist()]
max_recolte = [int(x) for x in data_recolte.loc['Maximum'].values.tolist()]
labels_craft = data_craft.columns.tolist()
count_craft = [int(x) for x in data_craft.loc['Total'].values.tolist()]
max_craft = [int(x) for x in data_craft.loc['Maximum'].values.tolist()]

fig1_total = px.line_polar(r=count_recolte, theta=labels_recolte, line_close=True)
fig1_max = px.line_polar(r=max_recolte, theta=labels_recolte, line_close=True)
fig2_total = px.line_polar(r=count_craft, theta=labels_craft, line_close=True)
fig2_max = px.line_polar(r=max_craft, theta=labels_craft, line_close=True)

fig_total = make_subplots(rows=1, cols=2, specs=[[{'type': 'polar'}, {'type': 'polar'}]])
fig_max = make_subplots(rows=1, cols=2, specs=[[{'type': 'polar'}, {'type': 'polar'}]])
fig_total.add_trace(fig1_total.data[0], row=1, col=1)
fig_max.add_trace(fig1_max.data[0], row=1, col=1)
fig_total.add_trace(fig2_total.data[0], row=1, col=2)
fig_max.add_trace(fig2_max.data[0], row=1, col=2)
fig_total.update_layout(polar=dict(radialaxis=dict(visible=True, nticks=max(count_recolte)+1)),
                  polar2=dict(radialaxis=dict(visible=True, nticks=max(count_craft)+1)))
fig_max.update_layout(polar=dict(radialaxis=dict(visible=True, nticks=5)),
                  polar2=dict(radialaxis=dict(visible=True, nticks=5)))
fig_total.update_traces(fill='toself')
fig_max.update_traces(fill='toself')