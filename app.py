import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# Загрузка данных
@st.cache_data
def load_data():
    return pd.read_excel('test_with_forecast.xlsx')

test_with_forecast_df = load_data()
test_with_forecast_df['dt'] = pd.to_datetime(test_with_forecast_df['dt'])

# Интерфейс Streamlit
st.title("Прогнозирование цены на арматуру")

# Определяем даты для выбора
default_date = datetime(2022, 9, 5)  # 05.09.2022 по умолчанию
min_date = test_with_forecast_df['dt'].min()
max_date = datetime(2023, 8, 28)  # Ограничение до 28.08.2023

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
    
    # Полные исторические данные (все доступные)
    historical_df = df[df['Цена на арматуру'].notna()].copy()
    
    # Прогнозные данные (начиная с выбранной даты)
    forecast_df = df[
        (df['dt'] >= start_date) & 
        (df['Forecast'].notna())
    ].copy()

    # Добавляем месяц для прогнозных данных
    forecast_df.loc[:, 'Месяц'] = forecast_df['dt'].dt.to_period('M').astype(str)

    # Построение основного графика
    st.subheader(f"График прогноза с {start_date.strftime('%d.%m.%Y')}")
    fig1, ax1 = plt.subplots(figsize=(16, 8))

    # Все исторические данные (не зависят от выбора даты)
    ax1.plot(historical_df['dt'], historical_df['Цена на арматуру'],
             label='Исторические данные', color='blue', linewidth=2)

    # Прогнозные данные (начиная с выбранной даты)
    ax1.plot(forecast_df['dt'], forecast_df['Forecast'],
             label='Прогноз', color='red', linestyle='--', linewidth=2)

    # Вертикальная линия разделения
    ax1.axvline(start_date, color='gray', linestyle=':', linewidth=1)
    ax1.text(start_date + pd.Timedelta(days=1), ax1.get_ylim()[1]*0.95,
             'Начало прогноза', rotation=90, fontsize=10, color='gray')

    # Настройка графика
    ax1.set_title(f'Цена на арматуру: история и прогноз с {start_date.strftime("%d.%m.%Y")}', 
                 fontsize=16, pad=20)
    ax1.set_xlabel('Дата', fontsize=12)
    ax1.set_ylabel('Цена, руб.', fontsize=12)
    ax1.legend(fontsize=10, loc='upper right')
    ax1.grid(True, linestyle='--', alpha=0.5)
    plt.xticks(fontsize=10)
    plt.yticks(fontsize=10)
    plt.tight_layout()
    st.pyplot(fig1)

    # Отображение таблицы с прогнозом
    st.subheader("Таблица с прогнозом")
    forecast_table = forecast_df[['dt', 'Forecast']].rename(
        columns={'dt': 'Дата', 'Forecast': 'Прогноз'}
    )
    st.dataframe(forecast_table.style.format({'Прогноз': '{:,.0f}'}))

    # График по месяцам (только прогноз)
    st.subheader("Прогноз по месяцам")
    monthly_forecast = forecast_df.groupby('Месяц')['Forecast'].mean().reset_index()

    fig2, ax2 = plt.subplots(figsize=(12, 6))
    ax2.bar(monthly_forecast['Месяц'], monthly_forecast['Forecast'],
            color='orange', alpha=0.7)
    ax2.set_title('Средняя прогнозируемая цена по месяцам', fontsize=14)
    ax2.set_xlabel('Месяц', fontsize=10)
    ax2.set_ylabel('Средняя цена, руб.', fontsize=10)
    plt.xticks(rotation=45, fontsize=8)
    plt.yticks(fontsize=8)
    plt.tight_layout()
    st.pyplot(fig2)

    # Сохранение результатов
    output_df = pd.concat([historical_df, forecast_df], axis=0)
    output_df.to_excel('test_with_forecast_updated.xlsx', index=False)
    st.success("Данные сохранены в файл 'test_with_forecast_updated.xlsx'")