import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Загрузка данных
test_with_forecast_df = pd.read_excel('test_with_forecast.xlsx')

# Преобразование дат в datetime формат
test_with_forecast_df['dt'] = pd.to_datetime(test_with_forecast_df['dt'])

# Интерфейс Streamlit
st.title("Прогнозирование цены на арматуру")

# Запрос количества недель для прогноза
weeks_ahead = st.slider("Выберите количество недель для прогноза (до 52 недель), начиная с 05.09.2022:", 1, 52, 52)

# Кнопка для отображения графика
if st.button("Показать график прогноза"):
    # Определение последней исторической даты
    last_historical_date = test_with_forecast_df[test_with_forecast_df['Цена на арматуру'].notna()]['dt'].max()

    # Разделение данных на исторические и прогнозные
    train_df = test_with_forecast_df[test_with_forecast_df['dt'] <= last_historical_date]
    forecast_df = test_with_forecast_df[
        (test_with_forecast_df['dt'] > last_historical_date) & 
        (test_with_forecast_df['dt'] <= last_historical_date + pd.Timedelta(weeks=weeks_ahead))
    ]

    # Построение основного графика
    st.subheader(f"График прогноза на {weeks_ahead} недель")
    plt.figure(figsize=(16, 8))

    # Исторические данные
    plt.plot(train_df['dt'], train_df['Цена на арматуру'],
             label='Исторические данные', color='blue', linewidth=3)

    # Прогнозные данные
    plt.plot(forecast_df['dt'], forecast_df['Forecast'],
             label='Прогноз', color='red', linestyle='--', linewidth=3)

    # Настройка графика
    plt.title(f'Прогноз цены на арматуру на {weeks_ahead} недель', fontsize=18, pad=20)
    plt.xlabel('Дата', fontsize=14)
    plt.ylabel('Цена, руб.', fontsize=14)
    plt.legend(fontsize=12, loc='upper right')
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)

    plt.tight_layout()
    st.pyplot(plt)

    # Отображение таблицы с прогнозом
    st.subheader("Таблица с прогнозом")
    forecast_table = forecast_df[['dt', 'Forecast']].rename(columns={'dt': 'Дата', 'Forecast': 'Прогноз'})
    st.dataframe(forecast_table)

    # График по месяцам (только прогноз)
    st.subheader("График прогноза по месяцам")
    forecast_df['Месяц'] = forecast_df['dt'].dt.to_period('M').astype(str)
    monthly_forecast = forecast_df.groupby('Месяц')['Forecast'].mean().reset_index()

    plt.figure(figsize=(16, 8))
    plt.plot(monthly_forecast['Месяц'], monthly_forecast['Forecast'],
             label='Прогноз по месяцам', color='green', linewidth=3)
    plt.title('Прогноз цены на арматуру по месяцам', fontsize=18, pad=20)
    plt.xlabel('Месяц', fontsize=14)
    plt.ylabel('Цена, руб.', fontsize=14)
    plt.legend(fontsize=12, loc='upper right')
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.xticks(rotation=45, fontsize=12)
    plt.yticks(fontsize=12)
    plt.tight_layout()
    st.pyplot(plt)

    # График по дням (только прогноз)
    st.subheader("График прогноза по дням")
    forecast_df['День'] = forecast_df['dt'].dt.date
    daily_forecast = forecast_df.groupby('День')['Forecast'].mean().reset_index()

    plt.figure(figsize=(16, 8))
    plt.plot(daily_forecast['День'], daily_forecast['Forecast'],
             label='Прогноз по дням', color='purple', linewidth=3)
    plt.title('Прогноз цены на арматуру по дням', fontsize=18, pad=20)
    plt.xlabel('День', fontsize=14)
    plt.ylabel('Цена, руб.', fontsize=14)
    plt.legend(fontsize=12, loc='upper right')
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.xticks(rotation=45, fontsize=12)
    plt.yticks(fontsize=12)
    plt.tight_layout()
    st.pyplot(plt)

    # Сохранение результатов в файл
    output_df = pd.concat([train_df[['dt', 'Цена на арматуру']], forecast_df[['dt', 'Forecast']]], ignore_index=True)
    output_df.to_excel('test_with_forecast_updated.xlsx', index=False)
    st.success("График успешно обновлен и сохранен в файл 'test_with_forecast_updated.xlsx'.")