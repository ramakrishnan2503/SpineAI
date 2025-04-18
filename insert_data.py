from db_helper import add_patient

def insert_dummy_data():
    dummy_patients = [
        {
            "patient_id": "P001",
            "name": "John Doe",
            "age": 45,
            "gender": "Male",
            "severity_history": "normal, mild"  
        },
        {
            "patient_id": "P002",
            "name": "Jane Smith",
            "age": 50,
            "gender": "Female",
            "severity_history": "severe, mild"
        },
        {
            "patient_id": "P003",
            "name": "Alice Johnson",
            "age": 60,
            "gender": "Female",
            "severity_history": "mild, severe"
        },
        {
            "patient_id": "P004",
            "name": "Bob Brown",
            "age": 38,
            "gender": "Male",
            "severity_history": "normal"
        },
        {
            "patient_id": "P005",
            "name": "Charlie Davis",
            "age": 55,
            "gender": "Male",
            "severity_history": "normal, severe"
        }
    ]

    inserted_count = 0
    for patient in dummy_patients:
        success = add_patient(
            patient_id=patient["patient_id"],
            name=patient["name"],
            age=patient["age"],
            gender=patient["gender"],
            severity_history=patient["severity_history"]
        )
        if success:
            print(f"Inserted patient {patient['patient_id']} - {patient['name']}")
            inserted_count += 1
        else:
            print(f"Failed to insert patient {patient['patient_id']} - {patient['name']} (Duplicate ID)")

    print(f"\nTotal Patients Inserted: {inserted_count} out of {len(dummy_patients)}")

insert_dummy_data()
