# importing needed libraries
import numpy as np
import pandas as pd
import plotly.express as px

# Data Reading
df_source = pd.read_csv("./Superstore-Analysis/Sources/Sample_Superstore.csv", encoding= 'unicode_escape') # Data from source - Before cleaning

# Data Cleaning & Preprocessing
# 1- Drop unnecessary columns.(customer name, country, postal code, region, city)
# 2- Check duplicate records.
# 3- Convert (Order Date & Ship Date) type to Date type.
# 4- Make columns names in one style.  
# 5- Dividing columns into two groups qual and quant.
# 6- Adding necessary columns.

df_source.drop(['Customer Name','Country','Postal Code','Region','City'], axis= 1, inplace= True)
df_source['Order Date'] = pd.to_datetime(df_source['Order Date'])
df_source['Ship Date'] = pd.to_datetime(df_source['Ship Date'])
df_source.columns = df_source.columns.str.lower().str.replace(' ','_').str.replace('-','_')
df = df_source # Data Frame after Cleaning
df['delivery_days'] = (df['ship_date'] - df['order_date']) / np.timedelta64(1, 'D')
df['order_year'] = df['order_date'].dt.year
df['order_month'] = df['order_date'].dt.month
df['order_day'] = df['order_date'].dt.day
qunat = [col for col in df.columns if (df[col].dtype != 'O' and df[col].dtype != 'datetime64[ns]')]
main_quant = ['sales','quantity','profit']
qual = [col for col in df.columns if (df[col].dtype == 'O' or df[col].dtype == 'datetime64[ns]')]

# Functions for first tab (Overall vision)
# First line chart
df_time = df.groupby('order_date')[['sales','profit']].sum().reset_index().sort_values(by= 'order_date')
fig_1 = px.line(df_time, x= 'order_date', y= ['sales','profit'], title= 'Total Sales & Profit over Time Period (2014-2017)')
# First bar chart
df_year = df.groupby('order_year')[['sales','profit']].sum().reset_index().sort_values(by= 'order_year')
fig_bar_year = px.bar(df_year, x= 'order_year', y= ['sales','profit'], barmode= 'group', title= 'Total Sales & Profit in each year')

# Pie charts
# pie_dist function takes dataframe, fact column, dimension column and returns pie chart

def pie_dist (dataf,dim,fact):
    pie_data = dataf.groupby(dim)[fact].sum().reset_index()
    fig_pie = px.pie(pie_data, values= fact, names= dim, title= f'Share of total {fact} by {dim}')
    return fig_pie

# Functions for second tab (States analysis) 
# Grouping function takes dataframe, fact column, dimension column and returns df with dim grouped and its fact
def grouping(df, dim, fact):
    df_grouped = df.groupby(dim)[fact].sum().reset_index().sort_values(fact, ascending = False).reset_index()[[dim,fact]]
    return df_grouped 

# Top 10 function dataframe, fact column, dimension column , high or low and returns bar plot with data
def bar_dist (dataf,dim,fact,section= 'Highest'):
    s_highest = pd.Series(range(10))
    s_lowest = pd.Series(range((df.state.nunique() - 10), df.state.nunique()))
    if section == 'Highest':
        bar_data = dataf.groupby(dim)[fact].sum().reset_index().sort_values(fact, ascending = False).head(10).set_index(s_highest)
    elif section == 'Lowest':
        bar_data = dataf.groupby(dim)[fact].sum().reset_index().sort_values(fact, ascending = False).tail(10).set_index(s_lowest)    
    fig_bar = px.bar(bar_data, x= fact, y= dim, width= 400).update_yaxes(categoryorder = 'total ascending')
    return fig_bar, bar_data
       

# One state function takes dataframe , fact, state, year and returns bar plot
def state_time (df, fact, state, year):
    df_state_time = df[(df['order_year'] == year) & (df['state']== state)].groupby(['order_month','category'])[fact].sum().reset_index()
    tit = f'Distribution of {fact} over {year} in {state}'
    fig_bar = px.bar(df_state_time, x= 'order_month', y= fact, color= 'category', title= tit)
    return fig_bar  

# functions for third tab (cat & sub_category tab)
# profit margin bar plot function calculates profit margin and returns bar plot 
def margin_bar(df):
    df_margin = df.groupby(['sub_category'])[['sales','profit']].sum().reset_index()
    df_margin['margin'] = (df_margin['profit'] / df_margin['sales']) * 100
    df_margin.sort_values(by= 'margin', ascending= True, inplace= True)
    fig_margin = px.bar(df_margin, x= 'margin', y= 'sub_category', color= 'margin',text= (df_margin['margin']/100), text_auto='.2s', title= 'Profit margin by sub_category')
    fig_margin.update_traces(texttemplate='%{text:.1%}', textposition='inside')
    fig_margin.add_vline(x= df_margin.select_dtypes(include= 'number').mean()[2], opacity=1, line_width=2, line_dash='dash', line_color='Red', annotation_text= f'Mean of Profit margin \n {int(df_margin.mean()[2])} %', annotation_font_color = "Red")
    return fig_margin

# Bar plot function in category & sub_category tab returns bar plot 
def bar_plot(df, dim, fact):
    df_sub_category = df.groupby(dim)[fact].sum().reset_index().sort_values(fact, ascending= False)
    fig_bar = px.bar(df_sub_category, x= dim, y= fact, color= fact, title= f'Distribution of {dim} According to {fact}')
    fig_bar.add_hline(y= df_sub_category.select_dtypes(include= 'number').mean()[0],opacity=1, line_width=2, line_dash='dash', line_color='Red', annotation_text= f'Mean of {fact} \n {int(df_sub_category.mean()[0])}')
    return fig_bar 

# Scatter function in sub_category tab takes dataframe, dimension, dimension value and returns scatter plot for sales against profit for this dimension value
def sub_cat_scat(df, dim, dim_value):
    df_scat = df[df[dim] == dim_value]
    corr_value = float('%.4f' % (df_scat.corr().loc['sales','profit']))
    scat_sub_cat = px.scatter(df_scat, x= 'sales', y= 'profit', title= f'Correlation between Sales & Profit of {dim_value} equal {corr_value}') 
    return scat_sub_cat # scatter plot

# functions for Fourth tab (segment)
# bar plot of segment and category for sales and profit
def seg_cat(df,fact):
    df_seg_cat = df.groupby(['segment','category'])[fact].sum().reset_index().sort_values(by= fact)
    fig_seg_cat = px.bar(df_seg_cat, x= 'segment', y= [fact], barmode= 'group', color= 'category', title= f'Total {fact} per segment')
    return fig_seg_cat # bar plot

# bar plot function takes fact, state, year and returns bar plot 
def state_time_segment (df, fact, state, year):
    df_state_time = df[(df['order_year'] == year) & (df['state']== state)].groupby(['order_month','segment'])[fact].sum().reset_index()
    tit = f'Distribution of {fact} over {year} in {state}'
    fig_bar_segment = px.bar(df_state_time, x= 'order_month', y= fact, color= 'segment', title= tit)
    return fig_bar_segment            
