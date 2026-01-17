import os
DATA_FILE = "students.txt"
def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")
def load_students():
    students = []
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            for line in f:
                if line.strip():
                    parts = line.strip().split("|")
                    if len(parts) == 6:
                        students.append(
                            {
                                "name": parts[0],
                                "math": float(parts[1]),
                                "science": float(parts[2]),
                                "english": float(parts[3]),
                                "total": float(parts[4]),
                                "percentage": float(parts[5]),
                            }
                        )
    return students
def save_students(students):
    with open(DATA_FILE, "w") as f:
        for student in students:
            f.write(
                f"{student['name']}|{student['math']}|{student['science']}|"
                f"{student['english']}|{student['total']}|{student['percentage']}\n"
            )


def calculate_results(math, science, english):
    total = math + science + english
    percentage = (total / 300) * 100
    return total, percentage
def add_student(students):
    clear_screen()
    print("=" * 50)
    print("ADD NEW STUDENT")
    print("=" * 50)

    name = input("Enter student name: ").strip()
    if not name:
        print("Name cannot be empty!")
        input("Press Enter to continue...")
        return

    try:
        print("\nEnter marks out of 100 for each subject:")
        math = float(input("Mathematics: "))
        science = float(input("Science: "))
        english = float(input("English: "))

        
        if not (0 <= math <= 100 and 0 <= science <= 100 and 0 <= english <= 100):
            print("Marks must be between 0 and 100!")
            input("Press Enter to continue...")
            return

        total, percentage = calculate_results(math, science, english)

        student = {
            "name": name,
            "math": math,
            "science": science,
            "english": english,
            "total": total,
            "percentage": percentage,
        }

        students.append(student)
        save_students(students)

        print("\n" + "=" * 50)
        print("Student added successfully!")
        print(f"Total Marks: {total}/300")
        print(f"Percentage: {percentage:.2f}%")
        print("=" * 50)

    except ValueError:
        print("Invalid input! Please enter numeric values.")

    input("\nPress Enter to continue...")


def view_all_students(students):
    """Display all students with their results"""
    clear_screen()
    print("=" * 80)
    print("ALL STUDENTS RESULTS")
    print("=" * 80)

    if not students:
        print("No students found in the database.")
    else:
        print(
            f"{'Name':<20} {'Math':<8} {'Science':<8} {'English':<8} {'Total':<8} {'%':<8} {'Grade'}"
        )
        print("-" * 80)

        for student in students:
            grade = get_grade(student["percentage"])
            print(
                f"{student['name']:<20} {student['math']:<8.1f} {student['science']:<8.1f} "
                f"{student['english']:<8.1f} {student['total']:<8.1f} "
                f"{student['percentage']:<8.2f} {grade}"
            )

    print("=" * 80)
    input("\nPress Enter to continue...")


def search_student(students):
    clear_screen()
    print("=" * 50)
    print("SEARCH STUDENT")
    print("=" * 50)

    name = input("Enter student name to search: ").strip().lower()

    found = False
    for student in students:
        if name in student["name"].lower():
            found = True
            grade = get_grade(student["percentage"])
            print("\n" + "=" * 50)
            print(f"Student Name: {student['name']}")
            print("-" * 50)
            print(f"Mathematics:  {student['math']}/100")
            print(f"Science:      {student['science']}/100")
            print(f"English:      {student['english']}/100")
            print("-" * 50)
            print(f"Total Marks:  {student['total']}/300")
            print(f"Percentage:   {student['percentage']:.2f}%")
            print(f"Grade:        {grade}")
            print("=" * 50)

    if not found:
        print(f"No student found with name containing '{name}'")

    input("\nPress Enter to continue...")


def get_grade(percentage):
    if percentage >= 90:
        return "A+"
    elif percentage >= 80:
        return "A"
    elif percentage >= 70:
        return "B"
    elif percentage >= 60:
        return "C"
    elif percentage >= 50:
        return "D"
    else:
        return "F"


def delete_student(students):
    clear_screen()
    print("=" * 50)
    print("DELETE STUDENT")
    print("=" * 50)

    if not students:
        print("No students to delete.")
        input("Press Enter to continue...")
        return

    for i, student in enumerate(students, 1):
        print(f"{i}. {student['name']} - {student['percentage']:.2f}%")

    try:
        choice = int(input("\nEnter student number to delete (0 to cancel): "))
        if choice == 0:
            return
        if 1 <= choice <= len(students):
            deleted = students.pop(choice - 1)
            save_students(students)
            print(f"{deleted['name']} deleted successfully!")
        else:
            print("Invalid student number!")
    except ValueError:
        print("Invalid input!")

    input("\nPress Enter to continue...")


def display_menu():
    clear_screen()
    print("=" * 50)
    print("STUDENT RESULTS MANAGEMENT SYSTEM")
    print("=" * 50)
    print("1. Add New Student")
    print("2. View All Students")
    print("3. Search Student")
    print("4. Delete Student")
    print("5. Exit")
    print("=" * 50)


def main():
    students = load_students()

    while True:
        display_menu()
        choice = input("Enter your choice (1-5): ").strip()

        if choice == "1":
            add_student(students)
        elif choice == "2":
            view_all_students(students)
        elif choice == "3":
            search_student(students)
        elif choice == "4":
            delete_student(students)
        elif choice == "5":
            print("\nThank you for using Student Results Manager!")
            print("All data saved to students.txt")
            break
        else:
            print("Invalid choice! Please enter 1-5.")
            input("Press Enter to continue...")


if __name__ == "__main__":
    main()
