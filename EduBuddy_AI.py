# app.py
import streamlit as st
import random
import pandas as pd
import numpy as np
from transformers import pipeline
from fuzzywuzzy import process
from deep_translator import GoogleTranslator

# Set up the Streamlit app
st.set_page_config(page_title="EduBuddy AI Chatbot", page_icon="🎓", layout="wide")

# Load NLP models
@st.cache_resource
def load_models():
    # Load GPT-2 model for text generation
    text_generator = pipeline("text-generation", model="gpt2")
    return text_generator

text_generator = load_models()

# Define the AI Education Assistant Class
class AI_Education_Assistant:
    def __init__(self):
        self.lessons = {
            "math": ["Counting", "Addition", "Multiplication", "Algebra", "Geometry"],
            "science": ["Weather", "Water Cycle", "Photosynthesis", "Solar System"],
            "english": ["Phonics", "Storytelling", "Grammar", "Creative Writing"],
            "history": ["Ancient Civilizations", "World Wars", "Historical Figures"]
        }
        self.subjects = list(self.lessons.keys())

    def get_lesson(self, subject, grade_level=None):
        subject = self._correct_subject(subject)
        if subject:
            lesson_topic = random.choice(self.lessons[subject])
            prompt = f"Create a {grade_level if grade_level else ''} {subject} lesson on {lesson_topic}."
            ai_lesson = text_generator(prompt, max_length=200, num_return_sequences=1)
            return ai_lesson[0]['generated_text']
        else:
            return "Subject not found!"

    def _correct_subject(self, input_subject):
        input_subject = input_subject.lower().strip()
        match, score = process.extractOne(input_subject, self.subjects)
        if score >= 70:
            return match
        return None

    def get_parent_report(self, student_name, language="english"):
        attendance = np.random.randint(80, 100)
        performance = np.random.choice(["Excellent", "Good", "Needs Improvement"])
        report = f"{student_name}'s Attendance: {attendance}% \nPerformance: {performance}"
        if language.lower() == "urdu":
            # Translate the report to Urdu using deep-translator
            translated_report = GoogleTranslator(source='auto', target='ur').translate(report)
            return translated_report
        return report

# Initialize the AI Assistant
ai_assistant = AI_Education_Assistant()

# Initialize session state for student data
if 'student_data' not in st.session_state:
    st.session_state.student_data = {}

# Streamlit UI
st.title("🎓 EduBuddy AI Chatbot")
st.markdown("Welcome to the AI-powered smart school assistant! Choose an option below to get started.")

# Sidebar for navigation
st.sidebar.header("Navigation")
option = st.sidebar.radio("Choose an option:", 
                          ["Home", "Get a Lesson (Teachers)", "Get a Lesson (Students)", 
                           "Student Report for Parents", "Track Student Progress"])

# Home Page
if option == "Home":
    st.write("### Welcome to EduBuddy AI!")
    st.write("This chatbot is designed to help teachers, students, and parents with:")
    st.write("- **AI-Powered Lesson Plans** for teachers and students.")
    st.write("- **Student Performance Reports** for parents.")
    st.write("- **Real-Time Student Progress Tracking**.")
    st.write("- **Interactive and Intelligent Assistance** for all users.")

# Get a Lesson (Teachers)
elif option == "Get a Lesson (Teachers)":
    st.write("### Get a Lesson Plan for Teachers")
    subject = st.text_input("Enter subject (math, science, english, history):")
    grade_level = st.selectbox("Select grade level:", ["Primary", "Elementary School", "High School"])
    if st.button("Generate Lesson"):
        if subject:
            lesson = ai_assistant.get_lesson(subject, grade_level)
            st.write("### Here's your lesson plan:")
            st.write(lesson)
        else:
            st.error("Please enter a subject.")

# Get a Lesson (Students)
elif option == "Get a Lesson (Students)":
    st.write("### Get a Lesson for Students")
    subject = st.text_input("Enter subject (math, science, english, history):")
    if st.button("Generate Lesson"):
        if subject:
            lesson = ai_assistant.get_lesson(subject)
            st.write("### Here's your lesson:")
            st.write(lesson)
        else:
            st.error("Please enter a subject.")

# Student Report for Parents
elif option == "Student Report for Parents":
    st.write("### Get a Student Report for Parents")
    student_name = st.text_input("Enter student name:")
    language = st.selectbox("Choose language:", ["english", "urdu"])
    if st.button("Generate Report"):
        if student_name:
            report = ai_assistant.get_parent_report(student_name, language)
            st.write("### Here's the student report:")
            st.write(report)
        else:
            st.error("Please enter a student name.")

# Track Student Progress
elif option == "Track Student Progress":
    st.write("### Track Student Progress")
    student_name = st.text_input("Enter student name:")
    subject = st.text_input("Enter subject:")
    score = st.number_input("Enter score (0-100):", min_value=0, max_value=100)
    
    if st.button("Submit"):
        if student_name and subject:
            # Store student progress in session state
            if student_name not in st.session_state.student_data:
                st.session_state.student_data[student_name] = {}
            st.session_state.student_data[student_name][subject] = score
            st.success("Progress updated!")
        else:
            st.error("Please enter both student name and subject.")
    
    if st.button("View Progress"):
        if student_name:
            if student_name in st.session_state.student_data:
                st.write("### Student Progress:")
                # Display the data in a table
                progress_data = st.session_state.student_data[student_name]
                st.write(pd.DataFrame(list(progress_data.items()), columns=["Subject", "Score"]))
                
                # Display the data in a bar chart
                st.write("### Progress Chart")
                progress_df = pd.DataFrame(list(progress_data.items()), columns=["Subject", "Score"])
                st.bar_chart(progress_df.set_index("Subject"))
            else:
                st.write("No data available for this student.")
        else:
            st.error("Please enter a student name.")

# Footer
st.sidebar.markdown("---")
st.sidebar.markdown("Built with ❤️ by Shahzad Ahmad")