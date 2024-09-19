import streamlit as st
import requests

# Set the FastAPI endpoint
API_ENDPOINT = st.secrets["api_endpoint"]
ANKER_URL = "https://uni-tuebingen.de/de/257900"

# Streamlit Interface
def main():
    st.title("AI Ethics Navigator")

    st.markdown("""
Dieses prototypische Tool wurde im Rahmen des Projekts [**ANKER**](%s) am Internationalen Zentrum für Ethik in den Wissenschaften an der Universität Tübingen entwickelt.

**Funktionen**
- Durchsucht den Inhalt von über **200 Ethikrichtlinien und -frameworks**.
- Bietet eine automatisch generierte Volltextantwort auf gestellte Fragen.
- Stellt die relevantesten Quellen mit Metadaten bereit.

**Hinweise**
- Fragen müssen in der aktuellen Version **in englischer Sprache** formuliert werden.
- Durch ein Fragezeichen neben den Quellen können die ausgewählten Textausschnitte eingesehen werden. 
- Textausschnitte sind aktuell für den prototypischen Anwendungsfall absichtlich kurz gehalten.
""" % ANKER_URL)

    
    # Input field for the search query
    query = st.text_input("Enter your search query here:")
    
    # Search button
    if st.button("Search"):
        if query:
            # Display the loading spinner
            with st.spinner("Searching..."):
                # Send the query to the FastAPI backend
                payload = {"question": query}
                response = requests.post(API_ENDPOINT, json=payload)
                
                # Check the response status
                if response.status_code == 200:
                    results = response.json()
                    print(results)
                    display_results(results)
                else:
                    st.error(f"Error: {response.status_code} - {response.text}")
        else:
            st.warning("Please enter a search query.")


# def display_results(results):
#     # Display each result
#     st.subheader(f"Answer")
#     st.write(results["result"]["answer"])
#     context = results["result"]["context"]
#     for i, source in enumerate(context):
#         metadata = source["metadata"]
#         st.write(f"**Source {i}: {metadata['document_name']}** \nURL:{metadata['document_url'] if 'document_url' in metadata else 'N/A'} \t Page:{metadata['page'] if 'page' in metadata else 'N/A'}")
#         st.write("---")

def display_results(results):
    # Use columns for layout: answer on the left, sources on the right
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Answer")
        st.write(results["answer"])
    
    with col2:
        st.subheader("Sources")
        if results["answer"] == "The answer is not available.":
            st.write("No sources found.")
        else:
            context = results["documents"]
            for i, source in enumerate(context):
                metadata = source["metadata"]
                pub_year = int(metadata.get('year_of_publication', None)) if metadata.get('year_of_publication', None) else 'N/A'
                document_url = metadata.get('document_url', 'N/A')

                # Adding formatting and color for the source container with proper word wrapping for URLs
                st.markdown(
                    f"""
                    <div style='background-color: #f0f2f6; padding: 10px; border-radius: 5px; margin-bottom: 10px; word-wrap: break-word;'>
                        <strong>Source {i + 1}:</strong> {metadata["document_name"]}<br>
                        <strong>Institution:</strong> {metadata["institution"]}<br>
                        <strong>Year:</strong> {pub_year}<br>
                        <strong>URL:</strong> <a href='{document_url}' style='word-break: break-all;'>{document_url}</a><br>
                        <strong>Page:</strong> {metadata.get('page', 'N/A')}
                    </div>
                    """,
                    unsafe_allow_html=True,
                    help=source["page_content"]
                )
                # Adding hover tooltip for each source context text
                


if __name__ == "__main__":
    main()