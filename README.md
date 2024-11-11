## QUIZ APP ##
Software Requirements Specification
Project Name
Multi-Part Time-Limited Quiz Application


Objective
To develop a quiz application that allows users to take a four-part exam within a specific time limit. Each section will contain different types of questions, and users must achieve at least 75% success in each section.

General Requirements
Programming Language: Python

Data Storage: JSON files

Interface: Console-based or a simple graphical user interface

Security: Optioal data encryption

Functional Requirements
User Actions
User Information Entry: Before starting the exam, the user will enter their name, surname, and other required information.

Exam Attempts: The user can take the exam at max 2 times.

Result Display: The result will be displayed automatically at the end of the exam or when the time is up. This will include pass/fail information and success rates for each section.

Exam Structure
Sections: Total of 4 sections

Questions: At least 5 questions in each section, and questions will be selected randomly each time.

Question Types:

True-False

Single-choice multiple choice

Multiple choice (multiple correct answers)

Each question will have a specific point value.

Time: The exam duration will be limited; the exam will end automatically when the time is up.

Success Criteria
Section Success: At least 75% success must be achieved in each section.

Overall Passing Grade: 75 points and above will be considered as a passing grade.

Technical Requirements
Files and Data Structure
Questions Folder: Will contain separate JSON files for each section:

questions_section1.json

questions_section2.json

questions_section3.json

questions_section4.json

Answers Folder: Correct answers will be stored in separate JSON files:

answers.json

Users Folder: User information and exam entry counts will be kept here:

users.json

Data Encryption (Optional)
All information in JSON files can be encrypted.

A suitable algorithm (e.g., AES) can be used for encryption.

Application Flow
User Login: The user enters their information and starts the exam.

Exam Start: The timer starts.

Question Display: Questions are displayed sequentially according to the sections.

Answering: The user answers the questions.

For single-choice questions, one option is selected.

For multiple-choice questions, multiple options can be selected.

For True-False questions, true or false is selected.

Time Tracking: If the time is up, the exam is automatically terminated.

Result Calculation:

The correct answer percentage is calculated for each section.

The overall score is calculated.

Result Display: Detailed results are shown to the user.

Exam Attempt Update: The user’s exam attempt count is updated.

Error and Status Management
Exam Attempt Limit Exceeded: If the user has exceeded the exam attempts, a warning is given, and the user is not allowed to take the exam.

Time Out: When the time is up, the evaluation is done based on the existing answers.

Invalid Entries: If an unexpected input is received from the user, a warning message is displayed, and the user is asked to enter again.

Testing and Verification
Unit Tests: Unit tests will be written for each function.

Integration Tests: It will be tested that the system components work together correctly.

User Acceptance Tests: User acceptance tests will be performed for different scenarios.

GOOD LUCK!
