## 🚀 Code Similarity Detection and Clustering Tool by Team Orion

Welcome to the **Python Code Similarity Detection and Clustering Tool** developed by **ORION**. This tool utilizes a hybrid approach that combines AST-based and text-based methodologies with the K-Means algorithm to effectively detect code similarity in Python.

## 🌐 Live App
You can access the live application [**here**](https://thesis-roqzofhqframgkykcznpcp.streamlit.app/).

## 📖 Step-by-Step Guide

## App: Code Similarity Detection and Clustering 

---

1. **📝 Enter a Title for the Code Activity**:
- Start by entering a title for the current code activity. This will be used as the filename for downloading the results later.

2. **📁 Upload Python Files**:
- Upload Python files by clicking the **"Browse files"** button or **"Drag and Drop files"** in the Upload Python Files section.

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

## Analyze : Clustered Code Similarity Analysis

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

---

