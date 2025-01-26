# Data Analysis and Dashboard Project ✨

## Setup Environment - Anaconda
'''
conda create --name main-ds python=3.9
conda activate main-ds
pip install -r requirements.txt
'''


## Setup Environment - Shell/Terminal
'''
mkdir proyek_analisis_data
cd proyek_analisis_data
pipenv install
pipenv shell
pip install -r requirements.txt
'''


## Run Streamlit App
'''
cd dashboard
streamlit run app.py
'''


## Project Structure
README.md
├───dashboard
│ ├───main_data.csv
│ └───dashboard.py
├───data
│ ├───data_1.csv
│ └───data_2.csv
├───notebook.ipynb
├───README.md
├───requirements.txt
└───url.txt


## Project Overview
Proyek ini merupakan analisis data dan pembuatan dashboard interaktif menggunakan dataset yang tersedia di folder `data`. Analisis dilakukan untuk mengeksplorasi dan memvisualisasikan insights penting dari data.

## File Descriptions
- `dashboard/dashboard.py`: Berisi kode untuk dashboard interaktif menggunakan Streamlit
- `dashboard/main_data.csv`: Dataset yang digunakan untuk dashboard
- `data/data_1.csv` & `data/data_2.csv`: Dataset mentah untuk analisis
- `notebook.ipynb`: Jupyter notebook berisi proses analisis data lengkap
- `requirements.txt`: Daftar package Python yang diperlukan
- `url.txt`: Berisi URL deployment dashboard

## Dashboard Features
Dashboard ini menyediakan beberapa fitur utama:
1. Data Overview
2. Interactive Visualizations
3. Data Filtering
4. Key Insights Display

## Dependencies
- streamlit==1.32.0
- pandas==2.2.0
- matplotlib==3.8.3
- seaborn==0.13.2
- numpy==1.26.4
- plotly==5.18.0

## Deployed Dashboard
Anda dapat mengakses dashboard yang sudah di-deploy melalui link yang tersedia di file `url.txt`

## Author
[Ayu Irmawati]

