import streamlit as st
import pandas as pd
from Week_4.frontend import ingest_syllabus, get_uploaded_files, get_chat_analytics, delete_uploaded_file

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
        st.header("🗂️ Uploaded Documents Registry")
        try:
            files = get_uploaded_files()
            if files:
                # Add CSS styling for custom badges and cards
                st.markdown("""
                    <style>
                    .file-title {
                        font-size: 1.05rem;
                        font-weight: 600;
                        color: #0f172a;
                        margin-bottom: 4px;
                    }
                    .date-text {
                        color: #64748b;
                        font-size: 0.85rem;
                        font-weight: 400;
                        margin-top: 4px;
                    }
                    .chunk-badge {
                        background-color: #f0fdf4;
                        color: #166534;
                        border: 1px solid #bbf7d0;
                        padding: 4px 12px;
                        border-radius: 9999px;
                        font-size: 0.8rem;
                        font-weight: 600;
                        display: inline-block;
                        margin-top: 2px;
                    }
                    </style>
                """, unsafe_allow_html=True)

                # Render table headers using nice looking markdown
                col_h1, col_h2, col_h3, col_h4 = st.columns([4, 3, 2, 2])
                with col_h1:
                    st.markdown("**📄 Filename**")
                with col_h2:
                    st.markdown("**📅 Uploaded At**")
                with col_h3:
                    st.markdown("**🧩 Chunks**")
                with col_h4:
                    st.markdown("**⚙️ Action**")
                st.markdown("<hr style='margin: 8px 0 16px 0; border: none; border-top: 1px solid #e2e8f0;' />", unsafe_allow_html=True)
                
                # Rows
                for idx, file in enumerate(files):
                    fname = file.get("filename")
                    uploaded_at = file.get("timestamp")
                    chunks = file.get("chunks")
                    
                    with st.container(border=True):
                        col1, col2, col3, col4 = st.columns([4, 3, 2, 2])
                        with col1:
                            st.markdown(f'<div class="file-title">{fname}</div>', unsafe_allow_html=True)
                        with col2:
                            st.markdown(f'<div class="date-text">{uploaded_at}</div>', unsafe_allow_html=True)
                        with col3:
                            st.markdown(f'<div class="chunk-badge">{chunks} Chunks</div>', unsafe_allow_html=True)
                        with col4:
                            if st.button("🗑️ Delete", key=f"del_{fname}_{idx}", type="secondary", use_container_width=True):
                                with st.spinner(f"Deleting {fname}..."):
                                    try:
                                        res = delete_uploaded_file(fname)
                                        st.toast(f"✅ Deleted {fname} successfully!")
                                        st.rerun()
                                    except Exception as err:
                                        st.error(f"Failed to delete: {err}")
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
                            f"<span style='background:#dbeafe;color:#1e3a8a;padding:2px 10px;"
                            f"border-radius:12px;font-size:0.82em;font-weight:600;'>{count_val} times</span>",
                            unsafe_allow_html=True
                        )
                        st.markdown("<div style='margin-bottom:8px'></div>", unsafe_allow_html=True)
                else:
                    st.info("No repeated syllabus questions found yet. More student interactions are needed to identify top topics.")
                    
            except Exception as e:
                st.error(f"Error fetching analytics: {e}")
