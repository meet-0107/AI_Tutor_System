import streamlit as st
import uuid
from Week_4.frontend import (
    stream_chat_response, 
    get_chat_history, 
    generate_quiz, 
    get_suggested_questions,
    generate_flashcards,
    generate_mindmap
)
from Week_4.frontend.components import display_chat_history, render_chat_message

def render():
    st.title("🎓 Student Dashboard")
    st.markdown("Interact with the AI Tutor, practice with quizzes.")

    # Active Tab state initialization
    if "active_tab_index" not in st.session_state or st.session_state.active_tab_index >= 3:
        st.session_state.active_tab_index = 0

    # Stable session_id initialization
    if "session_id" not in st.session_state:
        st.session_state.session_id = str(uuid.uuid4())

    # Load messages if not already in session_state
    if "messages" not in st.session_state:
        try:
            st.session_state.messages = get_chat_history(st.session_state.session_id)
        except Exception:
            st.session_state.messages = []

    # Render horizontal radio buttons as custom navigation bar
    tabs = ["💬 AI Tutor Chat", "📝 Practice Quiz", "🧠 Concept Mind Map"]
    active_tab = st.radio(
        "student_nav",
        tabs,
        index=st.session_state.active_tab_index,
        horizontal=True,
        label_visibility="collapsed"
    )
    st.session_state.active_tab_index = tabs.index(active_tab)
    st.markdown("---")

    # 1. AI Tutor Chat Tab
    if st.session_state.active_tab_index == 0:
        col1, col2 = st.columns([3, 1])
        with col1:
            st.subheader("💬 Chat with AI Tutor")
        with col2:
            with st.popover("⚡ Generate Flashcards"):
                fc_topic = st.text_input("Enter Topic for Flashcards")
                if st.button("Generate", key="fc_gen", use_container_width=True):
                    if fc_topic.strip():
                        with st.spinner("Extracting from syllabus..."):
                            try:
                                # Locally append user message to keep UI in sync
                                user_prompt = f"Generate flashcards for: {fc_topic.strip()}"
                                st.session_state.messages.append({
                                    "role": "user",
                                    "content": user_prompt
                                })
                                
                                # Call API with session_id
                                flashcards_data = generate_flashcards(fc_topic.strip(), st.session_state.session_id)
                                
                                st.session_state.messages.append({
                                    "role": "assistant",
                                    "type": "flashcards",
                                    "content": flashcards_data
                                })
                                st.rerun()
                            except Exception as e:
                                st.error(f"Error generating flashcards: {e}")
                    else:
                        st.warning("Please enter a topic.")
        
        # Check if there is an auto_prompt queued from suggestions click
        if "auto_prompt" in st.session_state and st.session_state.auto_prompt:
            prompt = st.session_state.auto_prompt
            st.session_state.auto_prompt = None
            
            # Save and display user question
            st.session_state.messages.append({"role": "user", "content": prompt})
            display_chat_history(st.session_state.messages[:-1])
            render_chat_message("user", prompt)
            
            # Stream assistant response
            with st.chat_message("assistant"):
                message_placeholder = st.empty()
                full_response = ""
                try:
                    for token in stream_chat_response(prompt, st.session_state.session_id):
                        full_response += token
                        message_placeholder.markdown(full_response + "▌")
                    message_placeholder.markdown(full_response)
                    st.session_state.messages.append({"role": "assistant", "content": full_response})
                    st.rerun()
                except Exception as e:
                    st.error(f"Error communicating with backend: {e}")
        else:
            # Regular chat render
            display_chat_history(st.session_state.messages)
            
            if prompt := st.chat_input("Ask a question..."):
                st.session_state.messages.append({"role": "user", "content": prompt})
                render_chat_message("user", prompt)
                
                with st.chat_message("assistant"):
                    message_placeholder = st.empty()
                    full_response = ""
                    try:
                        for token in stream_chat_response(prompt, st.session_state.session_id):
                            full_response += token
                            message_placeholder.markdown(full_response + "▌")
                        message_placeholder.markdown(full_response)
                        st.session_state.messages.append({"role": "assistant", "content": full_response})
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error communicating with backend: {e}")

    # 2. Practice Quiz Tab
    elif st.session_state.active_tab_index == 1:
        st.subheader("📝 Practice Quiz")
        st.markdown("Generate a 5-question multiple-choice quiz on any specific topic to test your knowledge.")
        
        quiz_topic = st.text_input("Enter Topic (e.g., Linear Regression, Deep Learning)", key="quiz_topic_input")
        
        if st.button("Generate Quiz", type="primary"):
            if quiz_topic.strip():
                with st.spinner("Generating 5 multiple-choice questions..."):
                    try:
                        quiz = generate_quiz(quiz_topic.strip(), st.session_state.session_id)
                        st.session_state.current_quiz = quiz
                        st.session_state.quiz_answers = {}
                        st.session_state.quiz_submitted = False
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error generating quiz: {e}")
            else:
                st.warning("Please enter a topic first.")

        if "current_quiz" in st.session_state and st.session_state.current_quiz:
            quiz = st.session_state.current_quiz
            st.markdown(f"### Practice Quiz: **{quiz_topic}**")
            
            if not st.session_state.quiz_submitted:
                with st.form("quiz_form"):
                    answers = {}
                    for i, q in enumerate(quiz.get("questions", [])):
                        st.markdown(f"**Q{i+1}: {q['question_text']}**")
                        options = q["options"]
                        answers[i] = st.radio(
                            f"Options for Q{i+1}",
                            options,
                            key=f"quiz_radio_{i}",
                            index=None,
                            label_visibility="collapsed"
                        )
                        st.markdown("<br/>", unsafe_allow_html=True)
                        
                    submit_quiz = st.form_submit_button("Submit Quiz", type="primary", use_container_width=True)
                    if submit_quiz:
                        st.session_state.quiz_answers = answers
                        st.session_state.quiz_submitted = True
                        st.rerun()
            else:
                score = 0
                questions = quiz.get("questions", [])
                for i, q in enumerate(questions):
                    user_ans = st.session_state.quiz_answers.get(i)
                    correct_ans = q["correct_answer"]
                    if user_ans == correct_ans:
                        score += 1
                        
                st.success(f"### 🎉 Quiz Completed! Your Score: {score} / {len(questions)}")
                st.markdown("---")
                
                for i, q in enumerate(questions):
                    user_ans = st.session_state.quiz_answers.get(i)
                    correct_ans = q["correct_answer"]
                    is_correct = (user_ans == correct_ans)
                    
                    st.markdown(f"#### Q{i+1}: {q['question_text']}")
                    if user_ans:
                        st.markdown(f"Your Answer: `{user_ans}`")
                    else:
                        st.markdown("Your Answer: *(None Selected)*")
                        
                    if is_correct:
                        st.markdown("✅ **Correct!**")
                    else:
                        st.markdown(f"❌ **Incorrect.** Correct Answer: `{correct_ans}`")
                        
                    st.info(f"**Explanation:** {q['explanation']}")
                    st.markdown("<hr/>", unsafe_allow_html=True)
                    
                if st.button("Try Another Quiz", use_container_width=True):
                    st.session_state.current_quiz = None
                    st.session_state.quiz_submitted = False
                    st.session_state.quiz_answers = {}
                    st.rerun()

    # 3. Concept Mind Map Tab
    elif st.session_state.active_tab_index == 2:
        st.subheader("🧠 Concept Mind Map")
        st.markdown("Generate an interactive visual concept map on any syllabus topic.")
        
        map_topic = st.text_input("Enter Topic (e.g., Linear Regression, Neural Networks)", key="map_topic_input")
        
        if st.button("Generate Mind Map", type="primary"):
            if map_topic.strip():
                with st.spinner("Analyzing syllabus and generating mind map..."):
                    try:
                        result = generate_mindmap(map_topic.strip(), st.session_state.session_id)
                        st.session_state.current_mindmap = result.get("mermaid_code")
                        # Add user request and assistant reply locally to st.session_state.messages
                        st.session_state.messages.append({
                            "role": "user",
                            "content": f"Generate mind map for: {map_topic.strip()}"
                        })
                        st.session_state.messages.append({
                            "role": "assistant",
                            "type": "mindmap",
                            "content": result.get("mermaid_code")
                        })
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error generating mind map: {e}")
            else:
                st.warning("Please enter a topic first.")

        if "current_mindmap" in st.session_state and st.session_state.current_mindmap:
            st.markdown("### Visual Diagram")
            import streamlit.components.v1 as components
            html_code = f"""
            <div class="mermaid" style="display: flex; justify-content: center; align-items: center; background: white; padding: 20px; border-radius: 12px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05);">
                {st.session_state.current_mindmap}
            </div>
            <script type="module">
                import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
                mermaid.initialize({{ startOnLoad: true, theme: 'neutral' }});
            </script>
            """
            components.html(html_code, height=500, scrolling=True)
