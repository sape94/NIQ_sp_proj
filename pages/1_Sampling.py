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


@st.cache_data
def cache_df(o_df, p, conf_lev, s_e):
    cc_1 = samp_mod.SamplingMachine(sample_portion=p,
                                    confidence_level=conf_lev,
                                    standard_error=s_e).rand_samp(o_df)
    return cc_1


def cache_df_2(o_df, p, conf_lev, s_e):
    cc_2 = samp_mod.SamplingMachine(sample_portion=p,
                                    confidence_level=conf_lev,
                                    standard_error=s_e).rand_samp(o_df)
    return cc_2


if selected == 'Home':
    switch_page('NIQ p app')

if selected == '':
    switch_page('Sindex')

if selected == 'Sampling':
    subhead_app_1 = '''
    <style>
    .subhead-item {
        backgroundcolor: transparent;
    }
    .subhead-item:hover {
        color: #2E6EF7;
    }
    </style>

    <h3 class="subhead-item">
    Sampling app
    </h3>
    '''
    st.write(subhead_app_1, unsafe_allow_html=True)

    with st.expander('If you want to upload a Dataframe, expand this section. When you finish you can collapse it again.'):
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

    # with st.expander(r'Expand this section if you know the **sample portion** from previous samples.'):
    #    p_100 = st.slider(
    #        r'Select the sample\'s portion value, $p$, (%):', 0, 100, 50)
    #    p = int(p_100)

    #    col1, col2 = st.columns(2, gap='medium')

    #    with col1:
    #        st.write('Select the **confidence level** (%):')
    #        conf_lev = st.selectbox(
    #            r'',
    #            ('95', '99', '98', '90', '85', '80'))

    #    with col2:
    #        z_score_dict = {99: 2.576,
    #                        98: 2.326,
    #                        95: 1.96,
    #                        90: 1.645,
    #                        85: 1.44,
    #                        80: 1.282}
    #        st.write(r'Then, the **Z-score value**, $Z$, is:')
    #        z_s = str(z_score_dict[int(conf_lev)])
    #        z_box = st.selectbox(r'',
    #                             (f'{z_s}', '0'), disabled=True)

    #    st.markdown('')
    #    st.markdown('')

    #    col3, col4 = st.columns(2, gap='medium')

    #    with col3:
    #        st.write(r'Select, $e$, the **standard error**(%):')
    #        s_e = st.selectbox(
    #            r'',
    #            ('5', '1', '2', '10', '20'))

    #    st.markdown('')
    #    st.markdown('')

    p = 50
    conf_lev = 95
    s_e = 5

    col_res_1, col_res_2, col_res_3 = st.columns([1, 2, 1], gap='medium')

    with col_res_2:
        if uploaded_file is not None:
            st.write(r'The **population size** is:')
            N = o_df.shape[0]
            N_s = str(N)
            z_box = st.selectbox(
                r'',
                (f'{N_s}', '4'), disabled=True)
        else:
            st.write(r'Type the **population size**:')
            N = st.number_input('', min_value=1)

        st.markdown('')
        st.markdown('')

        n = samp_mod.SamplingMachine(sample_portion=p,
                                     confidence_level=conf_lev,
                                     standard_error=s_e).calc_samp(population_size=N)

        st.markdown(
            r':arrow_forward::arrow_forward: Then, the **sample size** is:')
        st.latex(f'n = {n}')

    st.markdown('')
    st.markdown('')

    if uploaded_file is not None:
        with st.expander('If you want to sample the Dataframe, expand this section. When you finish you can collapse it again.'):
            samp_ans = st.radio('Do you want to sample your Dataframe?',
                                ('No.',
                                 'Yes, with a non-stratified method.',
                                 'Yes, with a stratified (structured) method.'))
            if samp_ans == 'Yes, with a non-stratified method.':
                sampled_df = cache_df(o_df, p=p, conf_lev=conf_lev, s_e=s_e)
                if st.button(':inbox_tray: Press here to re-sample :inbox_tray:'):
                    o_df = o_df.sample(frac=1)
                    sampled_df = cache_df_2(
                        o_df, p=p, conf_lev=conf_lev, s_e=s_e)

                st.write(sampled_df)
                sampled_df_csv = sampled_df.to_csv(index=False)

                coldoss, coldos = st.columns(2, gap='medium')

                with coldos:
                    st.download_button(label=':floppy_disk: Download Dataframe as CSV :floppy_disk:',
                                       data=sampled_df_csv,
                                       file_name=f'SAMPLED_{file_name_df}.csv',
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

            if samp_ans == 'Yes, with a stratified (structured) method.':
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

                        pivot_df = grouped_df
                        w_pivot_df = pivot_df.copy()
                        for column in pivot_df.columns:
                            if column == 'Count':
                                weight_column_name = f'Weight(%)'
                                s_s_col_name = f'Sample_size_by_weight'
                                column_feature = column
                                w_pivot_df[column_feature] = pivot_df[column]
                                w_pivot_df[weight_column_name] = np.round(
                                    (pivot_df[column] / N) * 100, 4)
                                w_pivot_df[s_s_col_name] = np.round(
                                    (pivot_df[column] / N) * n)
                        pre_est_samp_df = pd.DataFrame(columns=o_df_cols)
                        o_l_df = o_df.copy()
                        st.write('')
                        for _, row in w_pivot_df.iterrows():
                            temp_indices_list = []
                            n_temp = int(row['Sample_size_by_weight'])
                            filt_w_pivot_df = o_l_df.loc[(
                                o_l_df[par_col_list] == row[par_col_list]).all(axis=1)]
                            incomplete_est_samp_rows = filt_w_pivot_df.sample(
                                n=n_temp)
                            pre_est_samp_df = pd.concat(
                                [pre_est_samp_df, incomplete_est_samp_rows])
                            temp_indices_list.extend(
                                incomplete_est_samp_rows.index.tolist())
                            o_l_df = o_l_df.drop(temp_indices_list)
                        o_merge_pre_est_df = pd.merge(
                            o_df, pre_est_samp_df, how='left', indicator=True)
                        o_minus_pre_est_df = o_merge_pre_est_df[o_merge_pre_est_df['_merge'] == 'left_only'].drop(
                            columns='_merge')
                        a_auxiliar_df = w_pivot_df['Sample_size_by_weight'].value_counts(
                        ).sort_index().reset_index()
                        a_auxiliar_df.columns = [
                            'Sample_size_by_weight', 'Count']
                        d_auxiliar_df = a_auxiliar_df.sort_values(
                            'Sample_size_by_weight', ascending=False)
                        aux_eval = pre_est_samp_df.shape[0] - n
                        if aux_eval < 0:
                            sub_a_auxiliar = pd.DataFrame(
                                columns=a_auxiliar_df.columns)
                            temp_a_auxiliar_count = 0
                            for _, row in a_auxiliar_df.iterrows():
                                count = row['Count']
                                temp_a_auxiliar_count = temp_a_auxiliar_count + count
                                sub_a_auxiliar = pd.concat(
                                    [sub_a_auxiliar, row.to_frame().T])
                                if temp_a_auxiliar_count >= abs(aux_eval):
                                    break
                            sub_a_auxiliar = sub_a_auxiliar.reset_index(
                                drop=True)
                            values_a_filter = sub_a_auxiliar['Sample_size_by_weight'].tolist(
                            )
                            a_filt_w_pivot = w_pivot_df[w_pivot_df['Sample_size_by_weight'].isin(
                                values_a_filter)].sample(n=abs(aux_eval))
                            to_fill_a_w_pivot = pd.DataFrame()
                            for _, row in a_filt_w_pivot.iterrows():
                                temp_fill = o_minus_pre_est_df.loc[(
                                    o_minus_pre_est_df[par_col_list] == row[par_col_list]).all(axis=1)].sample(n=1)
                                to_fill_a_w_pivot = pd.concat(
                                    [to_fill_a_w_pivot, temp_fill])
                            est_samp_df = pd.concat(
                                [pre_est_samp_df, to_fill_a_w_pivot])
                            st.write(
                                'Sampled Dataframe given the selected structure:')
                            st.write(est_samp_df)
                            # st.write(est_samp_df.shape)
                            structure_sampled_l_df_csv = est_samp_df.to_csv(
                                index=False)
                            coldos_est_l_1, coldos_est_l_2 = st.columns(
                                2, gap='medium')

                            with coldos_est_l_2:
                                st.download_button(label=':floppy_disk: Download Dataframe as CSV :floppy_disk:',
                                                   data=structure_sampled_l_df_csv,
                                                   file_name=f'SAMPLED_STRUCTURE_{file_name_df}.csv',
                                                   mime='text/csv')
                        if aux_eval > 0:
                            sub_d_auxiliar = pd.DataFrame(
                                columns=d_auxiliar_df.columns)
                            temp_d_auxiliar_count = 0
                            for _, row in d_auxiliar_df.iterrows():
                                count = row['Count']
                                temp_d_auxiliar_count = temp_d_auxiliar_count + count
                                sub_d_auxiliar = pd.concat(
                                    [sub_d_auxiliar, row.to_frame().T])
                                if temp_d_auxiliar_count >= abs(aux_eval):
                                    break
                            sub_d_auxiliar = sub_d_auxiliar.reset_index(
                                drop=True)
                            values_d_filter = sub_d_auxiliar['Sample_size_by_weight'].tolist(
                            )
                            d_filt_w_pivot = w_pivot_df[w_pivot_df['Sample_size_by_weight'].isin(
                                values_d_filter)].sample(n=abs(aux_eval))
                            to_rem_d_w_pivot = pd.DataFrame()
                            for _, row in d_filt_w_pivot.iterrows():
                                temp_rem = pre_est_samp_df.loc[(
                                    pre_est_samp_df[par_col_list] == row[par_col_list]).all(axis=1)].sample(n=1)
                                to_rem_d_w_pivot = pd.concat(
                                    [to_rem_d_w_pivot, temp_rem])
                            pre_merge_to_rem = pd.merge(
                                pre_est_samp_df, to_rem_d_w_pivot, how='left', indicator=True)
                            est_samp_df = pre_merge_to_rem[pre_merge_to_rem['_merge'] == 'left_only'].drop(
                                columns='_merge')
                            st.write(
                                'Sampled Dataframe given the selected structure:')
                            st.write(est_samp_df)
                            structure_sampled_g_df_csv = est_samp_df.to_csv(
                                index=False)
                            coldos_est_g_1, coldos_est_g_2 = st.columns(
                                2, gap='medium')

                            with coldos_est_g_2:
                                st.download_button(label=':floppy_disk: Download Dataframe as CSV :floppy_disk:',
                                                   data=structure_sampled_g_df_csv,
                                                   file_name=f'SAMPLED_STRUCTURE_{file_name_df}.csv',
                                                   mime='text/csv')
                        if aux_eval == 0:
                            est_samp_df = pre_est_samp_df
                            st.write(
                                'Sampled Dataframe given the selected structure:')
                            st.write(est_samp_df)
                            structure_sampled_e_df_csv = est_samp_df.to_csv(
                                index=False)
                            coldos_est_e_1, coldos_est_e_2 = st.columns(
                                2, gap='medium')

                            with coldos_est_e_2:
                                st.download_button(label=':floppy_disk: Download Dataframe as CSV :floppy_disk:',
                                                   data=structure_sampled_e_df_csv,
                                                   file_name=f'SAMPLED_STRUCTURE_{file_name_df}.csv',
                                                   mime='text/csv')

                            pivot_df = grouped_df
                            w_pivot_df = pivot_df.copy()
                            for column in pivot_df.columns:
                                if column == 'Count':
                                    weight_column_name = f'Weight(%)'
                                    s_s_col_name = f'Sample_size_by_weight'
                                    column_feature = column
                                    w_pivot_df[column_feature] = pivot_df[column]
                                    w_pivot_df[weight_column_name] = np.round(
                                        (pivot_df[column] / N) * 100, 4)
                                    w_pivot_df[s_s_col_name] = np.round(
                                        (pivot_df[column] / N) * n)
                            pre_est_samp_df = pd.DataFrame(columns=o_df_cols)
                            o_l_df = o_df.copy()
                            st.write('')
                            for _, row in w_pivot_df.iterrows():
                                temp_indices_list = []
                                n_temp = int(row['Sample_size_by_weight'])
                                filt_w_pivot_df = o_l_df.loc[(
                                    o_l_df[par_col_list] == row[par_col_list]).all(axis=1)]
                                incomplete_est_samp_rows = filt_w_pivot_df.sample(
                                    n=n_temp)
                                pre_est_samp_df = pd.concat(
                                    [pre_est_samp_df, incomplete_est_samp_rows])
                                temp_indices_list.extend(
                                    incomplete_est_samp_rows.index.tolist())
                                o_l_df = o_l_df.drop(temp_indices_list)
                            o_merge_pre_est_df = pd.merge(
                                o_df, pre_est_samp_df, how='left', indicator=True)
                            o_minus_pre_est_df = o_merge_pre_est_df[o_merge_pre_est_df['_merge'] == 'left_only'].drop(
                                columns='_merge')
                            a_auxiliar_df = w_pivot_df['Sample_size_by_weight'].value_counts(
                            ).sort_index().reset_index()
                            a_auxiliar_df.columns = [
                                'Sample_size_by_weight', 'Count']
                            d_auxiliar_df = a_auxiliar_df.sort_values(
                                'Sample_size_by_weight', ascending=False)
                            aux_eval = pre_est_samp_df.shape[0] - n
                            if aux_eval < 0:
                                sub_a_auxiliar = pd.DataFrame(
                                    columns=a_auxiliar_df.columns)
                                temp_a_auxiliar_count = 0
                                for _, row in a_auxiliar_df.iterrows():
                                    count = row['Count']
                                    temp_a_auxiliar_count = temp_a_auxiliar_count + count
                                    sub_a_auxiliar = pd.concat(
                                        [sub_a_auxiliar, row.to_frame().T])
                                    if temp_a_auxiliar_count >= abs(aux_eval):
                                        break
                                sub_a_auxiliar = sub_a_auxiliar.reset_index(
                                    drop=True)
                                values_a_filter = sub_a_auxiliar['Sample_size_by_weight'].tolist(
                                )
                                a_filt_w_pivot = w_pivot_df[w_pivot_df['Sample_size_by_weight'].isin(
                                    values_a_filter)].sample(n=abs(aux_eval))
                                to_fill_a_w_pivot = pd.DataFrame()
                                for _, row in a_filt_w_pivot.iterrows():
                                    temp_fill = o_minus_pre_est_df.loc[(
                                        o_minus_pre_est_df[par_col_list] == row[par_col_list]).all(axis=1)].sample(n=1)
                                    to_fill_a_w_pivot = pd.concat(
                                        [to_fill_a_w_pivot, temp_fill])
                                est_samp_df = pd.concat(
                                    [pre_est_samp_df, to_fill_a_w_pivot])
                                st.write(
                                    'Sampled Dataframe given the selected structure:')
                                st.write(est_samp_df)
                                structure_sampled_l_df_csv = est_samp_df.to_csv(
                                    index=False)
                                coldos_est_l_1, coldos_est_l_2 = st.columns(
                                    2, gap='medium')

                                with coldos_est_l_2:
                                    st.download_button(label=':floppy_disk: Download Dataframe as CSV :floppy_disk:',
                                                       data=structure_sampled_l_df_csv,
                                                       file_name=f'SAMPLED_STRUCTURE_{file_name_df}.csv',
                                                       mime='text/csv')
                            if aux_eval > 0:
                                sub_d_auxiliar = pd.DataFrame(
                                    columns=d_auxiliar_df.columns)
                                temp_d_auxiliar_count = 0
                                for _, row in d_auxiliar_df.iterrows():
                                    count = row['Count']
                                    temp_d_auxiliar_count = temp_d_auxiliar_count + count
                                    sub_d_auxiliar = pd.concat(
                                        [sub_d_auxiliar, row.to_frame().T])
                                    if temp_d_auxiliar_count >= abs(aux_eval):
                                        break
                                sub_d_auxiliar = sub_d_auxiliar.reset_index(
                                    drop=True)
                                values_d_filter = sub_d_auxiliar['Sample_size_by_weight'].tolist(
                                )
                                d_filt_w_pivot = w_pivot_df[w_pivot_df['Sample_size_by_weight'].isin(
                                    values_d_filter)].sample(n=abs(aux_eval))
                                to_rem_d_w_pivot = pd.DataFrame()
                                for _, row in d_filt_w_pivot.iterrows():
                                    temp_rem = pre_est_samp_df.loc[(
                                        pre_est_samp_df[par_col_list] == row[par_col_list]).all(axis=1)].sample(n=1)
                                    to_rem_d_w_pivot = pd.concat(
                                        [to_rem_d_w_pivot, temp_rem])
                                pre_merge_to_rem = pd.merge(
                                    pre_est_samp_df, to_rem_d_w_pivot, how='left', indicator=True)
                                est_samp_df = pre_merge_to_rem[pre_merge_to_rem['_merge'] == 'left_only'].drop(
                                    columns='_merge')
                                st.write(
                                    'Sampled Dataframe given the selected structure:')
                                st.write(est_samp_df)
                                structure_sampled_g_df_csv = est_samp_df.to_csv(
                                    index=False)
                                coldos_est_g_1, coldos_est_g_2 = st.columns(
                                    2, gap='medium')

                                with coldos_est_g_2:
                                    st.download_button(label=':floppy_disk: Download Dataframe as CSV :floppy_disk:',
                                                       data=structure_sampled_g_df_csv,
                                                       file_name=f'SAMPLED_STRUCTURE_{file_name_df}.csv',
                                                       mime='text/csv')
                            if aux_eval == 0:
                                est_samp_df = pre_est_samp_df
                                st.write(
                                    'Sampled Dataframe given the selected structure:')
                                st.write(est_samp_df)
                                structure_sampled_e_df_csv = est_samp_df.to_csv(
                                    index=False)
                                coldos_est_e_1, coldos_est_e_2 = st.columns(
                                    2, gap='medium')

                                with coldos_est_e_2:
                                    st.download_button(label=':floppy_disk: Download Dataframe as CSV :floppy_disk:',
                                                       data=structure_sampled_e_df_csv,
                                                       file_name=f'SAMPLED_STRUCTURE_{file_name_df}.csv',
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
