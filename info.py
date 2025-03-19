import streamlit as st
import pandas as pd

def info(dlis_file):
    st.title('General Information')
    st.write('Select an option to expand and view details.')

    logical_files = list(dlis_file)
    
    if logical_files:
        logical_files_dict = {f"Logical File {i+1}": lf for i, lf in enumerate(logical_files)}
        
        with st.expander('Logical Files', expanded=False):
            logical_file_selection = st.selectbox('Select one Logical File', list(logical_files_dict.keys()))
            if logical_file_selection:
                selected_logical_file = logical_files_dict[logical_file_selection]
                st.write(selected_logical_file.describe())
        
        with st.expander('Origins', expanded=False):
            logical_file_selection = st.selectbox('Select one Logical File for Origins', list(logical_files_dict.keys()))
            if logical_file_selection:
                selected_logical_file = logical_files_dict[logical_file_selection]
                st.subheader('Origins')
                if hasattr(selected_logical_file, 'origins'):
                    origins = selected_logical_file.origins
                    if origins:
                        for origin in origins:
                            st.write(origin.describe())
                    else:
                        st.write('Origin not found!')
                else:
                    st.write('Origin not found!')
        
        with st.expander('Frames', expanded=False):
            logical_file_selection = st.selectbox('Select one Logical File for Frames', list(logical_files_dict.keys()))
            if logical_file_selection:
                selected_logical_file = logical_files_dict[logical_file_selection]
                st.subheader('Frames')
                if hasattr(selected_logical_file, 'frames'):
                    frames = selected_logical_file.frames
                    if frames:
                        for frame in frames:
                            st.write(frame.describe())
                    else:
                        st.write('Frame not found!')
                else:
                    st.write('Frame not found!')
        
        with st.expander('Channels', expanded=False):
            logical_file_selection = st.selectbox('Select one Logical File for Channels', list(logical_files_dict.keys()))
            if logical_file_selection:
                selected_logical_file = logical_files_dict[logical_file_selection]
                st.subheader('Channels')
                if hasattr(selected_logical_file, 'channels'):
                    channels = selected_logical_file.channels
                    if channels:
                        channel_data = [
                            {'Name': channel.name, 'Units': channel.units, 'Description': channel.long_name}
                            for channel in channels
                        ]
                        st.table(pd.DataFrame(channel_data))
                        st.write(f"There are {len(channels)} available logs")
                    else:
                        st.write('Channels not found!')
                else:
                    st.write('Channels not found!')
    else:
        st.write('Logical File not found!')