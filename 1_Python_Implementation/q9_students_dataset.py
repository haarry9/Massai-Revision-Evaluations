students = [
    {"name": "Alice", "marks": [80, 75, 90]},
    {"name": "Bob", "marks": [70, 60, 65]},
    {"name": "Charlie", "marks": [95, 85, 100]},
    {"name": "David", "marks": [60, 70, 80]}
]

def map_student_grades(students):
    avgs = {s["name"]: sum(s["marks"])/len(s["marks"]) for s in students}

    grades = {
        "A" : {name for name, avg in avgs.items() if avg>=85},
        "B" : {name for name, avg in avgs.items() if 70 <= avg < 85},
        "C" : {name for name, avg in avgs.items() if avg<70},
    }
    return grades

result = map_student_grades(students)
print(result)