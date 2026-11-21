import streamlit as st
import os, base64
import io

st.set_page_config(page_title="Exam Tracker", layout="centered")
st.title("5th Semester - Exam Preparation Tracker")

def show_pdf_file(file_bytes, file_name):
    # PDF aithe akkade PDF laaga chupinchu
    if file_name.lower().endswith(".pdf"):
        base64_pdf = base64.b64encode(file_bytes).decode('utf-8')
        pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="600" type="application/pdf"></iframe>'
        st.markdown(pdf_display, unsafe_allow_html=True)
        st.download_button("Download PDF", file_bytes, file_name=file_name, mime="application/pdf")

    # DOCX aithe akkade text laaga chupinchu - download cheyakunda chaduvukochu
    elif file_name.lower().endswith(".docx"):
        try:
            from docx import Document
            doc = Document(io.BytesIO(file_bytes))
            st.success(f"Reading: {file_name} - Akkade chaduvukondi")
            for para in doc.paragraphs:
                text = para.text.strip()
                if not text:
                    continue
                if para.style.name.startswith("Heading"):
                    st.subheader(text)
                else:
                    st.write(text)
            # Tables unte chupinchu
            for table in doc.tables:
                st.write("---")
                for row in table.rows:
                    st.write(" | ".join([cell.text for cell in row.cells]))
            st.divider()
            st.download_button("Download Word File (optional)", file_bytes, file_name=file_name)
        except Exception as e:
            st.error(f"Docx chadavadam lo error: {e}")
            st.download_button("Download File", file_bytes, file_name=file_name)

    else:
        st.info(f"File: {file_name}")
        st.download_button("Download File", file_bytes, file_name=file_name)

def show_pdf(pdf_path):
    if os.path.exists(pdf_path):
        with open(pdf_path, "rb") as f:
            show_pdf_file(f.read(), os.path.basename(pdf_path))
    else:
        st.error(f"Notes PDF not found: {pdf_path}")
        st.write("**Files actually found in notes folder:**")
        if os.path.exists("notes"):
            files = os.listdir("notes")
            if len(files) == 0:
                st.write("notes folder is EMPTY")
            else:
                for fl in files:
                    st.write(f"- {fl}")
        else:
            st.write("notes folder DOES NOT EXIST")
        st.write("---")
        st.write("**Or Upload file directly here:**")
        uploaded = st.file_uploader("Upload Notes for this Module", type=["pdf", "docx", "pptx"], key=f"up_{pdf_path}")
        if uploaded is not None:
            show_pdf_file(uploaded.read(), uploaded.name)

DATA = {
    "STA - Exam: 23 Nov": {
        "Unit I": ["Black Box vs White Box Testing", "STLC and V-Model", "Levels of Testing"],
        "Unit II": ["Test Planning", "Test Strategy vs Test Plan", "Entry and Exit Criteria"],
        "Unit III": ["Boundary Value Testing", "Equivalence Class Testing", "Path Testing"],
        "Unit IV": ["Load, Stress, Volume Testing", "Agile Testing", "Web and Mobile Testing"],
        "Unit V": ["Selenium WebDriver", "Locating Web Elements", "TestNG"],
    },
    "PD - Exam: 25 Nov": {
        "Module 1": ["Self-Esteem - Two Pillars, Johari Window", "Fixed vs Growth Mindset", "SMART Framework, Habit, Procrastination", "Case Study - Anya, Marcus"],
        "Module 2": ["ABC Model of Attitude, Cognitive Dissonance", "Emotional Contagion, Self-Fulfilling Prophecy", "Reframing - Three Lenses, Gratitude", "Case Studies - Sarah, David"],
        "Module 3": ["Intrinsic vs Extrinsic Motivation", "Locus of Control, Be Responsible", "Pareto 80/20, Eisenhower Matrix, Pomodoro", "Eustress vs Distress, 4 As of Stress", "Critical Thinking - 5 Whys, 6 Hats, SCAMPER", "Case Studies - Maria, Alex, David"],
        "Module 4": ["Mutual Expectations", "Managing Up", "Giving and Receiving Feedback", "Make Your Supervisor Look Good", "Case Studies - Sarah, David"],
        "Module 5": ["First Day - Halo Effect, 7-Second Rule", "First Day Checklist, Elevator Pitch", "Keeping Your Job - Reliability, Compliance", "Going Beyond Minimum", "Planning Your Career - 5 Year Vision", "Roadmap - Short, Medium, Long Term", "Moving Ahead - Visibility, Mentor vs Sponsor", "Stretch Assignment, Pivot, Door Rule", "Case Studies - James, Maria, David"],
    },
    "ML - Exam: 27 Nov": {
        "Module 1": ["Introduction to ML, Well-Posed Problems", "FIND-S, Candidate Elimination"],
        "Module 2": ["Decision Tree, Entropy, Information Gain", "ID3 Algorithm, Kernel Machines"],
        "Module 3": ["ANN, Perceptron, Activation Functions", "Backpropagation, Gradient Descent"],
        "Module 4": ["Bayesian Learning, MLE", "Bayes Optimal, Naive Bayes, EM Algorithm"],
        "Module 5": ["k-NN, LWR, CBR", "Reinforcement Learning, Q-Learning, TD Learning"],
    }
}

PDF_MAP = {
    "STA - Exam: 23 Nov|Unit I": "notes/STA - UNIT I.docx",
    "STA - Exam: 23 Nov|Unit II": "notes/STA - UNIT II.docx",
    "STA - Exam: 23 Nov|Unit III": "notes/STA - UNIT III.docx",
    "STA - Exam: 23 Nov|Unit IV": "notes/STA - UNIT IV.docx",
    "STA - Exam: 23 Nov|Unit V": "notes/STA - UNIT V.docx",
    "PD - Exam: 25 Nov|Module 1": "notes/PDCourseMaterialModule1.docx",
    "PD - Exam: 25 Nov|Module 2": "notes/PDCourseMaterialModule2.docx",
    "PD - Exam: 25 Nov|Module 3": "notes/PDCourseMaterialModule3.docx",
    "PD - Exam: 25 Nov|Module 4": "notes/PDCourseMaterialModule4.docx",
    "PD - Exam: 25 Nov|Module 5": "notes/PDCourseMaterialModule5.docx",
    "ML - Exam: 27 Nov|Module 1": "notes/ML_MATERIAL_M1.pdf",
    "ML - Exam: 27 Nov|Module 2": "notes/ML_M2_Capter1_PPT.pdf",
    "ML - Exam: 27 Nov|Module 3": "notes/ML_M3_PPT.pdf",
    "ML - Exam: 27 Nov|Module 4": "notes/ML_M4_PPT.pdf",
    "ML - Exam: 27 Nov|Module 5": "notes/ML_M5_PPT.pdf",
}

QUIZ = {
    "STA - Exam: 23 Nov": [
        {"q": "What is the first phase in STLC?", "options": ["Test Planning", "Requirement Analysis", "Test Execution", "Test Closure"], "answer": "Requirement Analysis"},
        {"q": "In Black Box Testing, what do we test?", "options": ["Internal Code", "Functionality without seeing code", "Database", "Hardware"], "answer": "Functionality without seeing code"},
        {"q": "Boundary Value Testing example?", "options": ["0, 1, 100, 101", "Only 50", "Random values", "Only 0"], "answer": "0, 1, 100, 101"},
        {"q": "What is Selenium WebDriver used for?", "options": ["Web Automation Testing", "Mobile Only", "Database Testing", "API Only"], "answer": "Web Automation Testing"},
        {"q": "What is TestNG?", "options": ["Testing Framework for Java", "Database", "Browser", "OS"], "answer": "Testing Framework for Java"},
    ],
    "PD - Exam: 25 Nov": [
        {"q": "In SMART, what does S stand for?", "options": ["Specific", "Simple", "Strong", "Slow"], "answer": "Specific"},
        {"q": "What is Growth Mindset?", "options": ["Abilities can be developed", "Born talented only", "Never change", "Avoid challenges"], "answer": "Abilities can be developed"},
        {"q": "What does Johari Window contain?", "options": ["Open, Blind, Hidden, Unknown", "Only Open", "Good, Bad", "Past, Future"], "answer": "Open, Blind, Hidden, Unknown"},
        {"q": "What is Pareto 80/20 Rule?", "options": ["80% results from 20% efforts", "80% work always", "20% only", "100% equal"], "answer": "80% results from 20% efforts"},
        {"q": "In Eisenhower Matrix, Urgent + Important should be?", "options": ["Do Now", "Delete", "Delegate", "Schedule"], "answer": "Do Now"},
    ],
    "ML - Exam: 27 Nov": [
        {"q": "What does FIND-S algorithm do?", "options": ["Finds most specific hypothesis", "Random guess", "Deletes data", "Sorts data"], "answer": "Finds most specific hypothesis"},
        {"q": "What is Entropy?", "options": ["Measure of impurity / disorder", "Accuracy", "Speed", "Size"], "answer": "Measure of impurity / disorder"},
        {"q": "What is activation function used for in Perceptron?", "options": ["To decide the output", "To delete data", "For speed", "For storage"], "answer": "To decide the output"},
        {"q": "Naive Bayes is based on?", "options": ["Bayes Theorem", "Pythagoras", "Newton Law", "Ohm Law"], "answer": "Bayes Theorem"},
        {"q": "What is Q-Learning?", "options": ["Reinforcement Learning", "Supervised Only", "Unsupervised Only", "No Learning"], "answer": "Reinforcement Learning"},
    ]
}

if "subject" not in st.session_state: st.session_state.subject = None
if "module" not in st.session_state: st.session_state.module = None
if "done_topics" not in st.session_state: st.session_state.done_topics = set()
if "page" not in st.session_state: st.session_state.page = "home"
if "quiz_answers" not in st.session_state: st.session_state.quiz_answers = {}

if st.session_state.page == "home":
    st.subheader("Step 1: Select Subject")
    for subj in DATA.keys():
        total = sum(len(v) for v in DATA[subj].values())
        done = sum(1 for m in DATA[subj] for t in DATA[subj][m] if f"{subj}|{m}|{t}" in st.session_state.done_topics)
        if st.button(f"{subj}  -  {done}/{total} Done", key=subj, use_container_width=True):
            st.session_state.subject = subj
            st.session_state.page = "modules"
            st.rerun()

elif st.session_state.page == "modules":
    subj = st.session_state.subject
    st.subheader(f"Step 2: {subj} - Select Module")
    if st.button("Back to Subjects"):
        st.session_state.page = "home"
        st.session_state.subject = None
        st.rerun()
    for mod in DATA[subj].keys():
        topics = DATA[subj][mod]
        done = sum(1 for t in topics if f"{subj}|{mod}|{t}" in st.session_state.done_topics)
        status = "Done" if done == len(topics) else f"{done}/{len(topics)}"
        if st.button(f"{mod}  -  {status}", key=mod, use_container_width=True):
            st.session_state.module = mod
            st.session_state.page = "topics"
            st.rerun()
    all_done = all(f"{subj}|{m}|{t}" in st.session_state.done_topics for m in DATA[subj] for t in DATA[subj][m])
    if all_done:
        st.success("All Modules Completed!")
        if st.button("TEST YOUR KNOWLEDGE", use_container_width=True, type="primary"):
            st.session_state.page = "quiz"
            st.rerun()

elif st.session_state.page == "topics":
    subj = st.session_state.subject
    mod = st.session_state.module
    st.subheader(f"Step 3: {subj} - {mod}")
    if st.button("Back to Modules"):
        st.session_state.page = "modules"
        st.rerun()
    pdf_key = f"{subj}|{mod}"
    pdf_path = PDF_MAP.get(pdf_key, "")
    st.info(f"{mod} Notes - You can view it here")
    if st.button(f"Open {mod} Notes", use_container_width=True):
        st.session_state.show_pdf = not st.session_state.get("show_pdf", False)
    if st.session_state.get("show_pdf", False):
        show_pdf(pdf_path)
    st.divider()
    st.write("Topics - Click a topic to open, mark Done after reading:")
    for t in DATA[subj][mod]:
        key = f"{subj}|{mod}|{t}"
        with st.expander(f"{t}"):
            st.write(f"Topic: {t}")
            st.write("Read the notes for this topic, then mark it as Done below.")
            checked = st.checkbox(f"Done - {t}", value=key in st.session_state.done_topics, key=f"chk_{key}")
            if checked:
                st.session_state.done_topics.add(key)
            else:
                st.session_state.done_topics.discard(key)
    st.divider()
    mods = list(DATA[subj].keys())
    idx = mods.index(mod)
    if idx + 1 < len(mods):
        if st.button(f"Next Module - {mods[idx+1]}", use_container_width=True, type="primary"):
            st.session_state.module = mods[idx+1]
            st.session_state.show_pdf = False
            st.rerun()
    else:
        if st.button("Finish - Go to Modules", use_container_width=True, type="primary"):
            st.session_state.page = "modules"
            st.rerun()

elif st.session_state.page == "quiz":
    subj = st.session_state.subject
    st.subheader(f"Test Your Knowledge - {subj}")
    if st.button("Back"):
        st.session_state.page = "modules"
        st.rerun()
    questions = QUIZ[subj]
    for i, q in enumerate(questions):
        st.write(f"**Q{i+1}. {q['q']}**")
        st.session_state.quiz_answers[i] = st.radio("Choose:", q["options"], key=f"quiz_{i}", index=None)
    if st.button("Submit Test", type="primary", use_container_width=True):
        score = sum(1 for i, q in enumerate(questions) if st.session_state.quiz_answers.get(i) == q["answer"])
        st.success(f"Your Score: {score} / {len(questions)}")
        if score == len(questions):
            st.balloons()
            st.write("Perfect! You are ready!")
        elif score >= 3:
            st.write("Good! A little more revision is enough.")
        else:
            st.write("Please read the modules again, you can do it.")
        for i, q in enumerate(questions):
            st.write(f"Q{i+1}: {q['answer']}")