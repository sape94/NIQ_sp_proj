import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu
from streamlit_extras.switch_page_button import switch_page
from PIL import Image
from app_modules import sampling_module as samp_mod
# from app_modules import replacing_module as repl_mod
import matplotlib.pyplot as plt
import numpy as np
from app_modules import niv_sample_selection as nss

# DO_NOT_CHANGE########################################################
#######################################################################

st.set_page_config(
    page_title='NIQ APP | Sampling',
    layout='centered',
    initial_sidebar_state='collapsed'
)

hide_menu_style = """
        <style>
        #MainMenu {visibility: display;}
        </style>
        """
st.markdown(hide_menu_style, unsafe_allow_html=True)

image = Image.open('images_main/NIQ_banner.png')

st.image(image, use_column_width='always', output_format='PNG')

selected = option_menu(
    menu_title=None,
    options=['Home', 'Sampling', 'Replacing', ''],
    icons=['house', 'calculator', 'archive', 'arrow-left-circle-fill'],
    menu_icon='cast',
    default_index=1,
    orientation='horizontal',
    styles={
        "container": {"padding": "0!important",
                      "background-color": "#fafafa"},
        "icon": {"color": "#31d1ff", "font-size": "15px"},
        "nav-link": {"color": "#31333F", "font-size": "15px",
                     "text-align": "centered",
                     "margin": "0px", "--hover-color": "#eee"},
        "nav-link-selected": {"color": "#FFFFFF",
                              "background-color": "#090a47"},
    }
)


if selected == 'Home':
    switch_page('NIQ p app')

if selected == '':
    switch_page('Sindex')

if selected == 'Sampling':
    subhead_app_7 = '''
    <style>
    .subhead-item {
        backgroundcolor: transparent;
    }
    .subhead-item:hover {
        color: #2E6EF7;
    }
    </style>

    <a style='display: inline; text-align: left; color: #31333F
    ; text-decoration: none; '
    href="/Structure_sample_size" target="_self">
    <h3 class="subhead-item">
    Structured Sample Size Calculator
    </h3>
    </a>
    '''
    st.write(subhead_app_7, unsafe_allow_html=True)

    with st.expander('Expand this section to upload your Dataframe. When you finish you can collapse it again.'):
        st.write(
            'Upload the CSV or XLSX file that contains the working Dataframe:')
        uploaded_file = st.file_uploader("Choose a file",
                                         type=['csv', 'xlsx'],
                                         key='gral_settings_df'
                                         )
        if uploaded_file is not None:
            try:
                o_df = pd.read_csv(uploaded_file, encoding='UTF8')
            except:
                o_df = pd.read_excel(uploaded_file, encoding='UTF8')

            try:
                file_name_df = uploaded_file.name.replace('.csv', '')
            except:
                try:
                    file_name_df = uploaded_file.name.replace('.xlsx', '')
                except:
                    pass
            st.write(o_df)

    st.markdown('')

    if uploaded_file is None:
        st.caption('<p style="color: #2e6ef7;">Please upload a Dataframe to continue.</p>',
                   unsafe_allow_html=True)

    if uploaded_file is not None:

        st.write('')
        st.write('')
        # with st.expander('Expand this section to continue.'):
        n = 354
        N = o_df.shape[0]
        o_df_cols = o_df.columns.to_list()
        st.write('Select the **identifier** column:')
        sort_col_list = st.multiselect(
            'This would be the column that uniquely identifies the items of the Dataframe.', o_df_cols, max_selections=1)
        if sort_col_list == []:
            st.caption('<p style="color: #2e6ef7;">You must select the identifier column if you want to continue.</p>',
                       unsafe_allow_html=True)
            sort_col = ''
            p_df = o_df
            grouped_df = p_df
            pivot_df = p_df
            pivot_df_2 = pivot_df
        if sort_col_list != []:
            sort_col = sort_col_list[0]
            p_df = o_df.sort_values(sort_col)

            st.write('')
            st.write('Select the **structure** parameters column(s):')
            p_df_cols = [
                item for item in o_df_cols if item != sort_col]
            par_col_list = st.multiselect(
                'This would be the parameters that will define the structure of the Dataframe for stratification.', p_df_cols)
            if par_col_list == []:
                st.caption('<p style="color: #2e6ef7;">You must select the parameters column(s) if you want to continue.</p>',
                           unsafe_allow_html=True)
                grouped_df = p_df
                pivot_df = grouped_df
                pivot_df_2 = pivot_df
            if par_col_list != []:
                grouped_df = p_df.groupby(
                    par_col_list).size().reset_index(name='Count')

                st.write('')
                st.write('Select the **feature** column:')
                features_ans = st.multiselect(
                    'This would be the column to select specific features.', par_col_list, max_selections=1)
                st.write('')
                # if feature_op_ans == 'No.':
                if features_ans != []:
                    feat_list = p_df[features_ans[0]].unique().tolist()
                    st.write('Select the **feature** of interest:')
                    interest_features_list = st.multiselect(
                        'This would be the interesting features of the Dataframe.', feat_list, max_selections=1)
                    if interest_features_list == []:
                        st.caption('<p style="color: #2e6ef7;">Please select a feature of interest.</p>',
                                   unsafe_allow_html=True)
                    if interest_features_list != []:
                        pivot_df = grouped_df[grouped_df[features_ans[0]]
                                              == interest_features_list[0]]
                        w_pivot_df = pivot_df.copy()

                        w_pivot_df['Weight'] = (
                            w_pivot_df['Count'] / w_pivot_df['Count'].sum())
                        p = 50
                        conf_lev = 95
                        s_e = 5
                        w_pivot_df['Ch_sample_size'] = w_pivot_df['Count'].apply(lambda x: samp_mod.SamplingMachine(sample_portion=p,
                                                                                                                    confidence_level=conf_lev,
                                                                                                                    standard_error=s_e).calc_samp(population_size=x))
                        w_pivot_df['Ch_w_sample_size'] = w_pivot_df['Weight'].apply(lambda x: round(x*samp_mod.SamplingMachine(sample_portion=p,
                                                                                                                               confidence_level=conf_lev,
                                                                                                                               standard_error=s_e).calc_samp(population_size=w_pivot_df['Count'].sum())))

                        w_pivot_df.rename(
                            columns={'Count': interest_features_list[0]}, inplace=True)
                        st.write('')
                        st.write(
                            'Sample sizes given the selected structure:')
                        st.write(w_pivot_df)
                        st.caption(
                            'Per row (Ch_sample_size), and per row and weight (Ch_w_sample_size).')
                        pivot_structure_sampled_df_csv = w_pivot_df.to_csv(
                            index=False)
                        coldos_pivot_1, coldos_pivot_2 = st.columns(
                            2, gap='medium')

                        with coldos_pivot_2:
                            st.download_button(label=':floppy_disk: Download Dataframe as CSV :floppy_disk:',
                                               data=pivot_structure_sampled_df_csv,
                                               file_name=f'PIVOT_STRUCTURE_{file_name_df}.csv',
                                               mime='text/csv')

                        st.write('')
                        st.write('Don\'t forget to **download** your sampled Dataframe.')
                        st.write(
                            'If you want to remove stores from the sampled Dataframe use our:')
                        subhead_app_2 = '''
                        <style>
                        .subhead-item_2 {
                            color: #2E6EF7;
                            backgroundcolor: transparent;
                        }
                        .subhead-item_2:hover {
                            color: #164fc9;
                        }
                        </style>
            
                        <a style='display: inline; text-align: center; color: #31333F
                        ; text-decoration: none; '
                        href="/Replacing" target="_self">
                        <h5 class="subhead-item_2">
                        Replacing app
                        </h5>
                        </a>
                        '''
                        st.write(subhead_app_2, unsafe_allow_html=True)
                        st.write('')
                        st.write('')


if selected == 'Replacing':
    switch_page('Replacing')

#######################################################################

ft = """
<style>
a:link , a:visited{
color: #808080;  /* theme's text color at 75 percent brightness*/
background-color: transparent;
text-decoration: none;
}

a:hover,  a:active {
color: #0283C3; /* theme's primary color*/
background-color: transparent;
text-decoration: underline;
}

#page-container {
  position: relative;
  min-height: 10vh;
}

footer{
    visibility:hidden;
}

.footer {
position: relative;
left: 0;
top:230px;
bottom: 0;
width: 100%;
background-color: transparent;
color: #BFBFBF; /* theme's text color at 50 percent brightness*/
text-align: left; /* 'left', 'center' or 'right' if you want*/
}
</style>
<div id="page-container">
<div class="footer">
<p style='font-size: 0.875em;'>Developed by <a style='display: inline;
text-align:
left;' href="https://github.com/sape94" target="_blank">
<img src="https://i.postimg.cc/vBnHmZfF/innovation-logo.png"
alt="AI" height= "20"/><br>LatAm's Automation & Innovation Team.
</br></a></p>
</div>
</div>
"""
st.write(ft, unsafe_allow_html=True)
