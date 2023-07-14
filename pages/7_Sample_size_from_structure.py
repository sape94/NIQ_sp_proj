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
    href="/Sample_size_from_structure" target="_self">
    <h3 class="subhead-item">
    Sample Size from Structure
    </h3>
    </a>
    '''
    st.write(subhead_app_7, unsafe_allow_html=True)

    # st.markdown('How you want to proceed:')

    with st.expander('Expand this section to upload your Dataframe. When you finish you can collapse it again.'):
        st.write(
            'Upload the CSV file that contains the Reference Dataframe:')
        uploaded_file = st.file_uploader("Choose a file",
                                         type=['csv'],
                                         key='gral_settings_df'
                                         )
        if uploaded_file is not None:
            pivot = pd.read_csv(uploaded_file, encoding='UTF8')

            pivot_name_df = uploaded_file.name.replace('.csv', '')

            pivot = pivot.fillna(0)
            st.write(pivot)

    st.markdown('')

    if uploaded_file is None:
        st.caption('<p style="color: #2e6ef7;">Please upload a Dataframe to continue.</p>',
                   unsafe_allow_html=True)

    if uploaded_file is not None:
        p = 50
        conf_lev = 95
        s_e = 5
        
        st.markdown('')
        st.write('')

        st.write('Select the **all the quota** columns:')
        quota_cols = st.multiselect(
            'This would be the relevant columns to generate the Summary dataframe.', pivot.columns)
        if quota_cols == []:
            st.caption('<p style="color: #2e6ef7;">You must select all the quota columns if you want to continue.</p>',
                       unsafe_allow_html=True)

        if quota_cols != []:
            pre_interest_cols = [
                x for x in pivot.columns if x not in quota_cols]
            interest_cols = [
                col for col in pre_interest_cols if pivot[col].dtype == float]
            pivot[interest_cols] = pivot[interest_cols].round()

            st.markdown('')
            st.write('')
            result_df = pd.DataFrame()
            for column in pivot.columns:
                result_df[column] = pivot[column]
                if column in interest_cols:
                    weight_column = f'{column}_weight'
                    result_df[weight_column] = (
                        pivot[column] / pivot[column].sum())
                    r_sample_size = f'{column}_regular_sample_size'
                    w_sample_size = f'{column}_weighted_sample_size'
                    result_df[r_sample_size] = result_df[column].apply(lambda x: samp_mod.SamplingMachine(sample_portion=p,
                                                                                                          confidence_level=conf_lev,
                                                                                                          standard_error=s_e
                                                                                                          ).calc_samp(population_size=x))
                    result_df[w_sample_size] = result_df[weight_column].apply(lambda x: round(x*samp_mod.SamplingMachine(sample_portion=p,
                                                                                                                         confidence_level=conf_lev,
                                                                                                                         standard_error=s_e
                                                                                                                         ).calc_samp(population_size=pivot[column].sum())))
            st.markdown(
                r'This is the **Sample Size by Structure** dataframe:')
            st.write(result_df)
            result_csv = result_df.to_csv(index=False)

            colres3, colres4 = st.columns(2, gap='medium')

            with colres4:
                st.download_button(label=':floppy_disk: Download Dataframe as CSV :floppy_disk:',
                                   data=result_csv,
                                   file_name=f'sample_size_structure_{pivot_name_df}.csv',
                                   mime='text/csv')
            st.write('')
            st.markdown(
                'Don\'t forget to **download** your Dataframe.')


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
</br></a>Version 1.4.1-b.1.</p>
</div>
</div>
"""
st.write(ft, unsafe_allow_html=True)
