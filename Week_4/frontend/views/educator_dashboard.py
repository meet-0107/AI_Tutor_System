import streamlit as st
import pandas as pd
from Week_4.frontend import ingest_syllabus, get_uploaded_files, get_chat_analytics

def render():
    st.title("👨‍🏫 Educator Dashboard")
    st.markdown("Monitor student learning activity, manage syllabus materials, and address curriculum gaps.")

    # Create tabs for clean separation of concerns
    tab_syllabus, tab_analytics = st.tabs(["📚 Syllabus Management", "📊 Student Analytics"])

    with tab_syllabus:
        st.header("Upload Syllabus & Materials")
        st.markdown("Upload additional PDF course materials to expand the AI Tutor's knowledge base.")
        
        uploaded_file = st.file_uploader("Choose a PDF file", type="pdf", key="syllabus_uploader")

        if st.button("Upload and Process", key="upload_button", type="primary"):
            if uploaded_file is not None:
                with st.spinner("Processing document..."):
                    try:
                        result = ingest_syllabus(uploaded_file)
                        st.success(f"Successfully processed {result.get('num_chunks', 'unknown')} chunks!")
                        st.rerun()  # Rerun to update the file registry table instantly
                    except Exception as e:
                        st.error(f"Error processing file: {e}")
            else:
                st.warning("Please upload a file first.")

        st.markdown("---")
        st.header("Uploaded Documents Registry")
        try:
            files = get_uploaded_files()
            if files:
                # Create a neat dataframe
                df = pd.DataFrame(files)
                # Rename columns for presentation
                df.columns = ["Filename", "Uploaded At", "Chunks Processed"]
                # Shift index to start from 1
                df.index = df.index + 1
                # Display table
                st.dataframe(df, use_container_width=True)
            else:
                st.info("No documents have been uploaded to the registry yet.")
        except Exception as e:
            st.error(f"Could not load uploaded files list: {e}")

    with tab_analytics:
        st.header("Student Interactions & Analytics")
        st.markdown("AI-generated analysis based on recent questions asked by students to identify the top topics of interest.")

        # Let user refresh analytics manually
        if st.button("🔄 Refresh Analytics", key="refresh_analytics_btn"):
            st.rerun()
        
        with st.spinner("Analyzing student queries..."):
            try:
                analytics = get_chat_analytics()
                top_topics = analytics.get("top_topics", [])
                
                
                st.subheader("🔥 Top Topics Asked by Students")
                if top_topics:
                    # Sort by frequency descending
                    top_topics = sorted(top_topics, key=lambda x: x.get("count", 0), reverse=True)
                    medals = ["🥇", "🥈", "🥉"]
                    for idx, item in enumerate(top_topics):
                        count_val = item.get("count", 0)
                        topic_name = item.get("topic", "")
                        medal = medals[idx] if idx < 3 else "🔹"
                        st.markdown(
                            f"{medal} **{topic_name}** &nbsp;&nbsp; "
                            f"<span style='background:#1e40af;color:white;padding:2px 10px;"
                            f"border-radius:12px;font-size:0.82em;'>{count_val} times</span>",
                            unsafe_allow_html=True
                        )
                        st.markdown("<div style='margin-bottom:8px'></div>", unsafe_allow_html=True)
                else:
                    st.info("No repeated syllabus questions found yet. More student interactions are needed to identify top topics.")
                    
            except Exception as e:
                st.error(f"Error fetching analytics: {e}")
