import main 
import streamlit as st 

# Display the plot in the Streamlit app

# Table of Content
st.sidebar.title('Table of Content')

# 페이지 선택
page = st.sidebar.radio('Choose the page to read.',
                        ('Data', 'Tree model','Other models'))

if page == 'Data':
    st.markdown('# Lung Cancer Classification')

    with st.expander('Data description',expanded=True):  
        '''
        Dataset Characteristics: Multivariate \n 
        Subject Area: Health and Medicine \n 
        Associated Tasks: Classification \n 
        Feature type: Integer \n 
        # Instances: 32 \n 
        # Features: 56 \n 

    This data was used by Hong and Young to illustrate the power of the optimal discriminant plane even in ill-posed settings. Applying the KNN method in the resulting plane gave 77% accuracy. However, these results are strongly biased (See Aeberhard's second ref. above, or email to stefan@coral.cs.jcu.edu.au). Results obtained by Aeberhard et al. are :
    
    RDA : 62.5%, KNN 53.1%, Opt. Disc. Plane 59.4%

    The data described 3 types of pathological lung cancers. The Authors give no information on the individual variables nor on where the data was originally used.

    Notes:
    -  In the original data 4 values for the fifth attribute were -1. These values have been changed to ? (unknown). (*)
    -  In the original data 1 value for the 39 attribute was 4.  This value has been changed to ? (unknown). (*)
        '''

if page == 'Tree model':
    with st.expander('Summary',expanded=True):
        '''
    Model: DTC(Decision Tree Classifier)

    GridSearch?: Yes \n
        parameter grid: \n
         1) 'ccp_alpha': np.linspace(0, 0.1, 5)\n
         2) 'max_depth': [None, 3, 5]\n
        cv: StratifiedKFold 
    
    '''
        st.markdown('When using "scoring=accuracy":')
        st.markdown(f'Best cost-complexity alpha: {main.best_alpha}')
        st.markdown(f'Best max-depth: {main.best_depth}') 
        st.markdown(f'Best accuracy score: {main.best_score}')    
    '''\n
    Here are interactive 3D-graphs for you. 
    '''
    st.write(main.fig)

    st.write(main.fig2)

    st.write(main.fig3)


if page == 'Other models':
    st.markdown("Here are results from alternative models:")

    button_status = False
    if st.button('Click to import result of other models',help='It will take 5-15 minutes') == True :
        button_status = True
            # 스피너 표시
        with st.spinner('Running the process...'):
            # 파일 import하는 함수 호출
            import other 
            time.sleep(2)  # 예시로 2초 대기

        # 스피너 종료
        st.success('Thank you for waiting. Process Completed!')

            # 결과물 가져오기 
        with st.expander('Random Forest', expanded=True): 
            st.markdown(f'Best parameters: {other.best_param_rf}') 
            st.markdown(f'Train accuracy: {other.Train_acc_rf}') 
            st.markdown(f'Test accuracy: {other.Test_acc_rf}')  
        
        with st.expander('XGBoost', expanded=True): 
            st.markdown(f'Best parameters: {other.best_param_xgb}') 
            st.markdown(f'Train accuracy: {other.Train_acc_xgb}') 
            st.markdown(f'Test accuracy: {other.Test_acc_xgb}') 

        with st.expander('SVC', expanded=True): 
            st.markdown(f'Best parameters: {other.best_param_svc}') 
            st.markdown(f'Train accuracy: {other.Train_acc_svc}') 
            st.markdown(f'Test accuracy: {other.Test_acc_svc}') 


    if button_status == True: 
        st.button('Click to import result of other models',help='It will take 5-15 minutes', disabled=False) 

    st.write('The process may take 5-15 mintues.') 
    st.markdown("---")







    





