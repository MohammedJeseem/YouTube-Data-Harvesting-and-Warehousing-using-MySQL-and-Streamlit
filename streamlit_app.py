import streamlit as st
from st_pages import add_page_title, get_nav_from_toml
from PIL import Image

def set_page_config_once():
    if 'page_config_set' not in st.session_state:
        st.session_state.page_config_set = False

    if not st.session_state.page_config_set:
        icon = Image.open("images/youtube.png")
        st.set_page_config(
            page_title='YouTube Data Harvesting and Warehousing',
            page_icon=icon,
            layout='wide',
            initial_sidebar_state='expanded',
            menu_items={
                'About': '''This Streamlit application was developed by Mohammed Jeseem .M
                            E-mail: mohammedjezeem786@gmail.com'''
            }
        )
        st.session_state.page_config_set = True

def main():
    set_page_config_once()

    # Sidebar toggle for sections
    sections = st.sidebar.checkbox("Sections", value=True, key="use_sections")

    # Get navigation from the corresponding .toml file
    nav_file = ".streamlit/pages_sections.toml" if sections else ".streamlit/pages.toml"
    nav = get_nav_from_toml(nav_file)

    # Display logo
    # st.sidebar.image("images/logo.png")

    # Navigation
    pg = st.navigation(nav)
    add_page_title(pg)

    # Run the page
    pg.run()

if __name__ == "__main__":
    main()
