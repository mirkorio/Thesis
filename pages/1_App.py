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
    st.markdown("<h3 style='text-align: center; margin: 20px;'>Code Similarity Detection and Clustering</h3>", unsafe_allow_html=True)

    # Adding an introductory section with markdown
    st.markdown("""
    This application enables you to detect and analyze code similarity by uploading Python files. 
    Get started by uploading your files to explore clustered similarity results, visualizations, and detailed comparisons.
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

    if 'davies_bouldin' not in st.session_state:
        st.session_state.davies_bouldin = None

    if 'extracted_files_content' not in st.session_state:
        st.session_state.extracted_files_content = {}

    if 'selected_pair' not in st.session_state:
        st.session_state.selected_pair = None

    if 'clustering_performed' not in st.session_state:
        st.session_state.clustering_performed = False

    # File Uploader
    uploaded_files = st.file_uploader("Upload Python files", type=['py'], accept_multiple_files=True)

    if uploaded_files:
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
                    # Adjust the similarity values to be percentages and rename columns
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
        
        # **Display dataframe with two decimal places and % sign**
        df_display = st.session_state.similarity_df.copy()
        df_display[['Text_Similarity_%', 'Structural_Similarity_%', 'Weighted_Similarity_%']] = df_display[['Text_Similarity_%', 'Structural_Similarity_%', 'Weighted_Similarity_%']].applymap(lambda x: f"{x:.2f}%")
        st.dataframe(df_display)

        # Clustering
        if st.button("Perform Clustering"):
            with st.spinner("Performing clustering..."):
                # Calculate the elbow method automatically
                clusterer = CodeClusterer(num_clusters=st.session_state.best_num_clusters)
                clusterer.load_data(st.session_state.similarity_df)
                clusterer.calculate_elbow(max_clusters=10)
                st.session_state.elbow_scores = clusterer.elbow_scores
                st.session_state.best_num_clusters = find_elbow_point(clusterer.elbow_scores)

                clusterer = CodeClusterer(num_clusters=st.session_state.best_num_clusters)
                clusterer.load_data(st.session_state.similarity_df)

                try:
                    features = clusterer.cluster_codes()
                    st.session_state.clustered_data = clusterer.get_clustered_data()
                    st.session_state.silhouette_avg = clusterer.silhouette_avg
                    st.session_state.davies_bouldin = clusterer.davies_bouldin
                    st.session_state.clustering_performed = True

                    st.success("Clustering complete!")
                except ValueError as e:
                    st.error(f"Error clustering data: {str(e)}")

        # Display Elbow Chart and Best Number of Clusters
        if st.session_state.clustering_performed and 'elbow_scores' in st.session_state and st.session_state.elbow_scores:
            st.header("Elbow Method")
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
            cluster_chart = alt.Chart(st.session_state.clustered_data).mark_circle(size=60).encode(
                x='Text_Similarity_%',
                y='Structural_Similarity_%',
                color='Cluster:N',
                tooltip=['Code1', 'Code2', 'Text_Similarity_%', 'Structural_Similarity_%', 'Weighted_Similarity_%']
            ).interactive()
            st.altair_chart(cluster_chart, use_container_width=True)

            # Display Silhouette Plot and Scores
            if 'clustered_data' in st.session_state and 'features' in locals():
                st.header("Silhouette Plot")
                silhouette_data = clusterer.get_silhouette_data(features)
                silhouette_chart = alt.Chart(silhouette_data).mark_bar().encode(
                    x='Silhouette Value',
                    y='Cluster:N',
                    color='Cluster:N',
                    tooltip=['Silhouette Value', 'Cluster']
                ).interactive()
                st.altair_chart(silhouette_chart, use_container_width=True)
                st.write(f"Silhouette Score: {st.session_state.silhouette_avg:.4f}")
                st.write(f"Davies-Bouldin Index: {st.session_state.davies_bouldin:.4f}")

            # Display Clustered codes from highest to lowest weighted similarity
            st.header("Clustered Codes")
            clustered_data_sorted = st.session_state.clustered_data.sort_values(by='Weighted_Similarity_%', ascending=False)
            clustered_data_sorted[['Text_Similarity_%', 'Structural_Similarity_%', 'Weighted_Similarity_%']] = clustered_data_sorted[['Text_Similarity_%', 'Structural_Similarity_%', 'Weighted_Similarity_%']].applymap(lambda x: f"{x:.2f}%")
            st.dataframe(clustered_data_sorted)

            # Side-by-Side Code Comparison
            st.header("Side-by-Side Code Comparison")

            # Expander for plagiarism forms and detection guidelines
            with st.expander("Plagiarism Forms and Detection Guidelines"):
                st.write("""
                In the context of computer programming, common forms of code plagiarism include:

                1. **Complete copy-pasting** of code.
                2. **Altering comments** within the code.
                3. **Changing identifiers** like variable names.
                4. **Rearranging the code sequence** without changing functionality.
                
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

