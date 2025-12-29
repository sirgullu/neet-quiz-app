import streamlit as st
import pandas as pd

# 1. Page Configuration
st.set_page_config(page_title="My NEET Quiz", page_icon="🧬")

# 2. Load Data
@st.cache_data 
def load_data():
    try:
        df = pd.read_csv("questions.csv")
        return df
    except FileNotFoundError:
        return pd.DataFrame()

df = load_data()

# 3. Sidebar: User Controls
st.sidebar.header("⚙️ Quiz Settings")

if not df.empty:
    # Get unique chapters
    all_chapters = df['chapter'].unique().tolist()
    
    # User selects chapters
    selected_chapters = st.sidebar.multiselect(
        "Select Chapters to Revise:",
        all_chapters,
        default=all_chapters[0]
    )
    
    # Filter questions
    quiz_data = df[df['chapter'].isin(selected_chapters)]

    # 4. Main Interface
    st.title("🧬 NEET Practice Quiz")
    st.markdown("---")

    # 5. Display Questions
    if not quiz_data.empty:
        for index, row in quiz_data.iterrows():
            st.subheader(f"Q: {row['question']}")
            
            user_choice = st.radio(
                "Choose an answer:",
                [row['option_a'], row['option_b'], row['option_c'], row['option_d']],
                index=None,
                key=f"q_{index}"
            )
            
            if st.button(f"Check Answer", key=f"btn_{index}"):
                # Compare user choice with the text in the correct option column
                correct_option_label = row['correct_option'].lower() # e.g. 'option_b'
                
                # We need to map 'option_b' (the column name) to the actual answer text (e.g., 'Mitochondria')
                # But looking at your CSV, I made it easier: 
                # The 'correct_option' column ALREADY contains the text answer (e.g. "Species") 
                # OR it contains the option key (e.g. "option_a").
                
                # Let's handle both cases to be safe:
                correct_answer_text = str(row['correct_option']).strip()
                
                # If the CSV says "option_a", we grab the text from the option_a column
                if correct_answer_text in ['option_a', 'option_b', 'option_c', 'option_d']:
                    correct_answer_text = row[correct_answer_text]

                if user_choice == correct_answer_text:
                    st.success(f"✅ Correct! {row['explanation']}")
                else:
                    st.error(f"❌ Incorrect. The answer is: {correct_answer_text}")
                    st.info(f"ℹ️ {row['explanation']}")
            st.markdown("---")
    else:
        st.info("Select a chapter to start!")
else:
    st.write("Could not find questions.csv. Please check the file name.")