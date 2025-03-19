import streamlit as st
from dlisio import dlis
import tempfile
import base64

import info
import data
import export

st.set_page_config(layout="wide", page_title='DLIS Data Explorer')

# Função para converter a imagem em base64
def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode('utf-8')

# Converter a imagem do QR Code para base64
qr_code_base64 = get_base64_image("QR-CODE_PIX.png")

# Funções
# Função para carregar o arquivo DLIS
def dlis_load(uploaded_file):
    if uploaded_file is not None:
        st.session_state.uploaded_file_name = uploaded_file.name
        try:
            with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
                tmp_file.write(uploaded_file.read())
                tmp_file_path = tmp_file.name
            dlis_file = dlis.load(tmp_file_path)
            
            # Verificar se o arquivo foi carregado corretamente
            if dlis_file:
                st.sidebar.success('File Loaded Successfully!')
                st.sidebar.write(f"Number of Logical Files: {len(dlis_file)}")
            else:
                st.sidebar.error('Failed to load DLIS file.')
            
            return dlis_file
        except Exception as e:
            st.error(f"Error loading DLIS file: {e}")
            return None
    else:
        st.warning("Please, select a DLIS file.")
        return None

# Página "Home" (página inicial)
def home_page():
    st.title("Welcome to DLIS Data Explorer")
    st.write("""
    **DLIS Data Explorer** is a Streamlit-based application designed to help you explore and analyze DLIS files, 
    which are commonly used in the oil and gas industry for storing well log data. 
    With this app, you can:
    - View general information about the DLIS file.
    - Explore the data contained in the file.
    - Visualize geophysical well log curves.
    - Export the data to LAS format.
    """)
    
    st.markdown("### How to use:")
    st.write("""
    1. Upload a DLIS file using the file upload option in the sidebar.
    2. Navigate to the desired page in the menu.
    3. Select the curve(s) you want to visualize and export (LAS).
    4. Have fun!
    """)
    
    st.markdown("### About the Developer")
    st.write("""
    Hi, I'm Rodrigo Bruneta, a geologist, geophysicist and data scientist with experience in petroleum research
    and exploration. My passion for these three fields has led me to discover how programming can enhance our knowledge of the geosciences.
    Feel free to contact me or check out my other projects:
    """)
    
    # Adicionar ícones clicáveis lado a lado
    col_left, col_center, col_right = st.columns([1, 3, 1])
    
    with col_center:
        st.markdown("""
            <div style="display: flex; justify-content: center; align-items: center; gap: 20px; margin-top: 20px;">
                <!-- Email -->
                <a href="mailto:rbrunetta@gmail.com" target="_blank">
                    <img src="https://img.icons8.com/ios-filled/50/ffffff/email.png" alt="Email" width="40" height="40" />
                </a>
                <!-- GitHub -->
                <a href="https://github.com/rbrunetta" target="_blank">
                    <img src="https://img.icons8.com/ios-filled/50/ffffff/github.png" alt="GitHub" width="40" height="40" />
                </a>
                <!-- LinkedIn -->
                <a href="https://linkedin.com/in/rodrigo-brunetta" target="_blank">
                    <img src="https://img.icons8.com/ios-filled/50/ffffff/linkedin.png" alt="LinkedIn" width="40" height="40" />
                </a>
                <!-- Lattes -->
                <a href="http://lattes.cnpq.br/1976460566524791" target="_blank">
                    <img src="https://www.gov.br/observatorio/pt-br/assuntos/programas-academicos/imagens/Lattes.png/@@images/image" alt="Lattes" width="40" height="40" style="filter: invert(100%);" />
                </a>
                <!-- YouTube -->
                <a href="https://www.youtube.com/@GeoDataScience-br" target="_blank">
                    <img src="https://img.icons8.com/ios-filled/50/ffffff/youtube-play.png" alt="YouTube" width="40" height="40" />
                </a>
            </div>
        """, unsafe_allow_html=True)
    
    # Seção de Doações
    st.markdown("### Support the Project")
    # Adicionar margem inferior à frase
    st.markdown("""
        <div style="margin-bottom: 50px;">
            If you find this app useful, consider supporting its development through PayPal or PIX:
        </div>
    """, unsafe_allow_html=True)
    
    # Criar colunas para centralizar os elementos de doação
    col_left, col_center, col_right = st.columns([1, 3, 1])
    
    with col_center:
        # Criar subcolunas para PayPal e PIX lado a lado
        col_paypal, col_pix = st.columns(2)
        
        with col_paypal:
            # Usar um contêiner com CSS para centralizar verticalmente
            st.markdown("""
                <div style="display: flex; flex-direction: column; justify-content: center; align-items: center; height: 250px;">
                    <h4 style="margin-bottom: 10px;">Donate via PayPal</h4>
                    <a href="https://www.paypal.com/donate?hosted_button_id=8X72NWMWHVWAN" target="_blank">
                        <img src="https://www.paypalobjects.com/en_US/i/btn/btn_donate_LG.gif" alt="Donate with PayPal button" title="PayPal - The safer, easier way to pay online!" />
                    </a>
                </div>
            """, unsafe_allow_html=True)
        
        with col_pix:
            # Usar um contêiner com CSS para centralizar verticalmente
            st.markdown(f"""
                <div style="display: flex; flex-direction: column; justify-content: center; align-items: center; height: 250px;">
                    <h4 style="margin-bottom: 10px;">Donate via PIX</h4>
                    <img src="data:image/png;base64,{qr_code_base64}" width="200" alt="PIX QR Code" />
                    <p style="margin-top: 10px;">Scan the QR Code to donate.</p>
                </div>
            """, unsafe_allow_html=True)

# Interface Streamlit
st.sidebar.title('DLIS Data Explorer')
st.sidebar.write('Load your DLIS file using the file upload option below')

uploaded_file = st.sidebar.file_uploader('DLIS File', type=['.dlis'], help='DLIS File is a binary file format for well logs, developed by Schlumberger in the late 80s and published by the American Petroleum Institute (API) in 1991.')

if uploaded_file:
    dlis_file = dlis_load(uploaded_file)
else:
    dlis_file = None
    
# Menu lateral
st.sidebar.title('Menu')
options = st.sidebar.radio('Pages', options=['Home', 'General Information', 'Data Visualization', 'Export'])

# Navegação entre páginas
if options == 'Home':
    home_page()
elif dlis_file:
    if options == 'General Information':
        info.info(dlis_file)
    elif options == 'Data Visualization':
        data.data(dlis_file)
    elif options == 'Export':
        export.export()
else:
    if options != 'Home':
        st.warning("Please, upload a DLIS file to access this page.")