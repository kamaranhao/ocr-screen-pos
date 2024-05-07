ERROR_MSG = """
Foi :red[detectado um problema de placa (**{}**)] na sua máquina!  
Confirme se o número de série é **{}**
"""

import easyocr
import io
import numpy as np
import streamlit as st

from PIL import Image
from pillow_heif import register_heif_opener


register_heif_opener()

st.set_page_config(page_title="GetClick", layout="wide")

st.markdown("# GetClick!")
st.caption("Oi! Como podemos te ajudar hoje?")
st.divider()

if "reader" not in st.session_state:
    st.session_state.reader = easyocr.Reader(
        ["en"],
        gpu=False,
        model_storage_directory=".",
    )

uploaded_img = st.file_uploader("Imagem")
if uploaded_img is not None:
    bytes_data = uploaded_img.getvalue()
    image = np.asarray(Image.open(io.BytesIO(bytes_data)))
    result = st.session_state.reader.readtext(image)

    image_text = [_[1].lower() for _ in result]
    error_detected = False
    sn_index = None
    tamper_index = None

    for i, text in enumerate(image_text):
        if "sn" in text:
            sn_index = i + 1

        if "tamper" in text:
            error_detected = True
            tamper_index = i

    if error_detected:
        st.divider()
        st.markdown(ERROR_MSG.format(image_text[tamper_index], image_text[sn_index]))
        st.button("Confirmar", type="primary", use_container_width=True)
