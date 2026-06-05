import streamlit as st

def render_chat_message(role: str, content: str, msg_type: str = "text"):
    """
    Renders a single chat message in the Streamlit UI.
    Supports standard text and custom 'flashcards' types.
    """
    with st.chat_message(role):
        if msg_type == "flashcards":
            st.markdown("### ⚡Flashcards")
            try:
                # The content might be a dict or a string depending on serialization
                import json
                if isinstance(content, str):
                    data = json.loads(content)
                else:
                    data = content
                
                cards = data.get("flashcards", [])
                
                # Render using custom HTML structure that CSS will flip
                for i, card in enumerate(cards):
                    flip_html = f"""
                    <div class="flip-card">
                      <div class="flip-card-inner">
                        <div class="flip-card-front">
                          <h4>Term</h4>
                          <h2>{card.get('term', '')}</h2>
                          <p><i>(Hover to flip)</i></p>
                        </div>
                        <div class="flip-card-back">
                          <h4>Definition</h4>
                          <p>{card.get('definition', '')}</p>
                        </div>
                      </div>
                    </div>
                    """
                    st.markdown(flip_html, unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Could not render flashcards: {e}")
        elif msg_type == "mindmap":
            st.markdown("### 🧠 Concept Mind Map")
            try:
                import streamlit.components.v1 as components
                html_code = f"""
                <div class="mermaid" style="display: flex; justify-content: center; align-items: center; background: white; padding: 20px; border-radius: 12px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05);">
                    {content}
                </div>
                <script type="module">
                    import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
                    mermaid.initialize({{ startOnLoad: true, theme: 'neutral' }});
                </script>
                """
                components.html(html_code, height=450, scrolling=True)
            except Exception as e:
                st.error(f"Could not render mind map: {e}")
        else:
            st.markdown(content)

def display_chat_history(messages: list):
    """
    Renders the entire chat history.
    """
    for msg in messages:
        msg_type = msg.get("type", "text")
        render_chat_message(msg["role"], msg["content"], msg_type)
