import streamlit as st
from streamlit.logger import get_logger
import subprocess
from PIL import Image

def run_script(script_name):
    subprocess.run(["streamlit", "run", script_name])

LOGGER = get_logger(__name__)

def run():
    st.set_page_config(
        page_title="Home",
        page_icon="logo/logo.png",  # Set your logo image as the page icon
    )
    
    # Load the cover photo image
    cover_photo_image = Image.open("logo/bago.png")  # Update with the path to your cover photo image
   
    
    # Display the cover photo image
    st.image(cover_photo_image, use_column_width=True)
    
    # Display the title
    st.markdown("<h2 style='text-align: center; margin: 20px;'>Python Code Similarity Detection and Clustering Tool</h2>", unsafe_allow_html=True)
    
    st.write("---")
    st.markdown(
        """<div style='text-align: justify; text-indent: 30px;'>
        Welcome to Python Code Similarity Detection and Clustering Tool by ORION. This tool is developed using a hybrid method that combines AST-based and text-based approaches with 
        the K-Means algorithm to detect code similarity in Python.
        </div><br>""",
        unsafe_allow_html=True
    )

    st.markdown(
        """<div style='text-align: justify; text-indent: 30px;'>
        Detecting similarity between code submissions can be time-consuming and difficult. To address this problem, this tool offers an innovative method for detecting code similarity,
        focusing on both the structural representation and code text information of Python code provided by Abstract Syntax Trees (ASTs) and a text-based approach. By leveraging these
        attributes, the method seeks to achieve a comprehensive detection of similarity in Python codes, capturing both structural patterns and textual features. Additionally, the computational
        efficiency of the K-Means algorithm will be utilized in clustering Python codes that exhibit similarity in their code text and structure, streamlining the process of identifying
        similarities and differences with in a set of code submissions.
        </div>""",
        unsafe_allow_html=True
    )
    st.write("---")
    
    # Expander for Step-by-Step Guide
    with st.expander("Instructions"):
        st.markdown("""
        ### **App: Code Similarity Detection and Clustering**

        1. **Launch the Application**:  
        Open the application to begin detecting and clustering code similarity.

        2. **Upload Python Files**:  
        - Upload individual Python files or a ZIP archive containing multiple Python files.
        - Click the "Upload" button to process the files.

        3. **Analyze Similarity**:  
        - The app will analyze the **Text Similarity** and **Structural Similarity** between the files.
        - Once processed, you will see various visualizations:
            - **Elbow Chart**: Helps determine the optimal number of clusters.
            - **Silhouette Plot**: Shows the silhouette score for clustering.

        4. **View Clustering Results**:  
        - The clustered files will be displayed, sorted by **Weighted Similarity** (a combination of text and structural similarity).
        - You can view a **Scatter Plot** of the clustered files and select two files for side-by-side comparison.

        5. **Download the Results**:  
        - Once the clustering is complete, you can download a CSV file that includes:
            - `Code1`, `Code2`
            - `Text_Similarity_%`, `Structural_Similarity_%`, and `Weighted_Similarity_%`
            - `Cluster` (cluster assignment for each pair)
        - Click the **Download CSV** button to save the file to your device.


        ### **Analyze: Clustered Code Similarity Analysis**

        1. **Upload the CSV File**:  
        - Open the **Clustered Code Similarity Analysis** section of the app.
        - Upload the CSV file that was generated from the **Code Similarity Detection and Clustering** step.

        2. **View and Explore the Data**:  
        - The uploaded CSV data will be displayed.
        - Use the **filters in the sidebar** to explore the data:
            - **Cluster(s)**: Filter by specific clusters.
            - **Text, Structural, and Weighted Similarity** ranges: Adjust these sliders to filter pairs based on similarity percentages.

        3. **Review Summary Statistics**:  
        - View summary statistics of the filtered dataset, including **average similarity scores** for each code pair.
        - Analyze the data with enhanced **visualizations**:
            - **Scatter Plot**: Visualizes Text Similarity vs. Structural Similarity.
            - **Histograms**: Show the distribution of similarity metrics (Text, Structural, and Weighted).

        4. **Download the Filtered Data**:  
        - Once you’ve applied filters and explored the data, you can download the filtered dataset.
        - Click **Download Filtered Data as CSV** from the sidebar.
        """)

    # Expander for Developers
    with st.expander("Developers"):
        st.write("This section is currently empty.")

    st.write("---")    
    # Display the images as a footer
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        st.image("logo/cspc.png", use_column_width=True)
    with col2:
        st.image("logo/ccs.png", use_column_width=True)
    with col3:
        st.image("logo/l2.png", use_column_width=True)
    
    # Add some spacing and align images properly using CSS
    st.markdown("""
    <style>
    .stImage {
        display: flex;
        justify-content: center;
        margin-bottom: 0 !important;
    }
    .stColumn > div {
        padding: 0px 5px;
    }
    </style>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    run()
