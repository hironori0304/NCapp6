import streamlit as st
import pandas as pd
from datetime import datetime

# データフレームを初期化
def init_df():
    data = {'食品名': [], 'エネルギー': [], 'たんぱく質': [], '脂質': [], '炭水化物': [], '食塩': [], '単価': []}
    return pd.DataFrame(data)

       
        
# Streamlitアプリを設定
st.title('栄養価計算')  # 栄養価計算ページをトップページとして表示

# ページ選択用のセレクトボックスを配置
selected_page = st.sidebar.selectbox("ページを選択", ["栄養価計算", "食品データベース"])  # 選択に応じて表示ページを変更

# 栄養価計算ページの要素
if selected_page == "栄養価計算":
    st.sidebar.title(f'{selected_page} - メニュー')
    st.sidebar.subheader('栄養価の計算')
    # 栄養価計算のコードをここに記述

    # セッション状態を管理するための初期化
    if 'result_df' not in st.session_state:
        st.session_state['result_df'] = pd.DataFrame(columns=['食品名', '重量（g）', 'エネルギー（kcal）', 'たんぱく質（g）', '脂質（g）', '炭水化物（g）', '食塩（g）', '単価（円）'])
        st.session_state['reset_clicked'] = False  # 初期状態ではリセットボタンがクリックされていない状態とします

    # サイドバーにウィジェットを配置
    uploaded_file = st.sidebar.file_uploader('食品データベースをアップロード', type='csv')
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.sidebar.markdown('### 登録済み食品リスト')
        selected_food = st.sidebar.selectbox('食品を選択', df['食品名'].unique())

        # 重量の入力ウィジェットを配置
        weight = st.sidebar.number_input('重量（g）', min_value=0.0, format='%f')

        if st.sidebar.button('登録') and weight > 0:
            # 選択した食品の情報を取得
            selected_food_info = df[df['食品名'] == selected_food].iloc[0]
            
            # 栄養価の計算
            energy = selected_food_info['エネルギー'] * weight / 100
            protein = selected_food_info['たんぱく質'] * weight / 100
            fat = selected_food_info['脂質'] * weight / 100
            carbs = selected_food_info['炭水化物'] * weight / 100
            salt = selected_food_info['食塩'] * weight / 100
            price = selected_food_info['単価'] * weight / 100

            # 登録したデータをDataFrameに追加
            new_row = pd.DataFrame({
                '食品名': [selected_food],
                '重量（g）': [weight],
                'エネルギー（kcal）': [energy],
                'たんぱく質（g）': [protein],
                '脂質（g）': [fat],
                '炭水化物（g）': [carbs],
                '食塩（g）': [salt],
                '単価（円）': [price]
            })
            st.session_state['result_df'] = pd.concat([st.session_state['result_df'], new_row], ignore_index=True)

    # 登録した表をメイン画面に表示
    st.subheader('登録済みデータ')
    if 'result_df' in st.session_state:
        # 行を選択するためのチェックボックスを追加
        rows_to_delete = st.session_state['result_df'].index.tolist()
        checked_rows = st.checkbox("全て選択")
        if checked_rows:
            rows_to_delete = st.session_state['result_df'].index.tolist()
        else:
            rows_to_delete = st.multiselect('削除する行を選択', st.session_state['result_df'].index.tolist())

        # チェックされた行を削除
        if st.button('選択した行を削除'):
            st.session_state['result_df'] = st.session_state['result_df'].drop(rows_to_delete)
            st.success('選択した行が削除されました。')

        # 登録したデータを表示
        st.dataframe(st.session_state['result_df'])

        # 保存ボタンを追加
        if st.button('登録済みデータを保存'):
            # ファイル名を現在の日付と時間に設定
            now = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
            filename = f'nutrition_data_{now}.csv'
            # 登録済みデータをCSVファイルとして保存
            st.session_state['result_df'].to_csv(filename, index=False)
            st.success(f'登録済みデータが {filename} として保存されました。')

        # 合計を計算
        total_energy = st.session_state['result_df']['エネルギー（kcal）'].sum()
        total_protein = st.session_state['result_df']['たんぱく質（g）'].sum()
        total_fat = st.session_state['result_df']['脂質（g）'].sum()
        total_carbs = st.session_state['result_df']['炭水化物（g）'].sum()
        total_salt = st.session_state['result_df']['食塩（g）'].sum()
        total_price = st.session_state['result_df']['単価（円）'].sum()

        # 合計を表で表示
        st.write('### 合計')
        total_row = pd.DataFrame({
            '食品名': ['合計'],
            '重量（g）': [''],
            'エネルギー（kcal）': [total_energy],
            'たんぱく質（g）': [total_protein],
            '脂質（g）': [total_fat],
            '炭水化物（g）': [total_carbs],
            '食塩（g）': [total_salt],
            '単価（円）': [total_price]
        })

        # 登録データと合計を組み合わせた表を作成
        combined_table = pd.concat([st.session_state['result_df'], total_row])
        st.dataframe(combined_table)

        # 保存ボタンを追加
        if st.button('登録済みデータと合計を保存'):
            # ファイル名を現在の日付と時間に設定
            now = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
            filename = f'nutrition_data_{now}.csv'
            # 登録済みデータをCSVファイルとして保存
            st.session_state['result_df'].to_csv(filename, index=False)
            st.success(f'登録済みデータが {filename} として保存されました。')
 
elif selected_page == "食品データベース":
    st.sidebar.title(f'{selected_page} - メニュー')
    st.sidebar.subheader('食品成分の登録')
    food_name = st.sidebar.text_input('食品名')
    energy = st.sidebar.number_input('エネルギー', min_value=0.0, step=0.1, format="%.1f")
    protein = st.sidebar.number_input('たんぱく質', min_value=0.0, step=0.1, format="%.1f")
    fat = st.sidebar.number_input('脂質', min_value=0.0, step=0.1, format="%.1f")
    carbs = st.sidebar.number_input('炭水化物', min_value=0.0, step=0.1, format="%.1f")
    salt = st.sidebar.number_input('食塩', min_value=0.0, step=0.1, format="%.1f")
    price = st.sidebar.number_input('単価', min_value=0.0, step=0.01, format="%.1f")
    reset_button = st.sidebar.button('リセット')
    register_button = st.sidebar.button('食品成分を登録')
    uploaded_file = st.sidebar.file_uploader('食品成分の一覧表をアップロードする', type=['csv'])

    # データフレームを取得
    df = st.session_state.get('food_df', None)

    # データフレームがない場合は初期化
    if df is None:
        df = init_df()
        st.session_state['food_df'] = df

    # 食品成分を登録する関数
    def register_food(food_name, energy, protein, fat, carbs, salt, price):
        df.loc[len(df)] = [food_name, energy, protein, fat, carbs, salt, price]
        st.session_state['food_df'] = df

    # 登録ボタンがクリックされたら食品成分を登録
    if register_button:
        if food_name != '':
            register_food(food_name, energy, protein, fat, carbs, salt, price)

    # リセットボタンがクリックされたらデータフレームをリセット
    if reset_button:
        st.session_state['food_df'] = init_df()
            
            
    # 登録された食品成分を表示する
    st.subheader('登録された食品成分:')
    st.write(df)

    # 保存ボタンがクリックされたら食品成分の一覧表を保存
    if st.button('食品成分の一覧表を保存'):
        filename = 'food_list.csv'
        df.to_csv(filename, index=False)
        st.success(f'{filename} が保存されました。')

    # アップロードされたファイルがあれば読み込み、結合して表示
    if uploaded_file is not None:
        uploaded_df = pd.read_csv(uploaded_file)
        combined_df = pd.concat([df, uploaded_df], ignore_index=True)
        st.subheader('新しい食品成分一覧:')
        st.write(combined_df)

        # 保存ボタンがクリックされたら結合した食品成分一覧表を保存
        if st.button('新しい食品成分一覧表を保存'):
            combined_filename = 'combined_food_list.csv'
            combined_df.to_csv(combined_filename, index=False)
            st.success(f'{combined_filename} が保存されました。')

