import streamlit as st
from streamlit_option_menu import option_menu
from apps import home, classify  # import your app modules here

st.set_page_config(page_title="Smart Travel", layout="wide")

# A dictionary of apps in the format of {"App title": "App icon"}
# More icons can be found here: https://icons.getbootstrap.com

def main():
    if "page" not in st.session_state:
        # Initialize session state.
        st.session_state.update({
            # Default page.
            "page": "home",
        })
        

apps = [
    {"func": home.app, "title": "Home", "icon": "house"},
    {"func": classify.app, "title": "Classify", "icon": "map"},
]

titles = [app["title"] for app in apps]
titles_lower = [title.lower() for title in titles]
icons = [app["icon"] for app in apps]

params = st.experimental_get_query_params()

if "page" in params:
    default_index = int(titles_lower.index(params["page"][0].lower()))
else:
    default_index = 0

with st.sidebar:
    st.sidebar.image("Dream Green.png", use_column_width=True)
    selected = option_menu(
    "Main Menu",
    options=titles,
    icons=icons,
    menu_icon="cast",
    default_index=default_index,
    )
    st.sidebar.title("Team")
    st.sidebar.info(
    """
        1. Jainy Shah
        2. Mihir Rambhia
        3. Mahir Bhatt
    """
    )
  

for app in apps:
    if app["title"] == selected:
        app["func"]()
        break
