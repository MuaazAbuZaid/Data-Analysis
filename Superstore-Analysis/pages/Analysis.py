# import needed libraries
import streamlit as st

import sys
# Directing to MEDA file path to be able to read it
# sys.path.append( 'D:\Moaaz\Programming\Epsilon_Data_Science_Diploma\Mid_Project' ) # Path of MEDA file
import MEDA as md

# Dividing our analysis into tabs, each tab contains information in one dimension and many facts (sales, profit, quantity)
tab_overall_vision, tab_states, tab_categ_subcat, tab_segment, tab_conclusion = st.tabs(['Overall Vision','States','Category & Subcategory','Segment','Conclusion'])

# Overall Vision Tab

with tab_overall_vision:
    # Title of tab
    st.title('Some statistcs over Time Period (2014-2017)') 
    # insights in this tab
    st.write('The information in this tab can answer the following questions :') 
    st.write('    1- Does the overall store profit is positive? Do we make money?')
    st.write('    2- if the profit is positive, Does it increase over time?')
    st.write('    3- Share of some dimensions in some facts?')
    # First section
    st.header('1- Does the overall store profit is positive? Do we make money?') 
    st.write('You can notice that the most values of the chart is above zero, which is good news.')
    st.plotly_chart(md.fig_1)
    # Second section
    st.header('2- if the profit is positive, Does it increase over time?')
    st.write('You can notice that the profit increases each year from the previous one.')
    st.plotly_chart(md.fig_bar_year)
    # Third section
    st.header('3- Share of some dimensions in some facts?')
    con_pie = st.container()
    col1_p, col2_p = con_pie.columns(2)
    with col1_p:
        # variable for each radio button to save the choosed value
        fact = st.radio(
                "Select value you interest",
                ["sales", "profit", "quantity"],
                horizontal= True,
            )
    with col2_p:
        dim = st.radio(
                "Select dimension you interest",
                ["category", "segment", "ship_mode"],
                horizontal= True,
            )
    # Passing the saved value choosed to pie_dist function in MEDA file which returns pie chart        
    st.plotly_chart(md.pie_dist(md.df, dim, fact))

# States Tab

with tab_states:
    # Title of tab
    st.title('Here you can focus in each state in specfic year')
    # insights in this tab
    st.write('The information in this tab can answer the following questions :')
    st.write('    1- What is the highest state according to profit?')
    st.write('    2- What is the least state according to profit?')
    st.write('    3- What are the highest & least ten states according to profit?')
    st.write('    4- What is the total sales, profit or quantity in each state in specific time?')
    # First section
    st.header('1- What is the highest state according to profit?')
    # Passing state and profit columns to grouping function in MEDA file which returns data about profit in each state
    states_rank = md.grouping(md.df, 'state', 'profit')
    con_best_state = st.container()
    col1_best_state, col2_best_state = con_best_state.columns(2)
    with col1_best_state:
        best_state = states_rank.state.head(1)[0] 
        st.subheader(best_state)
    best_state_profit = states_rank.profit.head(1)[0]    
    col2_best_state.metric('Profit',int(best_state_profit), int(best_state_profit))
    # Second section   
    st.header('2- What is the least state according to profit?')
    con_worst_state = st.container()
    col1_worst_state, col2_worst_state = con_worst_state.columns(2)
    with col1_worst_state:
        worst_state = states_rank.state.tail(1)[states_rank.profit.idxmin()]
        st.subheader(worst_state)
    worst_state_profit = states_rank.profit.tail(1)[states_rank.profit.idxmin()]    
    col2_worst_state.metric('Profit',int(worst_state_profit), int(worst_state_profit))
    # Third section
    st.header('3- What are the highest & least ten states according to profit?')
    con_state_radio_10 = st.container()
    con_state_radio_10_fact_1, con_state_radio_10_pos_2 = con_state_radio_10.columns(2)
    with con_state_radio_10_fact_1:
        # variable for each radio button to save the choosed value
        state_fact_10 = st.radio(
                "Select value you interest",
                ["sales", "profit", "quantity"],
                horizontal= True,
                key= 'state_10',
            )
    with con_state_radio_10_pos_2:
        state_pos = st.radio(
                "Select your interest",
                ['Highest','Lowest'],
                horizontal= True,
                key= 'state_10_pos',
            )
    # Passing the choosed value to bar_dist function in MEDA file which returns bar plot & the data         
    fig_10, data_10 = md.bar_dist (md.df,'state',state_fact_10,section= state_pos)          
    cont_state_10 = st.container() 
    col1_satate_10, col2_state_10 =  cont_state_10.columns(2)
    col1_satate_10.plotly_chart(fig_10) 
    col2_state_10.dataframe(data_10, width= 600)    
    # Fourth section
    st.header('4- What is the total sales, profit or quantity in each state in specific time?')
    # save the choosed state in variable state.
    state = st.selectbox('Pick state you interest', tuple(md.df.state.unique()), key= 'state_box')
    con_state_radio = st.container()
    con_state_radio_fact_1, con_state_radio_year_2 = con_state_radio.columns(2)
    with con_state_radio_fact_1:
        # variable for each radio button to save the choosed value
        state_fact = st.radio(
                "Select value you interest",
                ["sales", "profit", "quantity"],
                horizontal= True,
                key= 'state',
            )
    with con_state_radio_year_2:
        state_year = st.radio(
                "Select year you interest",
                [2014, 2015, 2016, 2017],
                horizontal= True,
                key= 'year',
            ) 
    # Passing the choosed value to state_time function in MEDA file which returns bar plot                
    st.plotly_chart(md.state_time(md.df, state_fact, state, state_year))

# Category & Subcategory Tab

with tab_categ_subcat:
    # Title of tab 
    st.title('Here you can get more information about each category & subcategory')
    # Insights in this tab
    st.write('The information in this tab can answer the following questions :')
    st.write('    1- What are the highest category & subcategory according to profit?')
    st.write('    2- What are the least category & subcategory according to profit?')
    st.write('    3- What is the profit margin of each subcategory?')
    st.write('    4- What is the distribution of category & subcategory according to sales, profit & quantity?')
    st.write('    5- What is the relation between sales & profit for each sub category?')
    # First section
    st.header('1- What are the highest category & subcategory according to profit?')
    # Passing category and profit columns to grouping function in MEDA file which returns data about profit per each category
    category_rank = md.grouping(md.df, 'category', 'profit')
    con_best_category = st.container()
    col1_best_category, col2_best_category = con_best_category.columns(2)
    with col1_best_category:
        best_category = category_rank.category.head(1)[0]
        st.subheader(best_category)
    best_category_profit = category_rank.profit.head(1)[0]    
    col2_best_category.metric('Profit',int(best_category_profit), int(best_category_profit))
    # Passing subcategory and profit columns to grouping function in MEDA file which returns data about profit per each subcategory
    sub_category_rank = md.grouping(md.df, 'sub_category', 'profit')
    con_best_sub_category = st.container()
    col1_best_sub_category, col2_best_sub_category = con_best_sub_category.columns(2)
    with col1_best_sub_category:
        best_sub_category = sub_category_rank.sub_category.head(1)[0]
        st.subheader(best_sub_category)
    best_sub_category_profit = sub_category_rank.profit.head(1)[0]    
    col2_best_sub_category.metric('Profit',int(best_sub_category_profit), int(best_sub_category_profit))
    # Second Section
    st.header('2- What are the least category & subcategory according to profit?')
    con_lowest_category = st.container()
    col1_lowest_category, col2_lowest_category = con_lowest_category.columns(2)
    with col1_lowest_category:
        lowest_category = category_rank.category.tail(1)[category_rank.profit.idxmin()]
        st.subheader(lowest_category)
    lowest_category_profit = category_rank.profit.tail(1)[category_rank.profit.idxmin()]    
    col2_lowest_category.metric('Profit',int(lowest_category_profit), int(lowest_category_profit))

    con_lowest_sub_category = st.container()
    col1_lowest_sub_category, col2_lowest_sub_category = con_lowest_sub_category.columns(2)
    with col1_lowest_sub_category:
        lowest_sub_category = sub_category_rank.sub_category.tail(1)[sub_category_rank.profit.idxmin()]
        st.subheader(lowest_sub_category)
    lowest_sub_category_profit = sub_category_rank.profit.tail(1)[sub_category_rank.profit.idxmin()]    
    col2_lowest_sub_category.metric('Profit',int(lowest_sub_category_profit), int(lowest_sub_category_profit))
    # Third section
    st.header('3- What is the profit margin of each subcategory?')
    # margin bar function in MEDA file takes dataframe and returns bar plot (margin)
    st.plotly_chart(md.margin_bar(md.df))
    # Fourth section
    st.header('4- What is the distribution of category & subcategory according to sales, profit & quantity?')
    con_cat_radio = st.container()
    col1_cat_radio, col2_cat_radio = con_cat_radio.columns(2)
    with col1_cat_radio:
        # variable for each radio button to save the choosed value
        fact_cat = st.radio(
                "Select value you interest",
                ["sales", "profit", "quantity"],
                horizontal= True,
                key= 'cat_fact',
            )
    with col2_cat_radio:
        dim_cat = st.radio(
                "Select dimension you interest",
                ["category", "sub_category"],
                horizontal= True,
                key= 'cat',
            )
    # Passing the saved values to bar_plot function in MEDA file which returns bar plot with line indicates to the mean
    fig_bar_cat = md.bar_plot(md.df, dim_cat, fact_cat)
    st.plotly_chart(fig_bar_cat)
    # Fifth section
    st.header('5- What is the relation between sales & profit for each sub category?')
    # save the choosed sub_category in variable sub_category.
    sub_category = st.selectbox('Pick sub_category you interest', tuple(md.df.sub_category.unique()), key= 'sub_category_box')
    # Passing the choosed sub category to sub_cat_scat function in MEDA file which returns scatter diagram
    st.plotly_chart(md.sub_cat_scat(md.df, 'sub_category', sub_category))

# Segment Tab

with tab_segment:
    # Title of tab
    st.title('Segments of our customers')
    st.write('The information in this tab can answer the following questions :')
    st.write('    1- What is the share of total sales by customer segment?')
    st.write('    2- What is the total sales by each segment?')
    st.write('    3- What is the total profit by each segment?')
    st.write('    4- What is the distribution of each customer segment in specific state & time?')
    # First section
    st.header('1- What is the share of total sales by customer segment?')
    # save the choosed value in fact_segment variable
    fact_segment = st.selectbox('Pick value you interest', tuple(md.main_quant))
    # Passing the choosed value to pie_dist function in MEDA file which returns pie chart
    st.plotly_chart(md.pie_dist(md.df, 'segment', fact_segment))
    # Second section
    st.header('2- What is the total sales by each segment?')
    # seg_cat function in MEDA file takes the dataframe and the fact column returns bar plot 
    st.plotly_chart(md.seg_cat(md.df, 'sales'))
    # Third section
    st.header('3- What is the total profit by each segment?')
    # seg_cat function in MEDA file takes the dataframe and the fact column returns bar plot
    st.plotly_chart(md.seg_cat(md.df, 'profit'))
    # Fourth section
    st.header('4- What is the distribution of each customer segment in specific state & time?')
    # save the choosed value in state_segment variable
    state_segment = st.selectbox('Pick state you interest', tuple(md.df.state.unique()), key= 'segment_box')
    con_segment_radio = st.container()
    con_segment_radio_fact_1, con_segment_radio_year_2 = con_segment_radio.columns(2)
    with con_segment_radio_fact_1:
        # variable for each radio button to save the choosed value
        segment_fact = st.radio(
                "Select value you interest",
                ["sales", "profit", "quantity"],
                horizontal= True,
                key= 'segment',
            )
    with con_segment_radio_year_2:
        segment_year = st.radio(
                "Select year you interest",
                [2014, 2015, 2016, 2017],
                horizontal= True,
                key= 'year_segment',
            ) 
    # Passing the choosed value to state_time_segment function in MEDA file which returns bar plot               
    st.plotly_chart(md.state_time_segment(md.df, segment_fact, state_segment, segment_year))
    
with tab_conclusion:
    # Title of tab
    st.title('What we see through this analysis')
    # Conclusion
    st.write('We can see the following results:')
    st.write('    1- Generally the store makes money and it increases year by year.')
    st.write('    2- We have some states have negative profit!!.')
    st.write('    3- We have three subcategories with negative profit!!.')
    st.write('    4- Profit margin differs from subcategory to another.')
    st.write('    5- Best state is California and worst one is Texas.   (Profit)')
    st.write('    6- Best Category is Technology & worst one is furniture.   (Profit)')
    st.write('    7- Best subcategory is copiers & worst one is tables.   (Profit)')
    st.write('    8- Consumers represents almost half of our sales and profit.')
