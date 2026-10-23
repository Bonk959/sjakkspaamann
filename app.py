import streamlit as st
import joblib
import pandas as pd

beste = joblib.load('modell.joblib')

def lag_features(df):
    X = pd.DataFrame(index=df.index)
    X['rating_diff'] = df['white_rating'] - df['black_rating']
    X['snitt_rating'] = (df['white_rating'] + df['black_rating']) / 2
    X['minutes'] = df['increment_code'].str.split('+').str[0].astype(int)
    X['increment'] = df['increment_code'].str.split('+').str[1].astype(int)
    X['rated'] = df['rated'].astype(int)
    eco = df['opening_eco'].str[0]
    for bokstav in ['A', 'B', 'C', 'D', 'E']:
        X['eco_' + bokstav] = (eco == bokstav).astype(int)
    return X

st.title('Sjakkspåmann')
st.write('Fyll inn informasjon om partiet, så viser modellen sjansen for hvert utfall.')

hvit_rating = st.number_input('Rating hvit', value=1500)
svart_rating = st.number_input('Rating svart', value=1500)
minutter = st.number_input('Minutter per spiller', value=10)
tillegg = st.number_input('Sekunder ekstra per trekk', value=0)
ratet = st.checkbox('Ratet parti', value=True)
aapninger = {'A: Flankeåpninger': 'A', 'B: Halvåpne forsvar': 'B', 'C: Åpne spill': 'C',
             'D: Lukkede spill': 'D', 'E: Indiske forsvar': 'E'}
valg = st.selectbox('Åpning', list(aapninger.keys()), index=2)

if st.button('Spå resultat'):
    df = pd.DataFrame([{'white_rating': hvit_rating, 'black_rating': svart_rating,
        'increment_code': f'{minutter}+{tillegg}', 'rated': ratet, 'opening_eco': aapninger[valg]}])
    p = beste.predict_proba(lag_features(df))[0]
    navn = {'white': 'Hvit vinner', 'draw': 'Remis', 'black': 'Svart vinner'}
    for klasse, sannsynlighet in zip(beste.classes_, p):
        st.write(f'{navn[klasse]}: {sannsynlighet:.1%}')
        st.progress(float(sannsynlighet))
