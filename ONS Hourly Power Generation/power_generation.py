from datetime import datetime
from pathlib import Path
import pandas as pd

def process_ons_generation(
    cegs: list, 
    output_dir: str = "./generation", 
    start_year: int = 2021, 
    start_month: int = 1,
    end_year: int = datetime.today().year,
    end_month: int = datetime.today().month,
    output_name: str = 'generation_database.csv'
):
    """
    Ingests and aggregates hourly power generation data from ONS open data,
    filters by specific power plant codes (CEG), and builds a consolidated time-series.
    """
    base_path = Path(output_dir)
    raw_folder = base_path / "ons_historical_data"
    raw_folder.mkdir(parents=True, exist_ok=True)

    df_list = []
    errors = [] #Saves the name of any file that results error

    # Iterates through requested years and months
    for year in range(start_year, end_year + 1):

        if year <= 2021:
            file_name = f"GERACAO_USINA_{year}.csv"
            local_file = raw_folder / file_name
            url = f"https://ons-aws-prod-opendata.s3.amazonaws.com/dataset/geracao_usina_2_ho/GERACAO_USINA-2_{year}.csv"

            df_list, errors = scraper(local_file, file_name, url, cegs, df_list, errors) # Scrapes generation on database
            
        else:
            m_start = start_month if year == start_year else 1
            m_end = end_month if year == end_year else 12

            for month in range(m_start, m_end + 1):
                file_name = f"GERACAO_USINA_{year}_{month:02d}.csv"
                local_file = raw_folder / file_name
                url = f"https://ons-aws-prod-opendata.s3.amazonaws.com/dataset/geracao_usina_2_ho/GERACAO_USINA-2_{year}_{month:02d}.csv"

                df_list, errors = scraper(local_file, file_name, url, cegs, df_list, errors) # Scrapes generation on database

    # Saves errors list if any is found:
    if len(errors) > 0:
        with open(base_path / 'errors.txt', "w", encoding="utf-8") as file:
            file.write("\n".join(errors))

    # Concatenates and finalize time series
    if df_list:
        final_df = pd.concat(df_list, axis=0, ignore_index=True)
        final_df = final_df.groupby('din_instante', as_index=False).mean()

        # Generates date and hour columns from din_instante col, which contains datetime values stored as strings, and converts it to datetime
        final_df['din_instante'] = pd.to_datetime(final_df['din_instante'])
        final_df['Date'] = final_df['din_instante'].dt.date
        final_df['Hour'] = final_df['din_instante'].dt.time

        # Reordering columns
        reindex = ['din_instante', 'Date', 'Hour'] + cegs
        final_df = final_df.reindex(reindex, axis=1)

        # Saves final database
        output_file = base_path / f"{output_name}.xlsx"
        final_df.to_excel(output_file, index=False)
        print(f"✅ Success! File saved to {output_file}")
        return final_df
    else:
        print("❌ No data found for the selected plants and timeframe.")
        return pd.DataFrame()
  

def scraper(local_file, file_name, url, cegs, df_list, errors):
    """
    Verifies if the database file for the given period is already downloaded from ONS and downloads it if necessary.
    Reads the file, extracts data for the power plants corresponding to the supplied CEG codes, and appends it to the main dataset.
    Registers errors in the error list if any exception occurs during the process.
    """
    try:
        # Downloads file from ONS site using Playwright
        if not local_file.exists():
            print(f"📥 Downloading ONS data for {file_name}...")
            
            from playwright.sync_api import sync_playwright
            
            with sync_playwright() as p:
                browser = p.firefox.launch()
                page = browser.new_page()
                
                # Expects the download to start when hitting the URL (60s timeout)
                with page.expect_download(timeout=120000) as download_info:
                    try:
                        page.goto(url)
                    except Exception:
                        # Direct download links often throw a navigation error, we just pass
                        pass
                
                # Saves the downloaded file to our specific cache directory
                download = download_info.value
                download.save_as(local_file)
                
                browser.close()
                
            print(f"✅ Download successful for {file_name}!")
        else:
            print(f"📂 Reading cached file for {file_name}...")
        
        # Loads the file (either just downloaded or cached) into Pandas
        base = pd.read_csv(local_file, delimiter=';')

        # Filter target power plants (CEGs)
        filtered = base[base['ceg'].isin(cegs)][['din_instante', 'ceg', 'val_geracao']]

        if not filtered.empty:
            # Aggregate & Pivot
            grouped = filtered.groupby(['din_instante', 'ceg'], as_index=False)['val_geracao'].mean() #aggregates for deduplication
            pivoted = grouped.pivot(index='din_instante', columns='ceg', values='val_geracao').reset_index()

            df_list.append(pivoted)

    except Exception as e:
        print(f"⚠️ Could not process {file_name}: {e}")
        errors.append(f'{file_name}: {e}')

    return df_list, errors
