import streamlit as st
import plotly.express as px
import data_functions as func

st.set_page_config(page_title="PP Analysis Dashboard", layout="wide",page_icon="assets/icon_chart.png")
st.title("Statement Analysis Dashboard")
st.divider()
uploaded_files = st.file_uploader("upload your bank statement to process", type="csv")
st.divider()
# df = func.extract_data("data/Data_Shyam.csv")
if uploaded_files is not None:
    try:
        df = func.extract_data(uploaded_files)
        total_exp, total_dc = st.columns(2, gap='medium')
        graph_total_exp, data_min_max_transaction = st.columns(2)
        pie_graph, reoccur_exp = st.columns(2)

        with total_exp:
            with st.container(border=True):
                total = func.total_expense(df)
                st.header(f":green[Total Expenses] : {total['Amount'].sum()}", divider='grey')
                st.dataframe(total, use_container_width=True)

        with total_dc:
            with st.container(border=True):
                total = func.total_debit_credit(df)
                st.header(f":green[Total Debit/Credit] ", divider='grey')
                st.dataframe(total, use_container_width=True)

        with graph_total_exp:
            with st.container(border=True):
                exp_graph_fig = func.total_expense_details(df)
                fig = px.bar(df, x='Date', y='Amount', color='Amount', color_continuous_scale=['green', 'yellow', 'red'])
                st.header(":green[Expense by Day]", divider='grey')
                st.write(fig)

        with data_min_max_transaction:
            with st.container(border=True, height="stretch"):
                max_transaction = func.max_transaction(df)
                min_transaction = func.min_transaction(df)
                avg_transaction = func.avg_expense(df)
                st.header(":green[Max Transaction]", divider='grey')
                st.dataframe(max_transaction, use_container_width=True)
                st.header(":green[Min Transaction]", divider='grey')
                st.dataframe(min_transaction, use_container_width=True)
                st.header(":green[Avg daily expense]", divider='grey')
                st.subheader(round(avg_transaction, 2))

        with pie_graph:
            with st.container(border=True, height="stretch"):
                recurring = func.recurring_transactions(df, 4)
                st.header(":green[Recurring Transactions]", divider='grey')
                fig = px.bar(recurring, x='Number of payments done', y='Transaction Details', orientation='h')
                st.write(fig)
                st.text("Note: More than 4 Transactions considered as recurring", text_alignment='left')

        with reoccur_exp:
            with st.container(border=True, height="stretch"):
                pie_data = func.total_expense_by_transaction(df, 200)
                st.header(":green[Total Expense Pie]", divider='grey')
                pie = px.pie(pie_data, values='Amount', names='Transaction Details', hole=0.3)
                st.write(pie)
                st.text("Note: Only transaction more than 200 included", text_alignment='left')

        with st.container(border=True, height="stretch"):
            with st.container(border=True, height="stretch"):
                st.header(":green[Entire Data Set]", divider='grey')
                with st.expander(label="Show data"):
                    st.dataframe(func.enitre_data(df), use_container_width=True)

    except ValueError as e:
        st.error(e)
    except Exception as e:
        st.error("There was an error while processing your data")

else:
    with st.container(horizontal_alignment='center'):
        st.header("No Data to process",text_alignment='center')