# Code Similarity Detection and Clustering Tool by Team Orion

Welcome to Python Code Similarity Detection and Clustering Tool by ORION. This tool is developed using a hybrid method that combines AST-based and text-based approaches with the K-Means algorithm to detect code similarity in Python.

## Live App
You can access the live application [here](https://thesis-roqzofhqframgkykcznpcp.streamlit.app/).

## Step-by-Step Guide

### Part 1: Code Similarity Detection and Clustering

1. **Upload Python Files**:
   - On the homepage, use the file uploader to upload your Python files or a ZIP archive containing Python files.

2. **Process Uploaded Files**:
   - After uploading, the application will automatically process the files to calculate similarity metrics.

3. **View Similarity Data**:
   - Once processing is complete, you will see a summary of the similarity metrics, including text similarity, structural similarity, and weighted similarity.

4. **Download CSV File**:
   - After viewing the similarity data, click the download button to export the results as a CSV file.

### Analyze: Clustered Code Similarity Analysis

1. **Upload CSV File**:
   - Navigate to the "Analyze" section of the app.
   - Use the file uploader to upload the CSV file generated from the Code Similarity Detection and Clustering step.

2. **View Uploaded Data**:
   - Once the CSV file is uploaded, you can view the complete DataFrame within an expander for a clean layout.

3. **Summary Statistics**:
   - Expand the summary statistics section to view descriptive statistics of the dataset.

4. **Filter Data**:
   - Use the filter options in the sidebar to refine the data based on cluster selection and similarity score ranges.

5. **View Filtered Data**:
   - After applying filters, the filtered data will be displayed along with an explanation of color coding for similarity scores.

6. **Visualize Similarity Metrics**:
   - Explore various visualizations, including scatter plots and histograms for better understanding of the similarities.

7. **Download Filtered Data**:
   - If needed, you can download the filtered data as a CSV file through the download button in the sidebar.

