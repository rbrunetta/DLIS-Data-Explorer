import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def data(dlis_file):
    st.header('Data Information and Visualization')

    if 'selected_curves' not in st.session_state:
        st.session_state.selected_curves = []
    
    if 'logical_file_dfs' not in st.session_state:
        st.session_state.logical_file_dfs = {}

    DEPTH_MNEMONICS = ['TDEP', 'DEPT', 'DEPTH', 'MD', 'TVD']

    logical_files = list(dlis_file)
    
    if logical_files:
        st.subheader("1 - Select a Logical File")
        logical_files_dict = {f"Logical File {i+1}": lf for i, lf in enumerate(logical_files)}
        logical_file_selection = st.selectbox('Logical Files', list(logical_files_dict.keys()))
        
        if logical_file_selection:
            selected_logical_file = logical_files_dict[logical_file_selection]
            
            if hasattr(selected_logical_file, 'frames'):
                frames = selected_logical_file.frames
                
                if frames:
                    st.subheader("2 - Select a Frame")
                    frame_names = [f"Frame {i+1}" for i in range(len(frames))]
                    frame_selection = st.selectbox('Frames', frame_names)
                    
                    if frame_selection:
                        selected_frame_index = int(frame_selection.split(' ')[1]) - 1
                        selected_frame = frames[selected_frame_index]
                        
                        data_dict = {}
                        
                        for channel in selected_frame.channels:
                            try:
                                values = channel.curves()
                                if np.ndim(values) == 1 and values is not None:
                                    values = np.where(values == -999.25, np.nan, values)
                                    data_dict[channel.name] = values
                                else:
                                    st.write(f"***{channel.name} - no data or multiple dimensions (ignored)***")
                            except Exception as e:
                                st.write(f"Error loading channel {channel.name}: {e}")
                        
                        df = pd.DataFrame(data_dict)
                        
                        logical_file_key = f"{logical_file_selection} - {frame_selection}"
                        st.session_state.logical_file_dfs[logical_file_key] = df
                        st.session_state.df = df
                        
                        if not df.empty:
                            depth_column = None
                            for col in df.columns:
                                if col in DEPTH_MNEMONICS:
                                    if df[col].is_monotonic_increasing or df[col].is_monotonic_decreasing:
                                        depth_column = col
                                        break
                            
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
                                depth_unit = 'index'
                                st.warning("No depth channel selected. Using sample index as Y-axis.")
                            else:
                                depth_column = selected_depth
                                depth_channel = next((ch for ch in selected_frame.channels if ch.name == depth_column), None)
                                depth_unit = depth_channel.units if depth_channel and hasattr(depth_channel, 'units') else 'unknown'
                                if not depth_unit:
                                    depth_unit = 'unknown'
                                st.write(f"Depth channel unit: {depth_unit}")

                            st.session_state.depth_column = depth_column

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
                                
                                col_left, col_center, col_right = st.columns([0.5, 4, 0.5])
                                
                                with col_center:
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
                            st.write("No channels with valid data found in this Frame.")
                else:
                    st.write('There is no Frame in this Logical File.')
            else:
                st.write('The selected Logical File has no frames.')
    else:
        st.write('No Logical File available in DLIS file.')