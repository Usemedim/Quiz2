from file_handler import load_questions, get_user_data, update_user_data
from time_manager import start_timer, check_time_remaining

def get_user_input(prompt, valid_options=None):
    while True:
        user_input = input(prompt).strip()
        if valid_options and user_input not in valid_options:
            print("Invalid input. Please enter a valid option.")
        else:
            return user_input

def show_question(section_id, question_id, question_text, options=None):
    print(f"Question {question_id}: {question_text}")
    if options:
        print("Options:")
        for idx, option in enumerate(options, 1):
            print(f"{idx}. {option}")
    valid_answer = False
    user_answer = None
    while not valid_answer:
        user_answer = input("Enter your answer: ").strip()
        if user_answer.isdigit():
            user_answer = int(user_answer)
            if 1 <= user_answer <= len(options):
                valid_answer = True
            else:
                print(f"Please enter a number between 1 and {len(options)}.")
        else:
            print("Invalid answer, please enter a number.")
    return user_answer

def evaluate_answers(user_answers, correct_answers):
    score = 0
    total_questions = len(correct_answers)
    for question_id, correct_answer in correct_answers.items():
        user_answer = user_answers.get(question_id)
        if user_answer is None:
            print(f"No valid answer provided for question {question_id}.")
            continue
        if user_answer == correct_answer:
            score += 1
    return (score / total_questions) * 100

def start_exam(username, exam_duration=3600):
    user_data = get_user_data(username)
    if user_data['attempts'] >= 2:
        print(f"{username}, you have no more attempts!")
        return
    print(f"Starting your exam, {username}!")
    user_answers = {}
    total_score = 0
    sections = [1, 2, 3, 4]
    start_time, end_time = start_timer(exam_duration)
    all_questions = load_questions()
    
    for section in sections:
        print(f"\nSection {section} - Starting...")
        section_questions = all_questions.get(section, [])
        correct_answers = {q["question_id"]: q["correct_answer"] for q in section_questions} 
        section_user_answers = {}
        for question_data in section_questions:
            question_id = question_data["question_id"]
            question_text = question_data["question_text"]
            valid_options = question_data.get("options", None)
            user_answer = show_question(section, question_id, question_text, valid_options)
            section_user_answers[question_id] = user_answer
        section_score = evaluate_answers(section_user_answers, correct_answers)
        print(f"Section {section} success rate: {section_score:.2f}%")
        total_score += section_score
    overall_score = total_score / len(sections)
    print(f"\nYour overall success rate: {overall_score:.2f}%")
    user_data['attempts'] += 1
    update_user_data(username, user_data['attempts'], overall_score)
    if overall_score >= 75:
        print(f"Congratulations, {username}! You passed the exam.")
    else:
        print(f"Unfortunately, {username}, you did not pass the exam. Try again.")

if __name__ == "__main__":
    print("Welcome!")
    username = input("Enter your username: ").strip()
    
    start_exam(username)
