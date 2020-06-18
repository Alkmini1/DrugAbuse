#tabula η βιβλιοθήκη που διαβάζει από το PDF τον πίνακα
import tabula
#βοηθητικές συναρτήσεις για διαχείριση αρχείων στο δίσκο
import os
import pandas as pd
import matplotlib.pyplot as plt

States=['Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado', 'Connecticut', 'Delaware', 'Florida',
        'Georgia', 'Hawaii', 'Idaho', 'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Kentucky','Louisiana', 'Maine',
        'Maryland', 'Massachusetts', 'Michigan', 'Midwest', 'Minnesota', 'Mississippi', 'Missouri', 'Montana',
        'Nebraska', 'Nevada', 'New Hampshire', 'New Jersey', 'New Mexico', 'New York', 'North Carolina', 'North Dakota',
        'Ohio', 'Oklahoma', 'Oregon', 'Pennsylvania', 'Rhode Island', 'South Carolina', 'South Dakota', 'Tennessee',
        'Texas', 'Utah', 'Vermont', 'Virginia', 'Washington', 'West Virginia', 'Wisconsin', 'Wyoming']

pathOfPDF = './StatesPDF/'
pathOfCSV = './StatesCSV/'

isDir = os.path.isdir(pathOfCSV)
if not isDir:
    os.mkdir(pathOfCSV)

#λίστα από dataframe όλων τψν πολιτειών
listOfDataFrames = []

for state in States:
    stateFile = state.replace(' ', '')
    if not isDir:
        #διάβασε το pdf αρχείο για κάθε πολιτεία και σώσε το σε μορφή csv για να είναι πολύ γρήγορη η πρόσβαση στα δεδομένα
        #συνθέτουμε το αρχείο για να διαβάσει το pdf κάθε πολιτείας
        tabula.convert_into(pathOfPDF + 'NSDUHsae' + stateFile + '2017.pdf', pathOfCSV + stateFile + '.csv', output_format="csv", pages='2')
    #διάβασε απο τα csv που δημιουργούνται τα δεδομένα και σώσε τα σε dataframe
    #και βάλτο στην λίστα με όλες τις πολιτείες
    df = pd.read_csv(pathOfCSV + stateFile + ".csv")
    #φροντίζουμε να μετατρέψουμε τα δεδομένα σε αριθμητικά αντικαθιστόντας ειδικούς συμβολισμύς
    #όπως για παράδειγμα το "--" σαν μη διαθέσιμο δεδομένο(NaN)"
    df['12+'] = df['12+'].str.replace('--', "NaN", regex=False).astype(float)
    df['12-17'] = df['12-17'].str.replace('--', "NaN", regex=False).astype(float)
    df['18-25'] = df['18-25'].str.replace('--', "NaN", regex=False).astype(float)
    df['26+'] = df['26+'].str.replace('--', "NaN", regex=False).astype(float)
    df['18+'] = df['18+'].str.replace('--', "NaN", regex=False).astype(float)
    #βάλε το dataframe στην λίστα
    listOfDataFrames.append(df)

measures = ["Past Month Alcohol Use", "Past Year Marijuana Use", "Past Year Heroin Use",
            "Past Month Cigarette Use", "Past Year Cocaine Use"]

measureIndex = 3 # από 0 μέχρι 4

#βάζουμε σε ένα dataframe όλες τις πολιτείες για την συγκεκριμένη κατάχρηση
measure_use = {'state':[], '12+':[], '12-17':[], '18-25':[], '26+':[], '18+':[]}
for i, state in enumerate(States):
    y = listOfDataFrames[i][listOfDataFrames[i]['Measure']==measures[measureIndex]].values
    measure_use['state'].append(state)
    measure_use['12+'].append(y[0][1])
    measure_use['12-17'].append(y[0][2])
    measure_use['18-25'].append(y[0][3])
    measure_use['26+'].append(y[0][4])
    measure_use['18+'].append(y[0][5])

#φτιάχουμε εδώ το dataframe
measure_use_per_state_df = pd.DataFrame(measure_use)

#απεικόνιση των συνηθέστερων ηλικιακών ομάδων σε μορφή bar
ax = measure_use_per_state_df.plot(x="state", y="12-17", kind="bar", color="C1")
measure_use_per_state_df.plot(x="state", y="18-25", kind="bar", ax = ax, color="C2")
measure_use_per_state_df.plot(x="state", y="26+", kind="bar", ax=ax, color="C3")
plt.ylabel("% " + measures[measureIndex])

plt.show()

#σώσε τα δεδομένα σε πίνακα για να φορτωθούν στον χάρτη
#measure_use_per_state_df.to_csv("marijuanaUse.csv", index=False)