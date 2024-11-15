import tkinter as tk
from tkinter import messagebox
from file_handler import find_or_create_user, load_users, save_users
import json
import time
import random

class EnhancedQuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Enhanced Quiz App")
        self.root.geometry("800x600")
        self.root.resizable(False, False)

        self.user = None
        self.current_question_index = 0
        self.answers = []
        self.timer_running = False
        self.timer_id = None
        self.total_duration = 10 * 60  # 10 dakika
        self.start_time = None
        self.end_time = None

        # Sorular JSON dosyasından yüklenir
        with open("questions.json", "r", encoding="utf-8") as file:
            self.sections = json.load(file)["sections"]

        self.user_entry_screen()

    def user_entry_screen(self):
        self.clear_window()
        frame = tk.Frame(self.root)
        frame.pack(fill="both", expand=True)
        tk.Label(frame, text="User Login", font=("Arial", 24)).pack(pady=20)
        tk.Label(frame, text="Name:", font=("Arial", 14)).pack(pady=5)
        self.name_entry = tk.Entry(frame, font=("Arial", 14))
        self.name_entry.pack(pady=5, padx=20, ipadx=10)
        tk.Label(frame, text="Email:", font=("Arial", 14)).pack(pady=5)
        self.email_entry = tk.Entry(frame, font=("Arial", 14))
        self.email_entry.pack(pady=5, padx=20, ipadx=10)
        tk.Button(frame, text="Login", font=("Arial", 14), command=self.check_user).pack(pady=20)

    def check_user(self):
        name = self.name_entry.get()
        email = self.email_entry.get()
        if not name or not email:
            messagebox.showerror("Error", "Please fill in all fields!")
            return
        self.user = find_or_create_user(email, name)

        # Kullanıcı sınav hakkı kontrolü
        if len(self.user.get("history", [])) >= 2:
            messagebox.showerror("Error", "You have exceeded the maximum number of attempts!")
            self.view_previous_results()
            return

        messagebox.showinfo("Welcome", f"Welcome, {self.user['name']}!")
        self.main_menu()

    def main_menu(self):
        self.clear_window()
        tk.Label(self.root, text=f"Welcome, {self.user['name']}!", font=("Arial", 16)).pack(pady=10)
        tk.Button(
            self.root,
            text="Start Exam",
            font=("Arial", 14),
            command=self.start_exam
        ).pack(pady=20)
        tk.Button(
            self.root,
            text="View Previous Results",
            font=("Arial", 14),
            command=self.view_previous_results
        ).pack(pady=20)
        tk.Button(self.root, text="Logout", font=("Arial", 14), command=self.user_entry_screen).pack(pady=10)

    def start_exam(self):
        """Karışık sorularla sınav başlat."""
        self.clear_window()
        self.answers = []

        # Tüm bölümlerden soruları karışık şekilde hazırlıyoruz
        all_questions = []
        for section in self.sections:
            for question in section["questions"]:
                question["section_name"] = section["section_name"]
                all_questions.append(question)
        random.shuffle(all_questions)
        self.mixed_questions = all_questions
        self.current_question_index = 0

        self.start_timer()
        self.show_question()

    def show_question(self):
        """Sıradaki soruyu göster."""
        self.clear_window()
        question = self.mixed_questions[self.current_question_index]
        tk.Label(self.root, text=f"Q: {question['question_text']}", font=("Arial", 14), wraplength=600).pack(pady=20)

        for idx, option in enumerate(question["options"], start=1):
            tk.Button(
                self.root,
                text=option,
                font=("Arial", 12),
                command=lambda opt=idx: self.record_answer(opt)
            ).pack(pady=5)

    def record_answer(self, selected_option):
        """Kullanıcının yanıtını kaydeder."""
        question = self.mixed_questions[self.current_question_index]
        self.answers.append({
            "question": question["question_text"],
            "selected": selected_option,
            "correct": question["correct_answer"],
            "section_name": question["section_name"],
            "options": question["options"]
        })
        self.current_question_index += 1
        if self.current_question_index < len(self.mixed_questions):
            self.show_question()
        else:
            self.review_answers()

    def review_answers(self):
        """Yanıtları gözden geçirme ekranı."""
        self.clear_window()
        tk.Label(self.root, text="Review Your Answers", font=("Arial", 16)).pack(pady=10)

        canvas = tk.Canvas(self.root)
        scrollbar = tk.Scrollbar(self.root, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        for idx, answer in enumerate(self.answers):
            frame = tk.Frame(scrollable_frame, bd=1, relief="solid", padx=10, pady=10)
            frame.pack(fill="x", pady=5)

            # Soruyu sola yaslı ve küçük font ile göster
            tk.Label(frame, text=f"Q{idx + 1}: {answer['question']}", font=("Arial", 10), anchor="w", wraplength=700).grid(row=0, column=0, sticky="w", columnspan=2)

            # Yanıt seçeneklerini yan yana göster
            for opt_idx, option in enumerate(answer["options"], start=1):
                color = "green" if opt_idx == answer["selected"] else "black"
                tk.Button(
                    frame,
                    text=option,
                    fg=color,
                    font=("Arial", 10),
                    command=lambda q_idx=idx, o_idx=opt_idx: self.change_answer(q_idx, o_idx)
                ).grid(row=1, column=opt_idx - 1, padx=10, sticky="w")

        tk.Button(self.root, text="Submit Exam", font=("Arial", 14), command=self.finalize_exam).pack(pady=20)


    def change_answer(self, question_idx, option_idx):
        """Yanıtı değiştirme."""
        self.answers[question_idx]["selected"] = option_idx
        self.review_answers()

    def finalize_exam(self):
        """Sınavı sonlandırır ve sonuçları gösterir."""
        self.clear_window()

        # Sonuç hesaplama
        section_results = {section["section_name"]: {"total": 0, "correct": 0} for section in self.sections}
        for answer in self.answers:
            section_name = answer["section_name"]
            section_results[section_name]["total"] += 1
            if answer["selected"] == answer["correct"]:
                section_results[section_name]["correct"] += 1

        total_correct = sum(result["correct"] for result in section_results.values())
        total_questions = sum(result["total"] for result in section_results.values())
        overall_percentage = (total_correct / total_questions) * 100

        # Sonuçları göster
        tk.Label(self.root, text="Exam Results", font=("Arial", 16)).pack(pady=10)
        for section, result in section_results.items():
            result_text = f"{section}: {result['correct']} / {result['total']}"
            tk.Label(self.root, text=result_text, font=("Arial", 12)).pack()
        result_text = f"Overall: {total_correct} / {total_questions} ({overall_percentage:.2f}%)"
        tk.Label(self.root, text=result_text, font=("Arial", 14)).pack(pady=10)

        if overall_percentage >= 75:
            tk.Label(self.root, text="You Passed! 🎉", font=("Arial", 16), fg="green").pack(pady=5)
        else:
            tk.Label(self.root, text="You Did Not Pass. 😔", font=("Arial", 16), fg="red").pack(pady=5)

        # Sonuçları kaydet
        self.user["history"].append({
            "date": time.strftime("%Y-%m-%d %H:%M:%S"),
            "results": section_results,
            "overall_percentage": overall_percentage
        })
        users = load_users()
        for user in users:
            if user["email"] == self.user["email"]:
                user["history"] = self.user["history"]
                break
        save_users(users)

        tk.Button(self.root, text="Main Menu", font=("Arial", 14), command=self.main_menu).pack(pady=20)

    def view_previous_results(self):
        """Önceki sonuçları görüntüleme."""
        self.clear_window()
        tk.Label(self.root, text="Previous Results", font=("Arial", 16)).pack(pady=10)
        if not self.user["history"]:
            tk.Label(self.root, text="No previous results available.", font=("Arial", 14)).pack(pady=20)
            tk.Button(self.root, text="Main Menu", font=("Arial", 14), command=self.main_menu).pack(pady=10)
            return

        for attempt in self.user["history"]:
            tk.Label(self.root, text=f"Date: {attempt['date']}", font=("Arial", 12)).pack(pady=5)
            for section, result in attempt["results"].items():
                result_text = f"{section}: {result['correct']} / {result['total']}"
                tk.Label(self.root, text=result_text, font=("Arial", 12)).pack()
            tk.Label(self.root, text=f"Overall: {attempt['overall_percentage']:.2f}%", font=("Arial", 12)).pack(pady=5)

        tk.Button(self.root, text="Main Menu", font=("Arial", 14), command=self.main_menu).pack(pady=20)

    def start_timer(self):
        """Zamanlayıcı başlat."""
        self.start_time = time.time()
        self.end_time = self.start_time + self.total_duration
        self.timer_running = True
        self.update_timer()

    def update_timer(self):
        """Zamanlayıcıyı güncelle."""
        if not self.timer_running:
            return
        remaining_time = self.end_time - time.time()
        if remaining_time <= 0:
            self.timer_running = False
            self.finalize_exam()
        else:
            minutes, seconds = divmod(int(remaining_time), 60)
            self.timer_label = tk.Label(self.root, text=f"Time Remaining: {minutes:02}:{seconds:02}", font=("Arial", 14), fg="red")
            self.timer_label.pack()
            self.timer_id = self.root.after(1000, self.update_timer)

    def clear_window(self):
        """Ekranı temizle ve zamanlayıcıyı durdur."""
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = EnhancedQuizApp(root)
    root.mainloop()
