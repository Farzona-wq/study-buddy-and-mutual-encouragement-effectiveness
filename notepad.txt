import tkinter as tk
from tkinter import messagebox, filedialog
import re
from datetime import datetime
import json
import csv

# ----------------- Validation functions -----------------
def validate_name(name):
    pattern = r"^[A-Za-z\s\-']+$"
    return bool(re.match(pattern, name))

def validate_dob(dob):
    try:
        datetime.strptime(dob, "%d/%m/%Y")
        return True
    except ValueError:
        return False

def validate_student_id(student_id):
    return student_id.isdigit()

# ----------------- Questionnaire Data -----------------
questions = [
    {"text": "1) Study sessions are more productive when working with a buddy.",
     "options": [("Never",0), ("Rarely",1), ("Sometimes",2), ("Often",3), ("Always",4)]},
    {"text": "2) Studying with a buddy helps maintain focus during study sessions.",
     "options": [("Never",0), ("Rarely",1), ("Sometimes",2), ("Often",3), ("Always",4)]},
    {"text": "3) Tasks are completed more efficiently when studying with a buddy.",
     "options": [("Strongly disagree",0), ("Disagree",1), ("Neutral",2), ("Agree",3), ("Strongly agree",4)]},
    {"text": "4) I achieve better academic results when studying with a buddy.",
     "options": [("Never",0), ("Rarely",1), ("Sometimes",2), ("Often",3), ("Always",4)]},
    {"text": "5) Positive feedback from a study buddy improves confidence.",
     "options": [("Strongly disagree",0), ("Disagree",1), ("Neutral",2), ("Agree",3), ("Strongly agree",4)]},
    {"text": "6) Collaborative studying helps identify gaps in my knowledge more effectively than studying alone.",
     "options": [("Never",0), ("Rarely",1), ("Sometimes",2), ("Often",3), ("Always",4)]},
    {"text": "7) Receiving encouragement from a study buddy enhances persistence when facing difficult tasks.",
     "options": [("Never",0), ("Rarely",1), ("Sometimes",2), ("Often",3), ("Always",4)]},
    {"text": "8) Studying with a buddy facilitates deeper understanding through explanation and discussion of concepts.",
     "options": [("Strongly disagree",0), ("Disagree",1), ("Neutral",2), ("Agree",3), ("Strongly agree",4)]},
    {"text": "9) Studying with a buddy increases my awareness of my own learning strategies.",
     "options": [("Strongly disagree",0), ("Disagree",1), ("Neutral",2), ("Agree",3), ("Strongly agree",4)]},
    {"text": "10) The presence of a study buddy increases my sense of accountability for academic responsibilities.",
     "options": [("Not at all",0), ("Slightly",1), ("Moderately",2), ("Significantly",3), ("Extremely",4)]},
    {"text": "11) Studying with a buddy reduces tendencies toward procrastination through shared responsibility.",
     "options": [("Strongly disagree",0), ("Disagree",1), ("Neutral",2), ("Agree",3), ("Strongly agree",4)]},
    {"text": "12) Interaction with a study buddy encourages me to reflect on how I learn.",
     "options": [("Not at all",0), ("Slightly",1), ("Moderately",2), ("Significantly",3), ("Extremely",4)]},
    {"text": "13) Mutual encouragement contributes significantly to my academic success.",
     "options": [("Never",0), ("Rarely",1), ("Sometimes",2), ("Often",3), ("Always",4)]},
    {"text": "14) Exposure to alternative viewpoints from a study buddy strengthens my understanding.",
     "options": [("Not at all",0), ("Slightly",1), ("Moderately",2), ("Significantly",3), ("Extremely",4)]},
    {"text": "15) Study buddy systems should be encouraged in academic settings.",
     "options": [("Strongly disagree",0), ("Disagree",1), ("Neutral",2), ("Agree",3), ("Strongly agree",4)]}
]

# ----------------- Psychological States -----------------
def get_psychological_state(score):
    if score <= 25:
        return "Highly stressed; may need psychological help."
    elif score <= 35:
        return "Moderately stressed; occasional support recommended."
    elif score <= 50:
        return "Stable psychological state; no help required."
    elif score <= 60:
        return "Positive state; good coping mechanisms."
    else:
        return "Very positive and resilient state."

# ----------------- Main Tkinter Window -----------------
root = tk.Tk()
root.title("Questionnaire System")
root.geometry("500x400")

# Frames
main_menu_frame = tk.Frame(root)
student_frame = tk.Frame(root)
question_frame = tk.Frame(root)

# ----------------- Main Menu Frame -----------------
def start_new():
    main_menu_frame.pack_forget()
    student_frame.pack()

def load_existing():
    filetypes = [("Text files", "*.txt"), ("CSV files", "*.csv"), ("JSON files", "*.json")]
    file_path = filedialog.askopenfilename(title="Open Saved Questionnaire", filetypes=filetypes)
    if not file_path:
        return  # Cancelled

    content_text = ""
    try:
        if file_path.endswith(".txt"):
            with open(file_path, "r", encoding="utf-8") as f:
                content_text = f.read()
        elif file_path.endswith(".csv"):
            with open(file_path, "r", encoding="utf-8") as f:
                reader = csv.reader(f)
                for row in reader:
                    content_text += "\t".join(row) + "\n"
        elif file_path.endswith(".json"):
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                content_text += f"Student Name: {data['name']}\n"
                content_text += f"Date of Birth: {data['date_of_birth']}\n"
                content_text += f"Student ID: {data['student_id']}\n\n"
                for ans in data['answers']:
                    content_text += f"{ans['question']}\nAnswer: {ans['selected_answer']} (Score: {ans['score']})\n\n"
                content_text += f"Total Score: {data['total_score']}\n"
                content_text += f"Psychological State: {data['psychological_state']}\n"
        else:
            messagebox.showerror("Error", "Unsupported file format.")
            return
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load file:\n{e}")
        return

    # Show results in a new window
    result_window = tk.Toplevel(root)
    result_window.title("Loaded Questionnaire Results")
    result_window.geometry("500x500")
    tk.Label(result_window, text="Loaded Questionnaire Results", font=("Arial", 14)).pack(pady=10)
    text_widget = tk.Text(result_window, wrap="word")
    text_widget.pack(expand=True, fill="both", padx=10, pady=10)
    text_widget.insert("1.0", content_text)
    text_widget.config(state="disabled")

tk.Label(main_menu_frame, text="Welcome! Choose an option:", font=("Arial", 14)).pack(pady=20)
tk.Button(main_menu_frame, text="Load Existing Questionnaire", width=30, command=load_existing).pack(pady=5)
tk.Button(main_menu_frame, text="Start New Questionnaire", width=30, command=start_new).pack(pady=5)
main_menu_frame.pack()

# ----------------- Student Input Frame -----------------
tk.Label(student_frame, text="Enter your details", font=("Arial", 14)).pack(pady=10)
tk.Label(student_frame, text="Full Name:").pack()
name_entry = tk.Entry(student_frame, width=40)
name_entry.pack()
tk.Label(student_frame, text="Date of Birth (DD/MM/YYYY):").pack()
dob_entry = tk.Entry(student_frame, width=40)
dob_entry.pack()
tk.Label(student_frame, text="Student ID:").pack()
id_entry = tk.Entry(student_frame, width=40)
id_entry.pack()

# ----------------- Questionnaire Variables -----------------
question_label = tk.Label(question_frame, text="", wraplength=450, font=("Arial", 12))
question_label.pack(pady=20)
answer_buttons = []
current_question_index = 0
total_score = 0
user_answers = []

student_name = ""
student_dob = ""
student_id_num = ""

# ----------------- Functions -----------------
def start_questionnaire(name, dob, student_id):
    global current_question_index, total_score, user_answers
    current_question_index = 0
    total_score = 0
    user_answers = []
    question_frame.pack()
    show_question(0)

def submit_student_info():
    name = name_entry.get().strip()
    dob = dob_entry.get().strip()
    student_id = id_entry.get().strip()
    if not validate_name(name):
        messagebox.showerror("Error", "Invalid name. Only letters, hyphens (-), apostrophes ('), and spaces allowed.")
        return
    if not validate_dob(dob):
        messagebox.showerror("Error", "Invalid date of birth. Use DD/MM/YYYY format.")
        return
    if not validate_student_id(student_id):
        messagebox.showerror("Error", "Invalid Student ID. Only digits are allowed.")
        return
    student_frame.pack_forget()
    start_questionnaire(name, dob, student_id)

tk.Button(student_frame, text="Submit", width=20, command=submit_student_info).pack(pady=15)

def show_question(index):
    question = questions[index]
    question_label.config(text=question["text"])
    for btn in answer_buttons:
        btn.destroy()
    answer_buttons.clear()
    for opt_text, opt_score in question["options"]:
        btn = tk.Button(question_frame, text=opt_text, width=25, command=lambda s=opt_score: answer_selected(s))
        btn.pack(pady=3)
        answer_buttons.append(btn)

def answer_selected(score):
    global total_score, current_question_index
    user_answers.append((current_question_index, score))
    total_score += score
    current_question_index += 1
    if current_question_index < len(questions):
        show_question(current_question_index)
    else:
        show_result()

def show_result():
    question_label.config(text="")
    for btn in answer_buttons:
        btn.destroy()
    answer_buttons.clear()
    global student_name, student_dob, student_id_num
    student_name = name_entry.get().strip()
    student_dob = dob_entry.get().strip()
    student_id_num = id_entry.get().strip()
    state = get_psychological_state(total_score)
    result_text = f"Your total score is {total_score}.\n\nPsychological state:\n{state}"
    result_label = tk.Label(question_frame, text=result_text, font=("Arial", 12), fg="blue")
    result_label.pack(pady=20)
    tk.Button(question_frame, text="Save Results", width=20, command=save_results).pack(pady=5)
    tk.Button(question_frame, text="Exit", width=20, command=root.destroy).pack(pady=5)

def save_results():
    filetypes = [("Text file", "*.txt"), ("CSV file", "*.csv"), ("JSON file", "*.json")]
    file_path = filedialog.asksaveasfilename(title="Save Results", defaultextension=".txt", filetypes=filetypes)
    if not file_path:
        return
    data = {
        "name": student_name,
        "date_of_birth": student_dob,
        "student_id": student_id_num,
        "answers": [],
        "total_score": total_score,
        "psychological_state": get_psychological_state(total_score)
    }
    for q_index, score in user_answers:
        q_text = questions[q_index]["text"]
        option_text = next(opt[0] for opt in questions[q_index]["options"] if opt[1] == score)
        data["answers"].append({"question": q_text, "selected_answer": option_text, "score": score})
    try:
        if file_path.endswith(".txt"):
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(f"Student Name: {data['name']}\n")
                f.write(f"Date of Birth: {data['date_of_birth']}\n")
                f.write(f"Student ID: {data['student_id']}\n\n")
                for ans in data["answers"]:
                    f.write(f"{ans['question']}\nAnswer: {ans['selected_answer']} (Score: {ans['score']})\n\n")
                f.write(f"Total Score: {data['total_score']}\n")
                f.write(f"Psychological State: {data['psychological_state']}\n")
        elif file_path.endswith(".csv"):
            with open(file_path, "w", newline='', encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["Student Name", data['name']])
                writer.writerow(["Date of Birth", data['date_of_birth']])
                writer.writerow(["Student ID", data['student_id']])
                writer.writerow([])
                writer.writerow(["Question", "Selected Answer", "Score"])
                for ans in data["answers"]:
                    writer.writerow([ans['question'], ans['selected_answer'], ans['score']])
                writer.writerow([])
                writer.writerow(["Total Score", data['total_score']])
                writer.writerow(["Psychological State", data['psychological_state']])
        elif file_path.endswith(".json"):
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
        else:
            messagebox.showerror("Error", "Unsupported file format.")
            return
        messagebox.showinfo("Success", f"Results saved successfully to:\n{file_path}")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save file:\n{e}")

root.mainloop()