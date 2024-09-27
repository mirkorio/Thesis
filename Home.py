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
    gif_url = "https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExazM2cnB2NGYyaHNnc2ZyaThtNXFnYXg5NHJ4dHpodHFpeXk0Y2ZweCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9cw/Eq1sxBSFpIBdUyBAsP/giphy.gif"  # Replace with your GIF URL

    # Display the animated GIF with a specified width
    st.image(gif_url, width=600)  # Adjust the width as needed


    
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
    
    # Expander for Instructions
    with st.expander("Instructions"):
        st.markdown("""
        ### App: Code Similarity Detection and Clustering 

        ---
        
        1. **📝 Enter a Title for the Code Activity**:
        - Start by entering a title for the current code activity. This will be used as the filename for downloading the results later.

        2. **📁 Upload Python Files**:
        - Upload individual Python files or a ZIP archive containing multiple Python files.
        - Click the **"Upload"** button to process the files.

        3. **🔄 Process Files**:
        - The app will automatically process the uploaded files, performing similarity analysis and clustering preparation.

        4. **📊 View Similarity Results**:
        - After the files are processed, you will see the similarity metrics:
            - **Text Similarity**
            - **Structural Similarity**
            - **Weighted Similarity** (a combination of the text and structural similarity)

        5. **🔍 Perform Clustering**:
        - The next step is to cluster the files based on the calculated similarities.
        - The app will automatically apply clustering using the **K-Means** algorithm.

        6. **📊 View Results**:
        - Once clustering is complete, various visualizations and metrics will be displayed:
            - **Elbow Method**: Helps you determine the optimal number of clusters.
            - **Best Number of Clusters**: Displays the best number of clusters found.
            - **Scatter Plot**: Visualizes the clustered codes.
            - **Silhouette Plot**: Shows the silhouette scores for clustering.
            - **Silhouette Score**: Quantifies how well the clusters are formed.
            - **Clustered Codes**: Lists the codes grouped by their clusters.
            - **Side-by-Side Code Comparison**: Compare two selected codes within the same cluster.

        7. **💾 Download Clustered Codes**:
        - After reviewing the results, click the **Download CSV** button to save the clustered codes, including:
            - **Code1**, **Code2**
            - **Text Similarity %**, **Structural Similarity %**, and **Weighted Similarity %**
            - **Cluster** (cluster assignment for each pair)

        ---

        ### Analyze: Clustered Code Similarity Analysis

        1. **📤 Upload CSV File**:
        - Navigate to the **"Analyze"** section of the app.
        - Use the file uploader to upload the CSV file generated from the Code Similarity Detection and Clustering step.

        2. **📜 View Uploaded Data**:
        - Once the CSV file is uploaded, you can view the complete DataFrame within an expander for a clean layout.

        3. **📈 Summary Statistics**:
        - Expand the summary statistics section to view descriptive statistics of the dataset.

        4. **🔍 Filter Data**:
        - Use the filter options in the sidebar to refine the data based on cluster selection and similarity score ranges.

        5. **🔑 View Filtered Data**:
        - After applying filters, the filtered data will be displayed along with an explanation of color coding for similarity scores.

        6. **📉 Visualize Similarity Metrics**:
        - Explore various visualizations, including scatter plots and histograms for a better understanding of the similarities.

        7. **💾 Download Filtered Data**:
        - If needed, you can download the filtered data as a CSV file through the download button in the sidebar.
        """)




    # Expander for Developers
    with st.expander("Developers"):
        st.markdown(
        """<div style='text-align: center;'><h3>
       Team Orion
        </h3></div>""",
        unsafe_allow_html=True
    )

        st.write("---") 
        col1, col2, col3 = st.columns([1, 1, 1])
       
    st.markdown("""
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
    """, unsafe_allow_html=True)


    with col1:
        st.image("developers/venn.png", use_column_width=True)
        st.markdown("<p style='text-align: center;'>Venn P. Delos Santos</p>", unsafe_allow_html=True)
        st.markdown("""
            <div style='text-align: center;'>
                <a href='https://github.com/7ELEVEENN' target='_blank'>
                    <i class="fa fa-github" style="font-size:30px; margin-right: 10px;"></i>
                </a>
                <a href='https://www.facebook.com/0nepiece12' target='_blank'>
                    <i class="fa fa-facebook" style="font-size:30px; margin-right: 10px;"></i>
                </a>
                <a href='mailto:vedelossantos@my.cspc.edu.ph'>
                    <i class="fa fa-envelope" style="font-size:30px;"></i>
                </a>
            </div>
        """, unsafe_allow_html=True)

    # For col2
    with col2:
        st.image("developers/chano.png", use_column_width=True)
        st.markdown("<p style='text-align: center;'>John Christian M. Gava</p>", unsafe_allow_html=True)
        st.markdown("""
            <div style='text-align: center;'>
                <a href='https://github.com/itsbabychano' target='_blank'>
                    <i class="fa fa-github" style="font-size:30px; margin-right: 10px;"></i>
                </a>
                <a href='https://facebook.com/itsbabychano' target='_blank'>
                    <i class="fa fa-facebook" style="font-size:30px; margin-right: 10px;"></i>
                </a>
                <a href=' mailto:jogava@my.cspc.edu.ph'>
                    <i class="fa fa-envelope" style="font-size:30px;"></i>
                </a>
            </div>
        """, unsafe_allow_html=True)

    # For col3
    with col3:
        st.image("developers/marc.png", use_column_width=True)
        st.markdown("<p style='text-align: center;'>Marc Christian D. Tumaneng</p>", unsafe_allow_html=True)
        st.markdown("""
            <div style='text-align: center;'>
                <a href='https://github.com/mirkorio' target='_blank'>
                    <i class="fa fa-github" style="font-size:30px; margin-right: 10px;"></i>
                </a>
                <a href='https://www.facebook.com/marcchristian.tumaneng.14' target='_blank'>
                    <i class="fa fa-facebook" style="font-size:30px; margin-right: 10px;"></i>
                </a>
                <a href='mailto:matumaneng@my.cspc.edu.ph'>
                    <i class="fa fa-envelope" style="font-size:30px;"></i>
                </a>
            </div>
        """, unsafe_allow_html=True)




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
