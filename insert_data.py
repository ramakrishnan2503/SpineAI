# insert_dummy_data.py

from db_helper import add_patient

# insert_dummy_data.py

from db_helper import add_patient

def insert_dummy_data():
    dummy_patients = [
        {
            "patient_id": "P001",
            "name": "John Doe",
            "age": 45,
            "gender": "Male",
            "disease": "Lumbar Disc Herniation",
            "medical_history": "Hypertension",
            "allergies": "Penicillin",
            "medications": "Lisinopril",
            "recent_procedures": "None"
        },
        {
            "patient_id": "P002",
            "name": "Jane Smith",
            "age": 50,
            "gender": "Female",
            "disease": "Spinal Stenosis",
            "medical_history": "Diabetes",
            "allergies": "None",
            "medications": "Metformin",
            "recent_procedures": "Knee Surgery"
        },
        {
            "patient_id": "P003",
            "name": "Alice Johnson",
            "age": 60,
            "gender": "Female",
            "disease": "Osteoarthritis of Lumbar Spine",
            "medical_history": "Osteoporosis",
            "allergies": "Sulfa Drugs",
            "medications": "Alendronate",
            "recent_procedures": "Hip Replacement"
        },
        {
            "patient_id": "P004",
            "name": "Bob Brown",
            "age": 38,
            "gender": "Male",
            "disease": "Spondylolisthesis",
            "medical_history": "None",
            "allergies": "None",
            "medications": "None",
            "recent_procedures": "None"
        },
        {
            "patient_id": "P005",
            "name": "Charlie Davis",
            "age": 55,
            "gender": "Male",
            "disease": "Lumbar Spondylosis",
            "medical_history": "High Cholesterol",
            "allergies": "Aspirin",
            "medications": "Atorvastatin",
            "recent_procedures": "None"
        },
        {
            "patient_id": "P006",
            "name": "Diana Evans",
            "age": 47,
            "gender": "Female",
            "disease": "Lumbar Compression Fracture",
            "medical_history": "Asthma",
            "allergies": "None",
            "medications": "Albuterol",
            "recent_procedures": "Vertebroplasty"
        },
        {
            "patient_id": "P007",
            "name": "Ethan Foster",
            "age": 52,
            "gender": "Male",
            "disease": "Lumbar Radiculopathy",
            "medical_history": "None",
            "allergies": "NSAIDs",
            "medications": "Ibuprofen",
            "recent_procedures": "None"
        },
        {
            "patient_id": "P008",
            "name": "Fiona Green",
            "age": 49,
            "gender": "Female",
            "disease": "Lumbar Scoliosis",
            "medical_history": "None",
            "allergies": "None",
            "medications": "None",
            "recent_procedures": "None"
        },
        {
            "patient_id": "P009",
            "name": "George Harris",
            "age": 44,
            "gender": "Male",
            "disease": "Lumbar Kyphosis",
            "medical_history": "Back Pain",
            "allergies": "Latex",
            "medications": "Morphine",
            "recent_procedures": "None"
        },
        {
            "patient_id": "P010",
            "name": "Hannah Irving",
            "age": 53,
            "gender": "Female",
            "disease": "Lumbar Foraminal Stenosis",
            "medical_history": "Migraines",
            "allergies": "None",
            "medications": "Sumatriptan",
            "recent_procedures": "None"
        }
    ]

    inserted_count = 0
    for patient in dummy_patients:
        success = add_patient(
            patient_id=patient["patient_id"],
            name=patient["name"],
            age=patient["age"],
            gender=patient["gender"],
            disease=patient["disease"],
            medical_history=patient["medical_history"],
            allergies=patient["allergies"],
            medications=patient["medications"],
            recent_procedures=patient["recent_procedures"]
        )
        if success:
            print(f"Inserted patient {patient['patient_id']} - {patient['name']}")
            inserted_count += 1
        else:
            print(f"Failed to insert patient {patient['patient_id']} - {patient['name']} (Duplicate ID)")

    print(f"\nTotal Patients Inserted: {inserted_count} out of {len(dummy_patients)}")

if __name__ == "__main__":
    insert_dummy_data()
