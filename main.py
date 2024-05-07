ERROR_MSG = """
Foi :red[detectado um problema] na sua máquina!  
Confirme se o número de série é **{}**
"""

import easyocr
import matplotlib.pyplot as plt
import streamlit as st


st.set_page_config(page_title="GetClick", layout="wide")

st.markdown("# GetClick!")
st.caption("Oi! Como podemos te ajudar hoje?")
st.divider()

if "reader" not in st.session_state:
    st.session_state.reader = easyocr.Reader(["en"])

uploaded_img = st.file_uploader("Imagem")
if uploaded_img is not None:
    bytes_data = uploaded_img.getvalue()
    result = st.session_state.reader.readtext(bytes_data)

    image_text = [_[1].lower() for _ in result]
    error_detected = False
    sn_index = None

    for i, text in enumerate(image_text):
        if "sn" in text:
            sn_index = i + 1

        if "tamper" in text:
            error_detected = True

    if error_detected:
        st.divider()
        st.markdown(ERROR_MSG.format(image_text[sn_index]))
        st.button("Confirmar", type="primary", use_container_width=True)


# # Create image result
# fig = plt.figure(figsize=(15, 15))
# im = plt.imread(filename)
# plt.imshow(im)

# for _ in result:
#     x = [n[0] for n in _[0]]
#     y = [n[1] for n in _[0]]
#     plt.fill(x, y, facecolor="none", edgecolor="red")
#     plt.text(x[0], y[0] - 5, f"{_[1]} ({_[2] * 100:.2f}%)", color="red", fontsize=12)

# plt.axis("off")
# plt.show()
