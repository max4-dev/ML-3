import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# Загрузка данных
@st.cache_data
def load_data():
    return pd.read_excel('test_with_forecast.xlsx')

def load_optimal_purchase():
    return pd.read_excel('optimal_purchase_forecast.xlsx')

test_with_forecast_df = load_data()
test_with_forecast_df['dt'] = pd.to_datetime(test_with_forecast_df['dt'])

optimal_purchase_df = load_optimal_purchase()
optimal_purchase_df['dt'] = pd.to_datetime(optimal_purchase_df['dt'])

# Интерфейс Streamlit
st.title("Прогнозирование цены на арматуру")

# Определяем даты для выбора
default_date = datetime(2022, 9, 5)
min_date = test_with_forecast_df['dt'].min()
max_date = datetime(2023, 8, 28)

# Выбор даты начала прогноза
start_date = st.date_input(
    "Выберите дату начала прогноза:",
    value=default_date,
    min_value=min_date,
    max_value=max_date,
    format="DD.MM.YYYY"
)
start_date = pd.to_datetime(start_date)

# Кнопка для отображения графика
if st.button("Показать график прогноза"):
    # Создаем копию данных
    df = test_with_forecast_df.copy()
    
    # Полные исторические данные
    historical_df = df[df['Цена на арматуру'].notna()].copy()
    
    # Прогнозные данные
    forecast_df = df[(df['dt'] >= start_date) & (df['Forecast'].notna())].copy()
    
    # Построение графика
    st.subheader(f"График прогноза с {start_date.strftime('%d.%m.%Y')}")
    fig1, ax1 = plt.subplots(figsize=(16, 8))
    
    ax1.plot(historical_df['dt'], historical_df['Цена на арматуру'],
             label='Исторические данные', color='blue', linewidth=2)
    ax1.plot(forecast_df['dt'], forecast_df['Forecast'],
             label='Прогноз', color='red', linestyle='--', linewidth=2)
    ax1.axvline(start_date, color='gray', linestyle=':', linewidth=1)
    ax1.set_title(f'Цена на арматуру: история и прогноз с {start_date.strftime("%d.%m.%Y")}', fontsize=16)
    ax1.set_xlabel('Дата', fontsize=12)
    ax1.set_ylabel('Цена, руб.', fontsize=12)
    ax1.legend(fontsize=10, loc='upper right')
    ax1.grid(True, linestyle='--', alpha=0.5)
    plt.tight_layout()
    st.pyplot(fig1)
    
    # Отображение таблицы из optimal_purchase_forecast.xlsx
    st.subheader("Таблица с оптимальным прогнозом закупок")
    filtered_purchase_df = optimal_purchase_df[optimal_purchase_df['dt'] >= start_date].copy()
    
    # Удаляем колонку "Цена на арматуру" если она есть и переименовываем колонки
    if 'Цена на арматуру' in filtered_purchase_df.columns:
        filtered_purchase_df = filtered_purchase_df.drop(columns=['Цена на арматуру'])
    
    filtered_purchase_df = filtered_purchase_df.rename(columns={
        'dt': 'Дата',
        'Forecast': 'Предсказание'
    })
    
    st.dataframe(filtered_purchase_df.style.format({'Предсказание': '{:,.0f}', 'Объем': '{:,.0f}'}))
    
    # Сохранение результатов
    output_df = pd.concat([historical_df, forecast_df], axis=0)
    output_df.to_excel('test_with_forecast_updated.xlsx', index=False)
    st.success("Данные сохранены в файл 'test_with_forecast_updated.xlsx'")