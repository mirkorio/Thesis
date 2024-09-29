import streamlit as st
import pandas as pd
import altair as alt

# Initialize session state for storing the uploaded data
if 'df' not in st.session_state:
    st.session_state.df = None

st.set_page_config(
    page_title="Analyze",
    page_icon="logo/logo.png",  # Set your logo image as the page icon
)

# Title of the Streamlit app
st.markdown("<h3 style='text-align: center; margin: 20px;'>Clustered Code Similarity Analysis</h3>", unsafe_allow_html=True)

# Adding an introductory section with markdown
st.markdown("""
This application allows you to analyze clustered code similarity using a CSV file. 
Upload your data to get started and explore various interactive visualizations and filters.
""")

# Function to apply color based on similarity score
def apply_color(val):
    """
    Color code cells based on the Weighted Similarity percentage.
    """
    if val >= 75:
        color = 'background-color: #A04747'#red
    elif 50 <= val < 75:
        color = 'background-color: #D8A25E'#orange
    elif 25 <= val < 50:
        color = 'background-color: #EEDF7A'#yellow
    elif 1 <= val < 25:
        color = 'background-color: #557C56'#green
    else:
        color = 'background-color: #6A9AB0'#blue
    return color

# Uploading the CSV file
uploaded_file = st.file_uploader("Upload a CSV file", type="csv")

if uploaded_file is not None:
    try:
        # Try to read the CSV file into a pandas DataFrame
        df = pd.read_csv(uploaded_file)

        # Normalize column names for consistency
        df.columns = df.columns.str.strip().str.lower()

        # Define required columns in lowercase for checking
        required_columns = ['code1', 'code2', 'text_similarity_%', 'structural_similarity_%', 'weighted_similarity_%', 'cluster']

        # Check if all required columns are present in the dataframe
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            # Raise an error if any required columns are missing
            st.error(f"The uploaded file is missing the following required columns: {', '.join(missing_columns)}, try again.")
        else:
            # If no columns are missing, store the dataframe in session state
            st.session_state.df = df
            # Display a success message
            st.success("CSV file data uploaded successfully!")

    except pd.errors.EmptyDataError:
        st.error("The uploaded file is empty. Please upload a valid CSV file.")
    except pd.errors.ParserError:
        st.error("There was an error parsing the CSV file. Please ensure the file is properly formatted.")
    except Exception as e:
        # Handle general exceptions
        st.error(f"An unexpected error occurred: {e}")

if st.session_state.df is not None:
    df = st.session_state.df

    # Display the dataframe with an expander to save space
    with st.expander("View Uploaded Data"):
        st.write("Full DataFrame")
        # Normalize column names for consistency
        df.columns = df.columns.str.strip().str.lower()

        # Format columns to two decimal places and apply color formatting to Weighted_Similarity_%
        df[['text_similarity_%', 'structural_similarity_%', 'weighted_similarity_%']] = df[['text_similarity_%', 'structural_similarity_%', 'weighted_similarity_%']].round(2)

        styled_df = df.style.format({
            'text_similarity_%': '{:.2f}%',
            'structural_similarity_%': '{:.2f}%',
            'weighted_similarity_%': '{:.2f}%'
        }).applymap(apply_color, subset=['weighted_similarity_%'])
        
        st.dataframe(styled_df)

    # Define required columns in lowercase
    required_columns = ['code1', 'code2', 'text_similarity_%', 'structural_similarity_%', 'weighted_similarity_%', 'cluster']

    # Check if all required columns are present in the dataframe
    if all(column in df.columns for column in required_columns):
        # Rename columns back to original names for consistency in visualizations
        df.columns = ['Code1', 'Code2', 'Text_Similarity_%', 'Structural_Similarity_%', 'Weighted_Similarity_%', 'Cluster']
        
        # Summary statistics with an expander
        with st.expander("Summary Statistics"):
            st.write(df.describe())

        # Filter options in the sidebar
        st.sidebar.header('Filter Options')
        selected_cluster = st.sidebar.multiselect('Select cluster(s) to visualize', options=df['Cluster'].unique(), default=df['Cluster'].unique())
        text_similarity_range = st.sidebar.slider('Text Similarity Range (%)', 0.0, 100.0, (0.0, 100.0))
        structural_similarity_range = st.sidebar.slider('Structural Similarity Range (%)', 0.0, 100.0, (0.0, 100.0))
        weighted_similarity_range = st.sidebar.slider('Weighted Similarity Range (%)', 0.0, 100.0, (0.0, 100.0))

        # Filter the dataframe based on user selection
        filtered_df = df[
            (df['Cluster'].isin(selected_cluster)) &
            (df['Text_Similarity_%'].between(*text_similarity_range)) &
            (df['Structural_Similarity_%'].between(*structural_similarity_range)) &
            (df['Weighted_Similarity_%'].between(*weighted_similarity_range))
        ]

        # Display filtered dataframe with formatted similarity columns
        # Subheader for the filtered data section
        st.subheader("Filtered Data")

        # Expander for Color Labels Explanation with styled text
        with st.expander("Filtering Guide"):
            st.markdown("""
            **Use the filters in the sidebar to refine the displayed data**:
            - **Text Similarity Range**: Adjust the slider to specify the range of text similarity percentages you want to include.
            - **Structural Similarity Range**: Adjust the slider to specify the range of the structural similarity percentages.
            - **Weighted Similarity Range**: This filter allows you to focus on specific weighted similarity scores.

            **Color Guide for Weighted Similarity**:
        
            <p><strong><span style='color: #6A9AB0;'>Blue</span></strong>: 0% similarity score or not similar.</p>
            
            <p><strong><span style='color: #557C56;'>Green</span></strong>: 1% - 24% very low similarity score.</p>
            
            <p><strong><span style='color: #EEDF7A;'>Yellow</span></strong>: 25% - 49% low similarity score.</p>
            
            <p><strong><span style='color: #D8A25E;'>Orange</span></strong>: 50% - 74% mid similarity score.</p>
            
            <p><strong><span style='color: #A04747;'>Red</span></strong>: 75% - 100% high similarity score.</p>
            """, unsafe_allow_html=True)

        # Rename the columns for better appearance in the table
        filtered_df = filtered_df.rename(columns={
            'Code1': 'Code 1',
            'Code2': 'Code 2',
            'Text_Similarity_%': 'Text Similarity %',
            'Structural_Similarity_%': 'Structural Similarity %',
            'Weighted_Similarity_%': 'Weighted Similarity %'
        })

        # Rounding the values for better display
        filtered_df[['Text Similarity %', 'Structural Similarity %', 'Weighted Similarity %']] = filtered_df[
            ['Text Similarity %', 'Structural Similarity %', 'Weighted Similarity %']
        ].round(2)

        # Styling and formatting the filtered DataFrame
        styled_filtered_df = filtered_df.style.format({
            'Text Similarity %': '{:.2f}%',
            'Structural Similarity %': '{:.2f}%',
            'Weighted Similarity %': '{:.2f}%'
        }).applymap(apply_color, subset=['Weighted Similarity %'])

        # Displaying the styled DataFrame in Streamlit
        st.dataframe(styled_filtered_df)


         # Summary for "Filtered Data"
        with st.expander("Summary of Filtered Data"):
            # Rename the columns for consistency and better display
            filtered_df = filtered_df.rename(columns={
                'Text_Similarity_%': 'Text Similarity %',
                'Structural_Similarity_%': 'Structural Similarity %',
                'Weighted_Similarity_%': 'Weighted Similarity %'
            })

            # Round the similarity columns to two decimal places
            filtered_df[['Text Similarity %', 'Structural Similarity %', 'Weighted Similarity %']] = filtered_df[
                ['Text Similarity %', 'Structural Similarity %', 'Weighted Similarity %']
            ].round(2)

            # Function to count how many entries fall into each similarity range
            def count_by_similarity_range(df):
                return {
                    'Blue (0%)': df[df['Weighted Similarity %'] == 0].shape[0],
                    'Green (1% - 24%)': df[df['Weighted Similarity %'].between(1, 24)].shape[0],
                    'Yellow (25% - 49%)': df[df['Weighted Similarity %'].between(25, 49)].shape[0],
                    'Orange (50% - 74%)': df[df['Weighted Similarity %'].between(50, 74)].shape[0],
                    'Red (75% - 100%)': df[df['Weighted Similarity %'] >= 75].shape[0]
                }

            # Generate a summary of the filtered data based on similarity ranges
            filtered_data_summary = count_by_similarity_range(filtered_df)

            # Convert the summary dictionary to a DataFrame
            summary_df = pd.DataFrame(list(filtered_data_summary.items()), columns=['Similarity Range', 'Count'])

            # Function to apply background colors to the summary rows based on the similarity range
            def apply_row_color(row):
                if 'Blue' in row['Similarity Range']:
                    return ['background-color: #6A9AB0'] * len(row)  # Blue
                elif 'Green' in row['Similarity Range']:
                    return ['background-color: #557C56'] * len(row)  # Green
                elif 'Yellow' in row['Similarity Range']:
                    return ['background-color: #EEDF7A'] * len(row)  # Yellow
                elif 'Orange' in row['Similarity Range']:
                    return ['background-color: #D8A25E'] * len(row)  # Orange
                elif 'Red' in row['Similarity Range']:
                    return ['background-color: #A04747'] * len(row)  # Red
                return [''] * len(row)

            # Apply row colors based on similarity ranges
            styled_summary_df = summary_df.style.apply(apply_row_color, axis=1)

            # Display the styled summary DataFrame
            st.dataframe(styled_summary_df)

        # Enhanced visualizations with custom themes and layering

        st.subheader('Text Similarity & Structural Similarity')

        # Add an expander explaining the purpose of the plot
        with st.expander("📝"):
            st.markdown("""
            This scatter plot visualizes the relationship between text similarity and structural similarity scores. 
            Each point represents a pair of code samples, allowing you to identify trends, clusters, 
            or outliers in the data. The color coding indicates the weighted similarity, providing insights into 
            how closely related the code samples are in terms of both their text and structure.
            """)

        # Rename columns for consistency and better readability in the plot
        filtered_df = filtered_df.rename(columns={
            'Text_Similarity_%': 'Text Similarity %',
            'Structural_Similarity_%': 'Structural Similarity %',
            'Weighted_Similarity_%': 'Weighted Similarity %'
        })

        # Define the custom color scale based on 'Weighted Similarity %' thresholds
        color_scale = alt.Scale(
            domain=[0, 1, 25, 50, 75, 100],
            range=['#6A9AB0', '#557C56', '#EEDF7A', '#D8A25E', '#A04747']
        )

        # Create a scatter plot with renamed columns
        scatter_plot = alt.Chart(filtered_df).mark_circle(size=60).encode(
            x=alt.X('Text Similarity %', title='Text Similarity (%)'),
            y=alt.Y('Structural Similarity %', title='Structural Similarity (%)'),
            color=alt.Color('Weighted Similarity %', scale=color_scale, legend=alt.Legend(title="Weighted Similarity (%)")),
            tooltip=['Code 1', 'Code 2', 'Text Similarity %', 'Structural Similarity %', 'Weighted Similarity %']
        ).interactive().properties(
            width=800,
            height=400
        )

        # Display the scatter plot
        st.altair_chart(scatter_plot, use_container_width=True)


        # Calculate and display overall similarity for each code
        st.subheader("""Each code's Average Similarity Scores""")

        # Expander explaining how the scores are calculated
        with st.expander("📝 "):
            st.markdown("""
            Average similarity scores are calculated for each code sample by aggregating the similarity metrics across all comparisons it is involved in. This analysis helps in understanding the general similarity of each code sample with others in the dataset. Additionally, a filter can be applied to focus on specific ranges of similarity scores. The metrics include:
            - **Text Similarity**: Measures how closely the text of the code samples match.
            - **Structural Similarity**: Assesses the similarity in the structural design of the code.
            - **Weighted Similarity**: A combined measure that takes both text and structural similarities into account, providing an overall similarity score.
            """)

        # Calculate overall/average similarity for each code
        overall_similarity = df.groupby('Code1').agg(
            average_text_similarity=('Text_Similarity_%', 'mean'),
            average_structural_similarity=('Structural_Similarity_%', 'mean'),
            average_weighted_similarity=('Weighted_Similarity_%', 'mean')
        ).reset_index()

        # Handle missing data by filling NaNs with 0
        overall_similarity.fillna(0, inplace=True)

        # Round results for display
        overall_similarity[['average_weighted_similarity', 'average_text_similarity', 'average_structural_similarity']] = overall_similarity[
            ['average_weighted_similarity', 'average_text_similarity', 'average_structural_similarity']].round(2)

        # Rename columns for better appearance
        overall_similarity = overall_similarity.rename(columns={
            'Code1': 'Code 1',
            'average_text_similarity': 'Average Text Similarity %',
            'average_structural_similarity': 'Average Structural Similarity %',
            'average_weighted_similarity': 'Average Weighted Similarity %'
        })

        # Sort by weighted similarity (highest to lowest)
        overall_similarity = overall_similarity.sort_values(by='Average Weighted Similarity %', ascending=False)

        # Sidebar filter for weighted similarity range
        weighted_similarity_range = st.sidebar.slider('Average Weighted Similarity Range (%)', 0.0, 100.0, (0.0, 100.0))

        # Filter based on user-selected range
        filtered_overall_similarity = overall_similarity[
            overall_similarity['Average Weighted Similarity %'].between(*weighted_similarity_range)
        ]

        # Apply color-coding and percentage formatting
        styled_filtered_overall_similarity = filtered_overall_similarity.style.applymap(
            apply_color, subset=['Average Weighted Similarity %']
        ).format({
            'Average Weighted Similarity %': '{:.2f}%',
            'Average Text Similarity %': '{:.2f}%',
            'Average Structural Similarity %': '{:.2f}%'
        })

        # Display the styled and filtered dataframe
        st.dataframe(styled_filtered_overall_similarity)


        # Summary for "Each code's Average Similarity Scores"
        with st.expander("Summary of Each Code's Average Similarity Scores"):

            # Calculate the average similarities
            overall_similarity = df.groupby('Code1').agg(
                average_text_similarity=('Text_Similarity_%', 'mean'),
                average_structural_similarity=('Structural_Similarity_%', 'mean'),
                average_weighted_similarity=('Weighted_Similarity_%', 'mean')
            ).reset_index()

            # Round the values to 2 decimal places
            overall_similarity[['average_weighted_similarity', 'average_text_similarity', 'average_structural_similarity']] = overall_similarity[
                ['average_weighted_similarity', 'average_text_similarity', 'average_structural_similarity']].round(2)

            # Sort by weighted similarity
            overall_similarity = overall_similarity.sort_values(by='average_weighted_similarity', ascending=False)

            # Create a summary of counts for each color-coded range
            def count_by_similarity_range(df):
                return {
                    'Blue (0%)': df[df['average_weighted_similarity'] == 0].shape[0],
                    'Green (1% - 24%)': df[df['average_weighted_similarity'].between(1, 24)].shape[0],
                    'Yellow (25% - 49%)': df[df['average_weighted_similarity'].between(25, 49)].shape[0],
                    'Orange (50% - 74%)': df[df['average_weighted_similarity'].between(50, 74)].shape[0],
                    'Red (75% - 100%)': df[df['average_weighted_similarity'] >= 75].shape[0]
                }

            # Generate the summary
            filtered_overall_summary = count_by_similarity_range(overall_similarity)

            # Display the summary in a table with color-coding
            summary_df = pd.DataFrame(list(filtered_overall_summary.items()), columns=['Range', 'Count'])

            def color_rows(row):
                if 'Blue' in row['Range']:
                    return ['background-color: #6A9AB0'] * len(row)
                elif 'Green' in row['Range']:
                    return ['background-color: #557C56'] * len(row)
                elif 'Yellow' in row['Range']:
                    return ['background-color: #EEDF7A'] * len(row)
                elif 'Orange' in row['Range']:
                    return ['background-color: #D8A25E'] * len(row)
                elif 'Red' in row['Range']:
                    return ['background-color: #A04747'] * len(row)
                return [''] * len(row)

            # Apply the color coding and display the table
            st.dataframe(summary_df.style.apply(color_rows, axis=1))

        st.subheader('Histograms of Similarity Metrics')

        # Interpretation for "Histograms of Similarity Metrics"
        with st.expander("📝"):
            st.subheader("Interpretation of Histograms")
            st.write("""
                - **Text Similarity Histogram**: This histogram shows the distribution of text similarity scores across the dataset. A concentration of bars at higher percentages indicates a greater number of code pairs with similar text.
                - **Structural Similarity Histogram**: The structural similarity histogram visualizes how similar the structures of the code pairs are. Peaks in the lower ranges suggest more varied structural designs, while higher values indicate structural consistency.
                - **Weighted Similarity Histogram**: The weighted similarity metric combines both text and structural similarities. A skew toward higher percentages might suggest that most code pairs are both textually and structurally similar. A balanced distribution across all ranges would indicate varied similarities across the dataset.
            """)

        # Rename columns for consistency and better readability in the histograms
        filtered_df = filtered_df.rename(columns={
            'Text_Similarity_%': 'Text Similarity %',
            'Structural_Similarity_%': 'Structural Similarity %',
            'Weighted_Similarity_%': 'Weighted Similarity %'
        })

        # Define the custom color scale based on the similarity score thresholds
        color_scale = alt.Scale(
            domain=[0, 1, 25, 50, 75, 100],
            range=['#6A9AB0', '#557C56', '#EEDF7A', '#D8A25E', '#A04747']  # Blue, Green, Yellow, Orange, Red
        )

        # Create histograms for each similarity metric
        for column in ['Text Similarity %', 'Structural Similarity %', 'Weighted Similarity %']:
            hist_chart = alt.Chart(filtered_df).mark_bar().encode(
                alt.X(column, bin=alt.Bin(maxbins=30), title=column),
                y=alt.Y('count()', title='Frequency'),
                color=alt.Color(column, scale=color_scale, legend=None),  # Apply color based on similarity score
                tooltip=[column, 'count()']
            ).properties(
                width=300,
                height=300,
                title=f'Distribution of {column}'
            )

            st.altair_chart(hist_chart, use_container_width=True)

        # Download button for filtered data in the sidebar
        st.sidebar.download_button(
            label="Download Filtered Data as CSV",
            data=filtered_df.to_csv(index=False),
            file_name='filtered_data.csv',
            mime='text/csv'
        )
    else:
        st.error('The uploaded file does not contain the required columns.')
else:
    st.info('Please upload a CSV file to analyze.')
