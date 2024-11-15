import tkinter as tk
from tkinter import messagebox
import json
import os

# JSON dosyalarını yükleme
users_file = 'users.json'
questions_file = 'questions.json'

# Kullanıcılar ve soruların yüklenmesi
if os.path.exists(users_file):
    with open(users_file, 'r', encoding='utf-8') as file:
        users = json.load(file)
else:
    users = []

with open(questions_file, 'r', encoding='utf-8') as file:
    data = json.load(file)

sections = {section['section_id']: section for section in data['sections']}

class QuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gelişmiş Quiz Uygulaması")
        self.user = None
        self.current_section = None
        self.current_question_index = 0
        self.answers = []
        self.score = 0

        # Kullanıcı bilgilerini alma
        self.user_entry_screen()

    def user_entry_screen(self):
        self.clear_window()
        tk.Label(self.root, text="Kullanıcı Girişi", font=("Arial", 16)).pack(pady=10)
        tk.Label(self.root, text="Adınız:", font=("Arial", 12)).pack()
        self.name_entry = tk.Entry(self.root)
        self.name_entry.pack(pady=5)

        tk.Label(self.root, text="E-posta:", font=("Arial", 12)).pack()
        self.email_entry = tk.Entry(self.root)
        self.email_entry.pack(pady=5)

        tk.Button(self.root, text="Giriş Yap", command=self.check_user).pack(pady=10)

    def check_user(self):
        name = self.name_entry.get()
        email = self.email_entry.get()

        if not name or not email:
            messagebox.showerror("Hata", "Lütfen tüm alanları doldurun!")
            return

        # Kullanıcı geçmişini kontrol et
        user = next((u for u in users if u['email'] == email), None)
        if user:
            self.user = user
            messagebox.showinfo("Hoş Geldiniz", f"Tekrar hoş geldiniz, {user['name']}!")
        else:
            self.user = {'name': name, 'email': email, 'history': []}
            users.append(self.user)
            messagebox.showinfo("Yeni Kullanıcı", "Yeni kullanıcı olarak kayıt oluşturdunuz.")
        self.main_menu()

    def main_menu(self):
        self.clear_window()
        tk.Label(self.root, text=f"Hoş Geldiniz, {self.user['name']}!", font=("Arial", 16)).pack(pady=10)
        tk.Label(self.root, text="Bir bölüm seçin:", font=("Arial", 12)).pack(pady=5)

        for section_id, section in sections.items():
            tk.Button(
                self.root, text=section['section_name'],
                command=lambda sid=section_id: self.start_quiz(sid)
            ).pack(pady=5)

        tk.Button(self.root, text="Çıkış Yap", command=self.user_entry_screen).pack(pady=10)

    def start_quiz(self, section_id):
        self.current_section = sections[section_id]
        self.current_question_index = 0
        self.answers = []
        self.score = 0
        self.show_question()

    def show_question(self):
        self.clear_window()
        question = self.current_section['questions'][self.current_question_index]
        tk.Label(self.root, text=f"Soru {self.current_question_index + 1}: {question['question_text']}",
                 font=("Arial", 12), wraplength=400).pack(pady=10)

        for idx, option in enumerate(question['options'], start=1):
            tk.Button(
                self.root, text=option,
                command=lambda i=idx: self.check_answer(i)
            ).pack(pady=5)

    def check_answer(self, selected_option):
        question = self.current_section['questions'][self.current_question_index]
        correct = selected_option == question['correct_answer']
        self.answers.append({
            'question': question['question_text'],
            'selected': question['options'][selected_option - 1],
            'correct': question['options'][question['correct_answer'] - 1],
            'is_correct': correct
        })
        if correct:
            self.score += 1

        self.current_question_index += 1
        if self.current_question_index < len(self.current_section['questions']):
            self.show_question()
        else:
            self.show_results()

    def show_results(self):
        self.clear_window()
        tk.Label(self.root, text="Quiz Tamamlandı!", font=("Arial", 16)).pack(pady=10)
        tk.Label(self.root, text=f"Skorunuz: {self.score}/{len(self.current_section['questions'])}", font=("Arial", 14)).pack(pady=10)

        for answer in self.answers:
            result_text = f"Soru: {answer['question']}\nSeçilen: {answer['selected']} (Doğru: {answer['correct']})"
            color = "green" if answer['is_correct'] else "red"
            tk.Label(self.root, text=result_text, fg=color, font=("Arial", 10), wraplength=400).pack(pady=5)

        self.user['history'].append({
            'section': self.current_section['section_name'],
            'score': self.score,
            'total': len(self.current_section['questions'])
        })

        with open(users_file, 'w', encoding='utf-8') as file:
            json.dump(users, file, indent=4)

        tk.Button(self.root, text="Ana Menüye Dön", command=self.main_menu).pack(pady=10)

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = QuizApp(root)
    root.mainloop()
