import pandas as pd
import streamlit as st
import csv


# def extract_data(file) -> pd.DataFrame:
#     ext_data = []
#     with open(file, 'r', encoding='utf-8') as data:
#         csv_data = csv.reader(data)
#         for row in csv_data:
#             if len(row) >= 8:
#                 ext_data.append(row)
#     data_frame = pd.DataFrame(ext_data)
#     data_frame.columns = data_frame.iloc[0]
#     data_frame = data_frame.drop([0, 0])
#     data_frame['Date'] = pd.to_datetime(data_frame['Date'], format='mixed', dayfirst=True)
#     data_frame['Amount'] = data_frame['Amount'].astype(int)
#     return data_frame

@st.cache_data
def extract_data(file) -> pd.DataFrame:
    ext_data = []
    csv_data = csv.reader(file.getvalue().decode('utf-8').splitlines())
    for row in csv_data:
        if len(row) >= 8:
            ext_data.append(row)
    if not ext_data:
        raise ValueError("The CSV contains no valid rows.")
    data_frame = pd.DataFrame(ext_data)
    data_frame.columns = data_frame.iloc[0]
    data_frame = data_frame.drop([0, 0])
    data_frame['Date'] = pd.to_datetime(data_frame['Date'], format='mixed', dayfirst=True)
    data_frame['Amount'] = data_frame['Amount'].astype(int)
    return data_frame


def max_transaction(df) -> pd.DataFrame:
    return df[df['Amount'] == df['Amount'].max()][['Date', 'Transaction Details', 'Amount']]


def min_transaction(df) -> pd.DataFrame:
    return df[df['Amount'] == df['Amount'].min()][['Date', 'Transaction Details', 'Amount']]


def max_debit(df) -> pd.DataFrame:
    df = df[(df['Transaction Type'] == 'DEBIT')]
    return df[df['Amount'] == df['Amount'].max()][['Date', 'Time', 'Transaction Details', 'Amount']]


def max_credit(df) -> pd.DataFrame:
    df = df[(df['Transaction Type'] == 'CREDIT')]
    return df[df['Amount'] == df['Amount'].max()][['Date', 'Time', 'Transaction Details', 'Amount']]


def total_expense(df) -> pd.DataFrame:
    return df.groupby([df['Date'].dt.to_period('M')])['Amount'].sum().reset_index()


def total_debit_credit(df) -> pd.DataFrame:
    return df.groupby(['Transaction Type'])['Amount'].sum().reset_index()


def recurring_transactions(df, val=0) -> pd.DataFrame:
    df['Month-Year'] = df['Date'].dt.to_period('M')
    df = (
        df[['Transaction Details', 'Month-Year']]
        .value_counts()
        .reset_index(name='Number of payments done')
    ).sort_values(by='Number of payments done', ascending=False)

    return df[df['Number of payments done'] >= val]


def total_expense_by_transaction(df, val=0) -> pd.DataFrame:
    df = df.groupby('Transaction Details')['Amount'].sum().reset_index().sort_values(by='Amount', ascending=False)
    df = df[df['Amount'] >= val]
    return df


def total_expense_details(df) -> pd.DataFrame:
    return df.groupby('Date')['Amount'].sum().reset_index()


def avg_expense(df) -> pd.DataFrame:
    return df['Amount'].mean()


def enitre_data(df) -> pd.DataFrame:
    return df[['Date', 'Time', 'Transaction Details', 'Transaction Type', 'Amount']].sort_values(by=['Date', 'Time'],
                                                                                                 ascending=[False,
                                                                                                            True])
