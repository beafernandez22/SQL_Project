import pandas as pd

# Función para limpiar y homogeneizar los datos de 2015 y 2016
def clean_happiness_2015_2016(df, year):
    df = df.copy()

# Renombramos columnas originales nombres comunes
#  todos los años del World Happiness Report
    df = df.rename(columns={
        "Country": "country",
        "Happiness Rank": "happiness_rank",
        "Happiness Score": "happiness_score",
        "Economy (GDP per Capita)": "gdp_score",
        "Family": "social_support",
        "Health (Life Expectancy)": "life_expectancy",
        "Freedom": "freedom",
        "Generosity": "generosity",
        "Trust (Government Corruption)": "corruption"
    })

# Seleccionamos solo las columnas que vamos a utilizar en el proyecto
    df = df[[
        "country",
        "happiness_rank",
        "happiness_score",
        "gdp_score",
        "social_support",
        "life_expectancy",
        "freedom",
        "generosity",
        "corruption"
    ]]

 # Añadimos el año porque los CSV originales están separados por año
 # y necesitaremos esta columna cuando unamos todos los datasets
    df["year"] = year

    # Devolvemos el DataFrame limpio
    return df

# Función para limpiar y homogeneizar los datos de 2017
def clean_happiness_2017(df, year):

    df = df.copy()

    # Renombramos las columnas originales de 2017
    # para que tengan los mismos nombres que 2015 y 2016
    df = df.rename(columns={
        "Country": "country",
        "Happiness.Rank": "happiness_rank",
        "Happiness.Score": "happiness_score",
        "Economy..GDP.per.Capita.": "gdp_score",
        "Family": "social_support",
        "Health..Life.Expectancy.": "life_expectancy",
        "Freedom": "freedom",
        "Generosity": "generosity",
        "Trust..Government.Corruption.": "corruption"
    })

    # Seleccionamos las mismas columnas que en los años anteriores
    df = df[[
        "country",
        "happiness_rank",
        "happiness_score",
        "gdp_score",
        "social_support",
        "life_expectancy",
        "freedom",
        "generosity",
        "corruption"
    ]]

    # Añadimos el año correspondiente
    df["year"] = year

    # Devolvemos el DataFrame limpio
    return df

# Función para limpiar y homogeneizar los datos de 2018 y 2019
def clean_happiness_2018_2019(df, year):

    df = df.copy()

    # Renombramos las columnas originales de 2018 y 2019
    # para que tengan los mismos nombres que el resto de años
    df = df.rename(columns={
        "Country or region": "country",
        "Overall rank": "happiness_rank",
        "Score": "happiness_score",
        "GDP per capita": "gdp_score",
        "Social support": "social_support",
        "Healthy life expectancy": "life_expectancy",
        "Freedom to make life choices": "freedom",
        "Generosity": "generosity",
        "Perceptions of corruption": "corruption"
    })

    # Seleccionamos las mismas columnas que en los años anteriores
    df = df[[
        "country",
        "happiness_rank",
        "happiness_score",
        "gdp_score",
        "social_support",
        "life_expectancy",
        "freedom",
        "generosity",
        "corruption"
    ]]

    # Añadimos el año correspondiente
    df["year"] = year

    # Devolvemos el DataFrame limpio
    return df

# Función para limpiar los datos obtenidos de la API del Banco Mundial
def clean_world_bank(df, indicator_name):

    df = df.copy()

    # Extraemos el nombre del país del diccionario de la columna country
    df["country"] = df["country"].apply(lambda x: x["value"])

    # Seleccionamos únicamente las columnas que necesitamos
    df = df[[
        "country",
        "countryiso3code",
        "date",
        "value"
    ]]

    # Renombramos las columnas comunes
    df = df.rename(columns={
        "countryiso3code": "iso3_code",
        "date": "year",
        "value": indicator_name
    })

    # Convertimos el año a número entero
    df["year"] = df["year"].astype(int)

    return df


# Función para limpiar los metadatos de países del Banco Mundial
def clean_world_bank_countries(df):

    # Creamos una copia para no modificar el DataFrame original
    df = df.copy()

    # Extraemos el nombre de la región del diccionario de la columna region
    df["region"] = df["region"].apply(lambda x: x["value"])

    # Extraemos el nivel de ingresos del diccionario de la columna incomeLevel
    df["income_level"] = df["incomeLevel"].apply(lambda x: x["value"])



    # Eliminamos los agregados porque no representan países individuales
    df = df[df["region"] != "Aggregates"]

    # Seleccionamos únicamente las columnas necesarias para el proyecto
    df = df[[
        "id",
        "name",
        "region",
        "income_level"
    ]]

    # Renombramos las columnas para que sean más claras
    df = df.rename(columns={
        "id": "iso3_code",
        "name": "country"
    })

    # Reiniciamos el índice después de eliminar los agregados
    df = df.reset_index(drop=True)

    return df



# Diccionario para adaptar los nombres de países de Happiness
# a los nombres utilizados por el Banco Mundial
country_name_mapping = {
    "Venezuela": "Venezuela, RB",
    "Czech Republic": "Czechia",
    "Slovakia": "Slovak Republic",
    "South Korea": "Korea, Rep.",
    "Russia": "Russian Federation",
    "Hong Kong": "Hong Kong SAR, China",
    "Hong Kong S.A.R., China": "Hong Kong SAR, China",
    "Vietnam": "Viet Nam",
    "Turkey": "Turkiye",
    "Kyrgyzstan": "Kyrgyz Republic",
    "Macedonia": "North Macedonia",
    "Laos": "Lao PDR",
    "Swaziland": "Eswatini",
    "Palestinian Territories": "West Bank and Gaza",
    "Iran": "Iran, Islamic Rep.",
    "Congo (Kinshasa)": "Congo, Dem. Rep.",
    "Egypt": "Egypt, Arab Rep.",
    "Yemen": "Yemen, Rep.",
    "Congo (Brazzaville)": "Congo, Rep.",
    "Ivory Coast": "Cote d'Ivoire",
    "Syria": "Syrian Arab Republic",
    "Trinidad & Tobago": "Trinidad and Tobago",
    "Gambia": "Gambia, The",
    "Puerto Rico": "Puerto Rico (US)",
    "Somalia": "Somalia, Fed. Rep."
}


# Función para adaptar los nombres de países del World Happiness Report
# a los nombres utilizados por el Banco Mundial
def standardize_happiness_countries(df):

    df = df.copy()

    # Sustituimos únicamente los nombres incluidos en nuestro diccionario
    df["country"] = df["country"].replace(country_name_mapping)

    return df