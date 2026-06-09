import os

FILE_NAME = "student_grades.txt"


def calculate_average(test1, test2, test3):
    """Return the average of three test scores."""
    return (test1 + test2 + test3) / 3.0


def determine_grade(average):
    """Return the letter grade for a numeric average."""
    if average >= 90:
        return "A"
    if average >= 80:
        return "B"
    if average >= 70:
        return "C"
    if average >= 60:
        return "D"
    return "F"


def format_score(value):
    """Format numeric scores to two decimal places."""
    return f"{float(value):.2f}"


def load_students(file_name=FILE_NAME):
    """Load student records from the file, if available."""
    students = []
    if not os.path.exists(file_name):
        print("No saved student file found. Starting with an empty list.")
        return students

    try:
        with open(file_name, "r", encoding="utf-8") as file:
            for line_number, line in enumerate(file, start=1):
                line = line.strip()
                if not line:
                    continue
                parts = line.split("|")
                if len(parts) != 7:
                    print(f"Skipping invalid record at line {line_number}.")
                    continue

                name, student_id, test1, test2, test3, average, grade = parts
                students.append({
                    "name": name,
                    "id": student_id,
                    "test1": float(test1),
                    "test2": float(test2),
                    "test3": float(test3),
                    "average": float(average),
                    "grade": grade,
                })
        print(f"Loaded {len(students)} student record(s) from {file_name}.")
    except OSError as error:
        print(f"Error reading {file_name}: {error}")

    return students


def save_students(students, file_name=FILE_NAME):
    """Save student records to a pipe-delimited text file."""
    try:
        with open(file_name, "w", encoding="utf-8") as file:
            for student in students:
                file.write(
                    "|".join([
                        student["name"],
                        student["id"],
                        format_score(student["test1"]),
                        format_score(student["test2"]),
                        format_score(student["test3"]),
                        format_score(student["average"]),
                        student["grade"],
                    ]) + "\n"
                )
        print(f"Student records saved to {file_name}.")
        return True
    except OSError as error:
        print(f"Error writing {file_name}: {error}")
        return False


def add_student(students):
    """Prompt for student data and add a new record."""
    print("\nAdd a new student record")
    name = input("Enter student name: ").strip()
    if not name:
        print("Student name cannot be empty.")
        return

    student_id = input("Enter student ID: ").strip()
    if not student_id:
        print("Student ID cannot be empty.")
        return

    try:
        test1 = float(input("Enter Test 1 score: "))
        test2 = float(input("Enter Test 2 score: "))
        test3 = float(input("Enter Test 3 score: "))
    except ValueError:
        print("Please enter numeric test scores.")
        return

    average = calculate_average(test1, test2, test3)
    grade = determine_grade(average)

    students.append({
        "name": name,
        "id": student_id,
        "test1": test1,
        "test2": test2,
        "test3": test3,
        "average": average,
        "grade": grade,
    })

    print(f"Student {name} added successfully.")


def display_students(students):
    """Display all students in a formatted table."""
    if not students:
        print("\nNo student records to display.")
        return

    print("\nStudent Grade Records")
    print("-" * 110)
    print(f"{'Name':<18} {'ID':<10} {'Test 1':>8} {'Test 2':>8} {'Test 3':>8} {'Average':>10} {'Grade':>6}")
    print("-" * 110)
    for student in students:
        print(
            f"{student['name']:<18} "
            f"{student['id']:<10} "
            f"{format_score(student['test1']):>8} "
            f"{format_score(student['test2']):>8} "
            f"{format_score(student['test3']):>8} "
            f"{format_score(student['average']):>10} "
            f"{student['grade']:>6}"
        )
    print("-" * 110)


def display_statistics(students):
    """Display highest, lowest, class average, and grade distribution."""
    if not students:
        print("\nNo student records available for statistics.")
        return

    # Track highest and lowest using the whole student dictionary to keep their names
    highest_student = students[0]
    lowest_student = students[0]
    total_average = 0
    grade_counts = {}

    for student in students:
        total_average += student["average"]
        
        # Check for highest
        if student["average"] > highest_student["average"]:
            highest_student = student
            
        # Check for lowest
        if student["average"] < lowest_student["average"]:
            lowest_student = student
            
        # Tally the grades for the distribution
        grade = student["grade"]
        grade_counts[grade] = grade_counts.get(grade, 0) + 1

    class_average = total_average / len(students)

    print("\nClass Statistics")
    print("-" * 45)
    print(f"Class Average:   {format_score(class_average)}")
    print(f"Highest Average: {format_score(highest_student['average'])} ({highest_student['name']})")
    print(f"Lowest Average:  {format_score(lowest_student['average'])} ({lowest_student['name']})")
    
    print("\nGrade Distribution:")
    for grade, count in sorted(grade_counts.items()):
        print(f"{grade}: {count} student(s)")
    print("-" * 45)


def search_student(students):
    """Search for a student by name, case-insensitive."""
    query = input("Enter student name to search: ").strip().lower()
    if not query:
        print("Please enter a name to search.")
        return

    matches = [student for student in students if query in student["name"].lower()]
    if not matches:
        print("No matching student found.")
        return

    display_students(matches)


def show_menu():
    """Show the program menu."""
    print("\nStudent Grade Calculator")
    print("1. Add student")
    print("2. Display all students")
    print("3. Search student")
    print("4. Show statistics")
    print("5. Save records")
    print("6. Exit (ESC)")


def main():
    """Run the main program loop."""
    students = load_students()

    while True:
        show_menu()
        choice = input("Choose an option (1-6, or type ESC to exit): ").strip().lower()

        if choice in ("", "esc", "escape"):
            print("Exiting Student Grade Calculator. Goodbye!")
            break

        if choice == "1":
            add_student(students)
            save_students(students)
        elif choice == "2":
            display_students(students)
        elif choice == "3":
            search_student(students)
        elif choice == "4":
            display_statistics(students)
        elif choice == "5":
            save_students(students)
        elif choice == "6":
            print("Exiting Student Grade Calculator. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number from 1 to 6.")


if __name__ == "__main__":
    main()