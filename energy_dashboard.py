import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title='Энергия мира', layout='wide')
st.title('Глобальное потребление энергии')

st.markdown('''
Интерактивный дашборд, отображающий потребление энергии по странам, источникам и годам.  
Вы можете сравнивать страны, анализировать структуру потребления и рассматривать потребление на душу населения.
''')

@st.cache_data
def load_data():
    # url = 'https://raw.githubusercontent.com/owid/energy-data/master/owid-energy-data.csv'
    # df = pd.read_csv(url)
    df = pd.read_csv("owid-energy-data.csv")
    df = df[df['year'] >= 1990]
    return df

df = load_data()

# Фильтры 
with st.sidebar:
    st.header('Фильтры')
    countries = sorted(df['country'].dropna().unique())
    selected_countries = st.multiselect('Выберите страну(ы)', countries, default=['Russia', 'United States', 'China'])
    selected_years = st.slider('Выберите диапазон лет', 1990, 2022, (2000, 2022), step=1)

# Источники энергии
energy_sources = {
    'Общее потребление': 'primary_energy_consumption',
    'Солнечная энергия': 'solar_consumption',
    'Ветровая энергия': 'wind_consumption',
    'Уголь': 'coal_consumption',
    'Газ': 'gas_consumption',
    'Ядерная энергия': 'nuclear_consumption',
    'Гидроэнергия': 'hydro_consumption'
}

filtered_df = df[
    (df['country'].isin(selected_countries)) &
    (df['year'].between(*selected_years))
]

# Вкладки 
tabs = st.tabs(list(energy_sources.keys()) + ['На душу населения', 'Структура потребления'])

# Графики по источникам 
for tab, (label, column_name) in zip(tabs[:len(energy_sources)], energy_sources.items()):
    with tab:
        st.subheader(f'{label}')
        fig = px.line(
            filtered_df,
            x='year',
            y=column_name,
            color='country',
            labels={'year': 'Год', column_name: 'TWh', 'country': 'Страна'},
            title=f'{label} с {selected_years[0]} по {selected_years[1]}'
        )
        fig.update_layout(height=500, template='plotly_white')
        st.plotly_chart(fig, use_container_width=True)

# На душу населения
with tabs[-2]:
    st.subheader('Потребление на душу населения')
    df_pp = df[df['year'].between(*selected_years)]
    df_pp['per_capita'] = df_pp['primary_energy_consumption'] / df_pp['population']
    filtered_pp = df_pp[df_pp['country'].isin(selected_countries)]

    fig = px.line(
        filtered_pp,
        x='year',
        y='per_capita',
        color='country',
        labels={'year': 'Год', 'per_capita': 'TWh на человека', 'country': 'Страна'},
        title='Потребление энергии на душу населения'
    )
    fig.update_layout(height=500, template='plotly_white')
    st.plotly_chart(fig, use_container_width=True)

#Структура потребления
with tabs[-1]:
    st.subheader('Структура потребления энергии')
    selected_country = st.selectbox('Выберите страну', selected_countries)
    structure_year = selected_years[1]
    country_data = df[(df['country'] == selected_country) & (df['year'] == structure_year)]

    if not country_data.empty:
        values = [country_data[source].values[0] for source in list(energy_sources.values())[1:]]
        labels = list(energy_sources.keys())[1:]
        fig = px.pie(
            names=labels,
            values=values,
            title=f'Структура потребления энергии в {selected_country} ({structure_year})',
            hole=0.4
        )
        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=False)
    else:
        st.warning('Нет данных для выбранной страны и года.')

# Возобновляемая энергия
st.markdown('---')
st.subheader('Доля солнечной и ветровой энергии')

for country in selected_countries:
    country_data = df[(df['country'] == country) & (df['year'] == selected_years[1])]
    if not country_data.empty:
        total = country_data['primary_energy_consumption'].values[0]
        solar = country_data['solar_consumption'].values[0]
        wind = country_data['wind_consumption'].values[0]
        renewable = solar + wind
        percent = (renewable / total * 100) if total > 0 else 0

        st.markdown(f'В **{country}** в **{selected_years[1]}** году возобновляемые источники составили **{percent:.2f}%** от общего потребления.')

# Карта 
st.markdown('---')
st.subheader('Карта потребления энергии по странам')

map_year = selected_years[1]
map_data = df[df['year'] == map_year][['country', 'iso_code', 'primary_energy_consumption']].dropna()

fig_map = px.choropleth(
    map_data,
    locations='iso_code',
    color='primary_energy_consumption',
    hover_name='country',
    color_continuous_scale='YlOrRd',
    title=f'Общее потребление энергии в {map_year} году',
    labels={'primary_energy_consumption': 'TWh'}
)

fig_map.update_layout(height=600, geo=dict(showframe=False, showcoastlines=True))
st.plotly_chart(fig_map, use_container_width=True)



