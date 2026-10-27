"""Service 1: Explore artworks using the Metropolitan Museum of Art Open API."""
import requests
import streamlit as st

SEARCH_URL = "https://collectionapi.metmuseum.org/public/collection/v1.1/search"
OBJECT_URL = "https://collectionapi.metmuseum.org/public/collection/v1/objects"

st.set_page_config(page_title="Explore Artworks", page_icon="🎨", layout="wide")
st.title("🎨 Explore Artworks")
st.caption("Arts and Advanced Big Data | Open API — Service 1")
st.write("Search The Metropolitan Museum of Art collection and discover artworks.")

@st.cache_data(ttl=3600, show_spinner=False)
def search_ids(query: str, limit: int) -> list[int]:
    response = requests.get(
        SEARCH_URL,
        params={"q": query, "hasImages": "true", "limit": limit},
        timeout=15,
    )
    response.raise_for_status()
    return response.json().get("objectIDs") or []

@st.cache_data(ttl=3600, show_spinner=False)
def get_object(object_id: int) -> dict:
    response = requests.get(f"{OBJECT_URL}/{object_id}", timeout=15)
    response.raise_for_status()
    return response.json()

query = st.text_input("Search for Artworks", value="flower")
count = st.slider("How many artworks to show", min_value=3, max_value=12, value=6)

if not query.strip():
    st.info("Enter a word to search the collection.")
else:
    try:
        with st.spinner("Searching the museum collection..."):
            ids = search_ids(query.strip(), count)
            artworks = []
            for object_id in ids:
                try:
                    art = get_object(object_id)
                except requests.RequestException:
                    continue
                if art.get("primaryImageSmall"):
                    artworks.append(art)

        if not artworks:
            st.info("No artworks found. Try another word, such as flower, cat, ocean, or gold.")
        else:
            cols = st.columns(3)
            for i, art in enumerate(artworks):
                with cols[i % 3]:
                    st.image(art["primaryImageSmall"], use_container_width=True)
                    st.markdown(f"**{art.get('title') or 'Untitled'}**")
                    st.write(f"Artist: {art.get('artistDisplayName') or 'Unknown'}")
                    st.write(f"Year: {art.get('objectDate') or 'Unknown'}")
                    if art.get("objectURL"):
                        st.markdown(f"[View at the Met]({art['objectURL']})")
                    st.divider()
    except (requests.RequestException, ValueError, KeyError):
        st.error("The museum service is temporarily unavailable. Please try again later.")

st.caption("Data: The Metropolitan Museum of Art Collection API (Open Access, CC0).")
