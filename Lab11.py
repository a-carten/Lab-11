import os
import matplotlib.pyplot as plt
import math

# --- Load students into dictionary: id -> name ---
def load_students(filepath):
    students = {}
    with open(filepath, 'r') as file:
        for line in file:
            line = line.strip()
            student_id = line[:3]
            student_name = line[3:]
            students[student_id] = student_name
    return students

# --- Load assignments into dictionary: id -> (name, points) ---
def load_assignments(filepath):
    assignments = {}
    with open(filepath, 'r') as file:
        lines = file.read().splitlines()
        for i in range(0, len(lines), 3):
            name = lines[i].strip()
            assign_id = lines[i+1].strip()
            points = int(lines[i+2].strip())
            assignments[assign_id] = (name, points)
    return assignments

# --- Load submissions into a list of (student_id, assign_id, percent) ---
def load_submissions(folder_path):
    submissions = []
    for filename in os.listdir(folder_path):
        path = os.path.join(folder_path, filename)
        with open(path, 'r') as file:
            for line in file:
                parts = line.strip().split('|')
                if len(parts) == 3:
                    submissions.append((parts[0], parts[1], float(parts[2])))
    return submissions

# --- Option 1: Calculate total course grade for a student ---
def calculate_student_grade(name, students, assignments, submissions):
    # Find student_id from name
    student_id = None
    for sid, sname in students.items():
        if sname == name:
            student_id = sid
            break

    if not student_id:
        print("Student not found")
        return

    total_earned = 0
    for sid, aid, percent in submissions:
        if sid == student_id and aid in assignments:
            _, points = assignments[aid]
            total_earned += (percent / 100) * points

    grade = round((total_earned / 1000) * 100)
    print(f"{grade}%")

# --- Option 2: Assignment statistics (min, avg, max) ---
def assignment_statistics(name, assignments, submissions):
    assignment_id = None
    for aid, (aname, _) in assignments.items():
        if aname == name:
            assignment_id = aid
            break

    if not assignment_id:
        print("Assignment not found")
        return

    scores = [percent for _, aid, percent in submissions if aid == assignment_id]
    if scores:
        print(f"Min: {math.floor(min(scores))}%")
        print(f"Avg: {math.floor(sum(scores)/len(scores))}%")
        print(f"Max: {math.floor(max(scores))}%")
    else:
        print("No submissions found for that assignment")

# --- Option 3: Display histogram of assignment scores ---
def assignment_graph(name, assignments, submissions):
    assignment_id = None
    for aid, (aname, _) in assignments.items():
        if aname == name:
            assignment_id = aid
            break

    if not assignment_id:
        print("Assignment not found")
        return

    scores = [percent for _, aid, percent in submissions if aid == assignment_id]
    if scores:
        plt.hist(scores, bins=[0, 25, 50, 75, 100])
        plt.title(f"Scores for {name}")
        plt.xlabel("Score (%)")
        plt.ylabel("Number of Students")
        plt.show()
    else:
        print("No submissions found for that assignment")

# --- Main menu ---
def main():
    students = load_students('data/students.txt')
    assignments = load_assignments('data/assignments.txt')
    submissions = load_submissions('data/submissions')

    print("1. Student grade")
    print("2. Assignment statistics")
    print("3. Assignment graph\n")
    selection = input("Enter your selection: ")

    if selection == '1':
        name = input("What is the student's name: ")
        calculate_student_grade(name, students, assignments, submissions)
    elif selection == '2':
        name = input("What is the assignment name: ")
        assignment_statistics(name, assignments, submissions)
    elif selection == '3':
        name = input("What is the assignment name: ")
        assignment_graph(name, assignments, submissions)

if __name__ == '__main__':
    main()
