import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def data(dlis_file):
    st.header('Data Information and Visualization')

    # Inicializar a lista de curvas selecionadas para exportação
    if 'selected_curves' not in st.session_state:
        st.session_state.selected_curves = []
    
    # Inicializar o dicionário para armazenar os DataFrames por Logical File
    if 'logical_file_dfs' not in st.session_state:
        st.session_state.logical_file_dfs = {}

    # Lista de mnemônicos comuns para profundidade
    DEPTH_MNEMONICS = ['TDEP', 'DEPT', 'DEPTH', 'MD', 'TVD']

    # Criar uma lista dos arquivos lógicos
    logical_files = list(dlis_file)
    
    if logical_files:
        # Seleção do Logical File
        st.subheader("1 - Select a Logical File")
        logical_files_dict = {f"Logical File {i+1}": lf for i, lf in enumerate(logical_files)}
        logical_file_selection = st.selectbox('Logical Files', list(logical_files_dict.keys()))
        
        if logical_file_selection:
            selected_logical_file = logical_files_dict[logical_file_selection]
            
            # Acessar os frames do Logical File selecionado
            if hasattr(selected_logical_file, 'frames'):
                frames = selected_logical_file.frames
                
                if frames:
                    # Seleção do Frame
                    st.subheader("2 - Select a Frame")
                    frame_names = [f"Frame {i+1}" for i in range(len(frames))]
                    frame_selection = st.selectbox('Frames', frame_names)
                    
                    if frame_selection:
                        selected_frame_index = int(frame_selection.split(' ')[1]) - 1
                        selected_frame = frames[selected_frame_index]
                        
                        # Criar um dicionário para armazenar os dados dos channels
                        data_dict = {}
                        
                        # Extrair os dados dos channels
                        for channel in selected_frame.channels:
                            try:
                                values = channel.curves()
                                if np.ndim(values) == 1 and values is not None:
                                    values = np.where(values == -999.25, np.nan, values)
                                    data_dict[channel.name] = values
                                else:
                                    st.write(f"***{channel.name} - no data or multiple dimensions (ignored)***")
                            except Exception as e:
                                st.write(f"Erro ao carregar o canal {channel.name}: {e}")
                        
                        # Criar um DataFrame com os dados válidos
                        df = pd.DataFrame(data_dict)
                        
                        # Armazenar o DataFrame no dicionário com a chave sendo o Logical File e Frame
                        logical_file_key = f"{logical_file_selection} - {frame_selection}"
                        st.session_state.logical_file_dfs[logical_file_key] = df
                        st.session_state.df = df  # Manter o df atual para visualização
                        
                        if not df.empty:
                            # Tentar identificar a curva de profundidade automaticamente
                            depth_column = None
                            for col in df.columns:
                                if col in DEPTH_MNEMONICS:
                                    if df[col].is_monotonic_increasing or df[col].is_monotonic_decreasing:
                                        depth_column = col
                                        break
                            
                            # Se não encontrar automaticamente, permitir que o usuário escolha
                            st.subheader("3 - Select Depth Channel")
                            depth_options = ['Auto (index)'] + list(df.columns)
                            selected_depth = st.selectbox(
                                'Select the depth channel (used as Y-axis)',
                                depth_options,
                                index=depth_options.index(depth_column) if depth_column else 0,
                                help="Choose the channel representing depth. Select 'Auto (index)' to use sample numbers."
                            )
                            
                            if selected_depth == 'Auto (index)':
                                df['INDEX'] = range(len(df))
                                depth_column = 'INDEX'
                                depth_unit = 'index'  # Unidade fictícia para o índice
                                st.warning("No depth channel selected. Using sample index as Y-axis.")
                            else:
                                depth_column = selected_depth
                                # Identificar a unidade do canal de profundidade
                                depth_channel = next((ch for ch in selected_frame.channels if ch.name == depth_column), None)
                                depth_unit = depth_channel.units if depth_channel and hasattr(depth_channel, 'units') else 'unknown'
                                if not depth_unit:
                                    depth_unit = 'unknown'
                                st.write(f"Depth channel unit: {depth_unit}")

                            # Armazenar o depth_column no st.session_state
                            st.session_state.depth_column = depth_column

                            # Seleção da Curva
                            st.subheader("4 - Select Channel and press button to save")
                            curve_names = [col for col in df.columns if col != depth_column]
                            curve_selection = st.selectbox('Channels', curve_names)
                            
                            if curve_selection:
                                curve_already_selected = any(
                                    curve_info['curve'] == curve_selection and
                                    curve_info['logical_file'] == logical_file_selection and
                                    curve_info['frame'] == frame_selection
                                    for curve_info in st.session_state.selected_curves
                                )
                                
                                if st.button(f"Press to select {curve_selection}"):
                                    if not curve_already_selected:
                                        st.session_state.selected_curves.append({
                                            'curve': curve_selection,
                                            'logical_file': logical_file_selection,
                                            'frame': frame_selection,
                                            'depth_column': depth_column,
                                            'depth_unit': depth_unit,
                                            'logical_file_key': logical_file_key
                                        })
                                        st.success(f"Channel {curve_selection} selected successfully!")
                                    else:
                                        st.warning(f"Channel {curve_selection} was already selected from {logical_file_selection}, {frame_selection}!")
                                
                                # Criar três colunas: margens laterais e conteúdo central
                                col_left, col_center, col_right = st.columns([0.5, 4, 0.5])
                                
                                with col_center:
                                    # Criar duas subcolunas para gráfico e tabela
                                    col1, col2 = st.columns([2, 1])
                                    
                                    with col1:
                                        with st.container():
                                            st.subheader(f'Channel {curve_selection}')
                                            fig, ax = plt.subplots(figsize=(2, 5))
                                            ax.plot(df[curve_selection], df[depth_column], label=curve_selection, linewidth=0.5, color='blue')
                                            
                                            channel = next((ch for ch in selected_frame.channels if ch.name == curve_selection), None)
                                            unit = channel.units if channel and hasattr(channel, 'units') else ''
                                            depth_unit_display = depth_unit if depth_unit != 'index' else ''
                                            
                                            ax.set_xlabel(f'{curve_selection} ({unit})', fontsize=5)
                                            ax.set_ylabel(f'Depth ({depth_column}) ({depth_unit_display})', fontsize=4)
                                            ax.set_title(f'{curve_selection}', fontsize=6)
                                            ax.grid(True)
                                            ax.tick_params(axis='both', which='major', labelsize=4)
                                            if depth_column != 'INDEX':
                                                ax.invert_yaxis()
                                            st.pyplot(fig, use_container_width=False)
                                    
                                    with col2:
                                        st.subheader(f'Channel {curve_selection} Statistics')
                                        stats = df[curve_selection].describe()
                                        st.table(stats)
                        else:
                            st.write("Nenhum channel com dados válidos encontrado neste Frame.")
                else:
                    st.write('Nenhum Frame disponível neste Logical File.')
            else:
                st.write('O Logical File selecionado não possui frames.')
    else:
        st.write('Nenhum Logical File disponível no DLIS.')