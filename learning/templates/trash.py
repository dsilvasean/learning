import pyquiz
import random

def generate_mcq_questions(topic):
    """Generate 5 MCQs based on the user topic using pyquiz."""
    questions = pyquiz.generate_questions(topic, num_questions=5, question_type="mcq")
    return questions

def conduct_quiz(questions):
    """Conducts the quiz and returns the score."""
    score = 0
    for i, question in enumerate(questions, 1):
        print(f"\nQuestion {i}: {question['question']}")
        for idx, option in enumerate(question['options'], 1):
            print(f"{idx}. {option}")
        
        user_answer = input("Enter the number of your answer: ")
        if question['answer'] == question['options'][int(user_answer) - 1]:
            print("Correct!")
            score += 1
        else:
            print(f"Wrong! The correct answer was: {question['answer']}")
    
    return score

def main():
    topic = input("Enter a topic for the quiz: ")
    questions = generate_mcq_questions(topic)
    score = conduct_quiz(questions)
    print(f"\nYour final score: {score}/5")

if __name__ == "_main_":
    main()