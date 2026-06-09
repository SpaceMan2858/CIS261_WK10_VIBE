# Frank McCladdie
# CIS261
# WK10 VIBE Coding - Student Grade Calculator

import os

# File name for storing student records
DATA_FILE = "student_grades.txt"


def calculate_average(test1, test2, test3):
    """Calculate the average of three test scores."""
    return round((test1 + test2 + test3) / 3, 2)

def calculate_grade(average):
    """Calculate the letter grade based on the average score."""
    if average >= 90:
        return 'A'
    elif average >= 80:
        return 'B'
    elif average >= 70:
        return 'C'
    elif average >= 60:
        return 'D'
    else:
        return 'F'


def load_students():
    """Loads student records from the text file into a list of dictionaries."""
    students = []
    if not os.path.exists(DATA_FILE):
        return students
        
    try:
        with open(DATA_FILE, 'r') as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue
                
                parts = line.split('|')
                if len(parts) == 7:
                    student = {
                        'name': parts[0],
                        'id': parts[1],
                        'test1': float(parts[2]),
                        'test2': float(parts[3]),
                        'test3': float(parts[4]),
                        'average': float(parts[5]),
                        'grade': parts[6]
                    }
                    students.append(student)
    except Exception as e:
        print(f"Error loading student records: {e}")
        
    return students

def save_students(students):
    """Saves the list of student dictionaries back to the text file using a pipe-delimited format."""
    print("\nSaving records...")
    try:
        with open(DATA_FILE, 'w') as file:
            for s in students:
                line = f"{s['name']}|{s['id']}|{s['test1']:.2f}|{s['test2']:.2f}|{s['test3']:.2f}|{s['average']:.2f}|{s['grade']}\n"
                file.write(line)
        print(f"✓ Saved {len(students)} student record(s) to file.")
    except Exception as e:
        print(f"Error saving student records: {e}")

def add_student(students):
    """Prompts the user for a new student's details and adds them to the list."""
    print("\n========================")
    print("    ADD NEW STUDENT     ")
    print("========================")
    
    try:
        name = input("Enter student name: ").strip()
        student_id = input("Enter student ID: ").strip()
        test1 = float(input("Enter Test 1 score: "))
        test2 = float(input("Enter Test 2 score: "))
        test3 = float(input("Enter Test 3 score: "))
        
        avg = calculate_average(test1, test2, test3)
        grade = calculate_grade(avg)
        
        student = {
            'name': name,
            'id': student_id,
            'test1': test1,
            'test2': test2,
            'test3': test3,
            'average': avg,
            'grade': grade
        }
        
        students.append(student)
        print(f"\n✓ Added student: {name} (ID: {student_id})")
        print(f"  Average: {avg:.2f} | Grade: {grade}")
    except ValueError:
        print("Invalid input. Test scores must be numerical values.")

def display_students(students):
    """Displays all stored students in a neatly formatted table."""
    print("\nALL STUDENT RECORDS")
    print("================================================================================")
    print(f"{'Name':<20} | {'ID':<10} | {'Test 1':<8} | {'Test 2':<8} | {'Test 3':<8} | {'Average':<8} | {'Grade'}")
    print("================================================================================")
    
    if not students:
        print("No student records found.")
    else:
        for s in students:
            print(f"{s['name']:<20} | {s['id']:<10} | {s['test1']:<8.2f} | {s['test2']:<8.2f} | {s['test3']:<8.2f} | {s['average']:<8.2f} | {s['grade']}")
    
    print("================================================================================")
    print(f"Total students: {len(students)}")

def search_student(students):
    """Prompts for a student name and searches the list (case-insensitive)."""
    print("\n========================")
    print("     SEARCH STUDENT     ")
    print("========================")
    
    search_name = input("Enter student name to search: ").strip().lower()
    found = False
    
    for s in students:
        if s['name'].lower() == search_name:
            print("\nFound student:")
            print(f"Name: {s['name']}")
            print(f"ID: {s['id']}")
            print(f"Test 1: {s['test1']:.2f}")
            print(f"Test 2: {s['test2']:.2f}")
            print(f"Test 3: {s['test3']:.2f}")
            print(f"Average: {s['average']:.2f}")
            print(f"Grade: {s['grade']}")
            found = True
            break
            
    if not found:
        print(f"No student found with name: {search_name}")

def view_class_statistics(students):
    """Calculates and displays the highest average, lowest average, class average, and grade distribution."""
    print("\n========================")
    print("    CLASS STATISTICS    ")
    print("========================")
    
    if not students:
        print("Not enough data to calculate statistics.")
        return
        
    total_avg = 0
    highest_student = students[0]
    lowest_student = students[0]
    grades = {}
    
    for s in students:
        total_avg += s['average']
        
        # Track Highest
        if s['average'] > highest_student['average']:
            highest_student = s
            
        # Track Lowest
        if s['average'] < lowest_student['average']:
            lowest_student = s
            
        # Tally Grades
        if s['grade'] in grades:
            grades[s['grade']] += 1
        else:
            grades[s['grade']] = 1
            
    class_average = total_avg / len(students)
    
    print(f"Class Average:   {class_average:.2f}")
    print(f"Highest Average: {highest_student['average']:.2f} ({highest_student['name']})")
    print(f"Lowest Average:  {lowest_student['average']:.2f} ({lowest_student['name']})")
    print("\nGrade Distribution:")
    for grade, count in sorted(grades.items()):
        print(f"{grade}: {count} student(s)")


def main():
    """Main execution loop driving the menu options."""
    students = load_students()
    
    while True:
        print("\n===========================================")
        print("         STUDENT GRADE CALCULATOR          ")
        print("===========================================")
        print("1. Add New Student")
        print("2. Display All Students")
        print("3. Search Student by Name")
        print("4. View Class Statistics")
        print("5. Save and Exit (or press ESC)")
        
        choice = input("\nSelect an option (1-5) or press ESC to exit: ")
        
        if choice == '1':
            add_student(students)
        elif choice == '2':
            display_students(students)
        elif choice == '3':
            search_student(students)
        elif choice == '4':
            view_class_statistics(students)
        elif choice == '5' or choice == '\x1b' or choice == '^[':
            save_students(students)
            print("Thank you for using Student Grade Calculator!")
            break
        else:
            print("Invalid option. Please enter a number between 1 and 5.")

if __name__ == "__main__":
    main()