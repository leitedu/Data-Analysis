import pandas as pd
import matplotlib.pyplot as plt

def update_nominations_db(update_file, db_path):
    """Processes daily gas nomination Excel files, cleans inconsistent column names, and updates historical database."""

    # Loads raw Excel sheet
    df = pd.read_excel(update_file, sheet_name='NOMI AE -2', header = 1)
    df.columns.values[2] = 'FECHATOTAL'

    # Filters relevant TOTAL columns
    totals = df.filter(like='TOTAL', axis=1).copy()
    totals = totals.drop(columns=totals.filter(regex='REASIGNACION|SIN GAS COMBUSTIBLE').columns)

    # Cleans and standardize column names
    substitutions = ['TOTAL', 'FINAL', 'CON GAS COMBUSTIBLE', 'CON COMBUSTIBLE', '(', ')']
    for term in substitutions:
        totals.columns = totals.columns.str.replace(term, '')

    # Strips whitespaces
    totals.columns = totals.columns.str.strip()

    # Drops second column (raw total without fuel gas) & rename available total
    totals.drop(columns=[totals.columns[1]], inplace=True)
    totals.rename(columns={totals.columns[1]: 'PRODUÇÃO TOTAL DISPONÍVEL'}, inplace=True)

    # Removes empty rows
    totals.dropna(subset=totals.columns[1], inplace=True)

    # Consolidates with historical Database
    if db_path.exists():
        db = pd.read_excel(db_path)
        db = pd.concat([db, totals], ignore_index=True).drop_duplicates(subset=['FECHA'], keep='last')
    else:
        db = totals.copy()

    db.to_excel(db_path, index=False)

    return db

def daily_nominations_chart(db, output_graph):
    '''Generates summary chart of last 7 days nominations volumes'''

    # Extracts last 7 days summary table and format numbers using .map()
    table = db.tail(7).copy()
    table.iloc[:, 1:] = table.iloc[:, 1:].map('{:,.2f}'.format)
    table['FECHA'] = pd.to_datetime(table['FECHA']).dt.normalize()

    # Generates Stackplot for Nomination in Mutun point (Entry in Brazilian gas transport system from Bolivia)
    colunas_mutun = ['FECHA'] + [col for col in db.columns if 'Mutun' in col] # Selects date (fecha in spanish) and columns with 'Mutun'
    table_mutun = db[colunas_mutun].copy()
    table_mutun = table_mutun.drop(columns=table_mutun.filter(regex='BRASIL').columns) # Removes contract named "BRASIL"

    # Renames columns to short names
    shorter_names = ['DATE'] + [col.split()[0] for col in table_mutun.columns[1:]]
    table_mutun.columns = shorter_names
    table_mutun['DATE'] = pd.to_datetime(table_mutun['DATE'])

    # Plot
    data_cols = [col for col in table_mutun.columns if col != 'DATE']
    plt.figure(figsize=(15, 8), dpi=120)
    plt.stackplot(table_mutun['DATE'], data_cols.values.T.tolist(),
                    labels=data_cols.columns.tolist())
    plt.title('Mutun nominations', fontsize=20 ,fontweight="bold")
    plt.legend(loc='upper left')
    plt.ylabel('Volume - MMm³', fontsize=14)
    plt.tight_layout()
    plt.savefig(output_graph)
    plt.close()


# File paths (Placeholders for public showcase)
UPDATE_FILE = 'data/sample_daily_update.xlsx'  # Daily nominations received via email
DB_PATH = 'data/nominations_history.xlsx'       # Historical nominations database
OUTPUT_GRAPH = 'outputs/daily_chart.png'         # Generated output chart

if __name__ == "__main__":

    db = update_nominations_db(UPDATE_FILE, DB_PATH)

    daily_nominations_chart(db, OUTPUT_GRAPH)
