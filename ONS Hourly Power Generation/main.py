from power_generation import process_ons_generation

# Configuration Variables
OUTPUT_NAME = 'generation_database.xlsx' 
CEGS = ['UHE.PH.PR.001161-4.01', 'UTN.UR.RJ.000101-5.01'] # CEG examples

if __name__ == "__main__":
    
    process_ons_generation(cegs=CEGS, start_year=2021, end_year=2023, end_month=12, output_name=OUTPUT_NAME)
