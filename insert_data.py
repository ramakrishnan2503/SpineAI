from db_helper import add_patient

def insert_dummy_data():
    dummy_patients = [
        {
            "patient_id": "1",
            "name": "John Doe",
            "age": 45,
            "gender": "Male",
            "severity_history": "2024-03-01 10:00:00 normal,2024-03-15 14:30:00 mild"
        },
        {
            "patient_id": "2",
            "name": "Jane Smith",
            "age": 50,
            "gender": "Female",
            "severity_history": "2024-02-20 09:45:00 severe,2024-03-10 13:20:00 mild"
        },
        {
            "patient_id": "3",
            "name": "Alice Johnson",
            "age": 60,
            "gender": "Female",
            "severity_history": "2024-01-25 08:15:00 mild,2024-03-18 16:45:00 severe"
        },
        {
            "patient_id": "4",
            "name": "Bob Brown",
            "age": 38,
            "gender": "Male",
            "severity_history": "2024-04-10 11:00:00 normal"
        },
        {
            "patient_id": "5",
            "name": "Charlie Davis",
            "age": 55,
            "gender": "Male",
            "severity_history": "2024-02-28 10:30:00 normal,2024-04-01 15:00:00 severe"
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
