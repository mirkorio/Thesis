#app.py
import streamlit as st
import pandas as pd
import altair as alt
from backend.code_similarity_detection import extract_files, compare_files, sanitize_title
from backend.code_clustering import CodeClusterer, find_elbow_point
import os
import multiprocessing

def main():
    st.set_page_config(
        page_title="App",
        page_icon="logo/logo.png",  # Set your logo image as the page icon
    )
    st.markdown("<h3 style='text-align: center;'>Code Similarity Detection and Clustering</h3>", unsafe_allow_html=True)

    st.markdown("""
    This application allows you to detect and analyze code similarity by uploading Python files. 
    Get started by uploading your files and exploring clustered similarity results, visualizations, and detailed comparisons.
    """)

    # Text input for activity title
    activity_title = st.text_input("Enter a title for the code activity")

    # Initialize session state variables
    if 'similarity_df' not in st.session_state:
        st.session_state.similarity_df = pd.DataFrame()

    if 'elbow_scores' not in st.session_state:
        st.session_state.elbow_scores = []

    if 'best_num_clusters' not in st.session_state:
        st.session_state.best_num_clusters = 2

    if 'clustered_data' not in st.session_state:
        st.session_state.clustered_data = pd.DataFrame()

    if 'silhouette_avg' not in st.session_state:
        st.session_state.silhouette_avg = None

    if 'silhouette_data' not in st.session_state:
        st.session_state.silhouette_data = pd.DataFrame()

    if 'extracted_files_content' not in st.session_state:
        st.session_state.extracted_files_content = {}

    if 'selected_pair' not in st.session_state:
        st.session_state.selected_pair = None

    if 'clustering_performed' not in st.session_state:
        st.session_state.clustering_performed = False

    # File Uploader
    uploaded_files = st.file_uploader("Upload Python files (at least 5)", type=['py'], accept_multiple_files=True)

    if uploaded_files:
        # Check for duplicate file names
        file_names = [uploaded_file.name for uploaded_file in uploaded_files]
        if len(file_names) != len(set(file_names)):
            st.error("Duplicate file names are not allowed.")
        elif len(uploaded_files) == 1:
            st.error("Please upload more files to proceed.")
        else:
            st.write(f"Number of uploaded files: {len(uploaded_files)}")
            if st.button("Process Files"):
                with st.spinner("Processing files..."):
                    extracted_files, extracted_files_content = extract_files(uploaded_files)
                    st.session_state.extracted_files_content = extracted_files_content
                    file_pairs = [(extracted_files[i], extracted_files[j]) for i in range(len(extracted_files)) for j in range(i + 1, len(extracted_files))]

                    pool = multiprocessing.Pool()
                    results = pool.starmap(compare_files, [(pair, st.session_state.extracted_files_content) for pair in file_pairs])

                    results = [result for result in results if all(result)]
                    pool.close()
                    pool.join()

                    try:
                        # Convert similarity values to percentages and display with 2 decimal places
                        similarity_df = pd.DataFrame(results, columns=['Code1', 'Code2', 'Text_Similarity_%', 'Structural_Similarity_%', 'Weighted_Similarity_%'])
                        similarity_df[['Text_Similarity_%', 'Structural_Similarity_%', 'Weighted_Similarity_%']] = similarity_df[['Text_Similarity_%', 'Structural_Similarity_%', 'Weighted_Similarity_%']].apply(lambda x: round(x * 100, 2))
                        st.session_state.similarity_df = similarity_df

                        st.success("Processing complete!")
                    except Exception as e:
                        st.error(f"An error occurred: {str(e)}")
    else:
        st.info('Please upload Python files.')


   
    # Show similarity results
    if 'similarity_df' in st.session_state and not st.session_state.similarity_df.empty:
        st.header("Similarity Results")
        # Similarity Results Expander
        with st.expander("📝"):
            st.write("""
            The similarity results are calculated using a combination of text and structural similarity.
            Text similarity is measured using Simhash and Hamming distance, while structural similarity
            is assessed by comparing the Abstract Syntax Trees (AST) of the code files. The weighted similarity
            is then calculated to give the final or weighted similarity score.
            """)

        # Column renaming mapping
        column_mapping = {
            'Code1': 'Code 1',
            'Code2': 'Code 2',
            'Text_Similarity_%': 'Text Similarity %',
            'Structural_Similarity_%': 'Structural Similarity %',
            'Weighted_Similarity_%': 'Weighted Similarity %'
        }

        # Rename columns if they exist in the DataFrame
        df_display = st.session_state.similarity_df.rename(columns={col: column_mapping[col] for col in st.session_state.similarity_df.columns if col in column_mapping})

        # Convert similarity percentages to strings with 2 decimal places and %
        df_display[['Text Similarity %', 'Structural Similarity %', 'Weighted Similarity %']] = df_display[['Text Similarity %', 'Structural Similarity %', 'Weighted Similarity %']].applymap(lambda x: f"{x:.2f}%")

        # Display the dataframe
        st.dataframe(df_display)

        # Clustering
        if st.button("Perform Clustering"):
            with st.spinner("Performing clustering..."):
                clusterer = CodeClusterer(num_clusters=st.session_state.best_num_clusters)
                clusterer.load_data(st.session_state.similarity_df)
                
                try:
                    # Ensure that number of clusters doesn't exceed the number of samples
                    max_clusters_possible = len(st.session_state.similarity_df)
                    if max_clusters_possible < 2:
                        st.warning("Clustering cannot be performed because there are not enough distinct samples.")
                    else:
                        # Limit max_clusters based on number of samples
                        max_clusters = min(10, max_clusters_possible)
                        
                        # Calculate the elbow method with limited clusters
                        clusterer.calculate_elbow(max_clusters=max_clusters)
                        st.session_state.elbow_scores = clusterer.elbow_scores
                        st.session_state.best_num_clusters = find_elbow_point(clusterer.elbow_scores)

                        # Recheck if the best number of clusters is within the valid range
                        if st.session_state.best_num_clusters > max_clusters_possible:
                            st.warning(f"Clustering cannot be performed. The number of clusters {st.session_state.best_num_clusters} exceeds the number of samples.")
                        else:
                            # Proceed with clustering if everything is valid
                            clusterer = CodeClusterer(num_clusters=st.session_state.best_num_clusters)
                            clusterer.load_data(st.session_state.similarity_df)

                            features = clusterer.cluster_codes()
                            st.session_state.clustered_data = clusterer.get_clustered_data()
                            st.session_state.silhouette_avg = clusterer.silhouette_avg
                            st.session_state.silhouette_data = clusterer.get_silhouette_data(features)
                            st.session_state.clustering_performed = True

                            st.success("Clustering complete!")
                except ValueError as e:
                    if "Number of labels is 1" in str(e):
                        st.warning("This implies that all uploaded files are identical, resulting in only one cluster. Clustering requires at least two distinct groups to work.")
                    else:
                        st.error(f"Error clustering data: {str(e)}")


        # Display Elbow Chart and Best Number of Clusters
        if st.session_state.clustering_performed and 'elbow_scores' in st.session_state and st.session_state.elbow_scores:
            st.header("Elbow Method")
            # Elbow Method Expander
            with st.expander("📝 "):
                st.write("""
                The Elbow Method helps in determining the optimal number of clusters for clustering algorithms.
                It does this by plotting the sum of squared distances from each point to its assigned cluster center
                (inertia). The 'elbow' is the point where adding more clusters doesn't significantly reduce the inertia,
                indicating the best number of clusters.
                """)
            elbow_chart = alt.Chart(pd.DataFrame({
                'Clusters': list(range(2, len(st.session_state.elbow_scores) + 2)),
                'Inertia': st.session_state.elbow_scores
            })).mark_line().encode(
                x='Clusters:O',
                y='Inertia:Q'
            ).interactive()
            st.altair_chart(elbow_chart, use_container_width=True)
            st.write(f"Best Number of Clusters: {st.session_state.best_num_clusters}")

        # Display Clustering Visualization (Scatter Plot)
        if st.session_state.clustering_performed and 'clustered_data' in st.session_state and not st.session_state.clustered_data.empty:
            st.header("Scatter Plot")
            # Scatter Plot Expander
            with st.expander("📝"):
                st.write("""
                The scatter plot visualizes the clustered data points in a two-dimensional space. Each point represents
                a code file, and its position depends on the similarity metrics. The plot helps in understanding the distribution
                of files across different clusters.
                """)

            # Column renaming mapping for the scatter plot
            scatter_column_mapping = {
                'Text_Similarity_%': 'Text Similarity %',
                'Structural_Similarity_%': 'Structural Similarity %',
                'Weighted_Similarity_%': 'Weighted Similarity %'
            }

            # Rename columns in clustered_data for display
            clustered_data_display = st.session_state.clustered_data.rename(columns={col: scatter_column_mapping[col] for col in st.session_state.clustered_data.columns if col in scatter_column_mapping})

            # Create the scatter plot with the renamed columns
            cluster_chart = alt.Chart(clustered_data_display).mark_circle(size=60).encode(
                x='Text Similarity %',
                y='Structural Similarity %',
                color='Cluster:N',
                tooltip=['Code1', 'Code2', 'Text Similarity %', 'Structural Similarity %', 'Weighted Similarity %']
            ).interactive()

            st.altair_chart(cluster_chart, use_container_width=True)


            # Display Silhouette Plot and Scores
            if 'silhouette_data' in st.session_state and not st.session_state.silhouette_data.empty:
                st.header("Silhouette Plot")
                # Silhouette Plot and Score Expander
                with st.expander("📝 "):
                    st.write("""
                    The Silhouette plot and score are used to measure how well each data point lies within its cluster.
                    A high silhouette score indicates that the data point is well-clustered. The plot provides a visualization
                    of how close data points are to the clusters they are assigned to, helping assess clustering performance.
                    """)
                silhouette_chart = alt.Chart(st.session_state.silhouette_data).mark_bar().encode(
                    x='Silhouette Value',
                    y='Cluster:N',
                    color='Cluster:N',
                    tooltip=['Silhouette Value', 'Cluster']
                ).interactive()
                st.altair_chart(silhouette_chart, use_container_width=True)
                st.write(f"Silhouette Score: {st.session_state.silhouette_avg:.4f}")

            # Display Clustered codes from highest to lowest weighted similarity
            st.header("Clustered Codes")
            # Clustered Codes Expander
            with st.expander("📝"):
                st.write("""
                Once the clustering process is complete, each code file is assigned to a cluster based on its similarity
                with other files. The clusters represent groups of code files that share similar characteristics, both textually
                and structurally. This grouping can help identify patterns and relationships between the code files.
                """)

            # Column renaming mapping for the clustered data display
            cluster_column_mapping = {
                'Code1': 'Code 1',
                'Code2': 'Code 2',
                'Text_Similarity_%': 'Text Similarity %',
                'Structural_Similarity_%': 'Structural Similarity %',
                'Weighted_Similarity_%': 'Weighted Similarity %'
            }

            # Sort clustered data by Weighted Similarity in descending order
            clustered_data_sorted = st.session_state.clustered_data.sort_values(by='Weighted_Similarity_%', ascending=False)

            # Apply percentage formatting with 2 decimal places
            clustered_data_sorted[['Text_Similarity_%', 'Structural_Similarity_%', 'Weighted_Similarity_%']] = clustered_data_sorted[['Text_Similarity_%', 'Structural_Similarity_%', 'Weighted_Similarity_%']].applymap(lambda x: f"{x:.2f}%")

            # Rename columns for display
            clustered_data_display = clustered_data_sorted.rename(columns={col: cluster_column_mapping[col] for col in clustered_data_sorted.columns if col in cluster_column_mapping})

            # Display the sorted and renamed DataFrame
            st.dataframe(clustered_data_display)


            # Side-by-Side Code Comparison
            st.header("Side-by-Side Code Comparison")

            # Expander for plagiarism forms and detection guidelines
            with st.expander("Plagiarism Forms and Detection Guidelines"):
                st.write("""
                In the context of computer programming, common forms of code plagiarism include:

                1. **Complete copy-pasting** of code - 100% Weighted Similarity.
                2. **Altering comments** within the code.
                3. **Changing identifiers** like variable names - Low Text Similarity but High Structural Similarity.
                4. **Rearranging the code sequence** without changing functionality - Low Structural Similarity but Hight Text Similarity.
                
                However, if an individual replicates another’s code but performs extensive modifications and restructuring while maintaining the function’s integrity, this action should not be classified as plagiarism.
                """)

            code_pairs = st.session_state.similarity_df[['Code1', 'Code2']].apply(tuple, axis=1).tolist()
            selected_pair = st.selectbox("Select a pair of files to compare", options=code_pairs)
            st.session_state.selected_pair = selected_pair

            if selected_pair:
                code1, code2 = selected_pair
                code1_path = [key for key in st.session_state.extracted_files_content.keys() if os.path.basename(key) == code1]
                code2_path = [key for key in st.session_state.extracted_files_content.keys() if os.path.basename(key) == code2]

                if code1_path and code2_path:
                    code1_content = st.session_state.extracted_files_content.get(code1_path[0], "Content not found.")
                    code2_content = st.session_state.extracted_files_content.get(code2_path[0], "Content not found.")

                    # Retrieve similarity metrics
                    similarity_data = st.session_state.similarity_df[
                        (st.session_state.similarity_df['Code1'] == code1) & 
                        (st.session_state.similarity_df['Code2'] == code2)
                    ]
                    text_similarity = similarity_data['Text_Similarity_%'].values[0]
                    structural_similarity = similarity_data['Structural_Similarity_%'].values[0]
                    weighted_similarity = similarity_data['Weighted_Similarity_%'].values[0]

                    # Create columns for side-by-side display
                    col1, col2 = st.columns(2)

                    with col1:
                        st.markdown("### Code 1 Details")
                        st.write(f"**File Name:** {code1}")
                        st.write(f"**Text Similarity:** {text_similarity:.2f}%")
                        st.write(f"**Structural Similarity:** {structural_similarity:.2f}%")
                        st.write(f"**Weighted Similarity:** {weighted_similarity:.2f}%")
                        st.code(code1_content, language='python')

                    with col2:
                        st.markdown("### Code 2 Details")
                        st.write(f"**File Name:** {code2}")
                        st.write(f"**Text Similarity:** {text_similarity:.2f}%")
                        st.write(f"**Structural Similarity:** {structural_similarity:.2f}%")
                        st.write(f"**Weighted Similarity:** {weighted_similarity:.2f}%")
                        st.code(code2_content, language='python')
                        
            # Display the download button in the sidebar only if clustering is done
            with st.sidebar:
                if st.session_state.clustering_performed and not st.session_state.clustered_data.empty:
                    #st.write("Download Results")
                    df = st.session_state.clustered_data[['Code1', 'Code2', 'Text_Similarity_%', 'Structural_Similarity_%', 'Weighted_Similarity_%', 'Cluster']]
                    csv = df.to_csv(index=False)
                    st.download_button(
                        label="Download Clustered Codes",
                        data=csv,
                        file_name=f"{sanitize_title(activity_title)}_clustered_codes.csv",
                        mime="text/csv"
                    )
if __name__ == "__main__":
    main()

