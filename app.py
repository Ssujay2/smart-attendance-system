import os
from datetime import date

import pandas as pd
import streamlit as st


STUDENTS_FILE = "students.csv"
ATTENDANCE_FILE = "attendance.csv"


def load_students():
    if os.path.exists(STUDENTS_FILE):
        return pd.read_csv(STUDENTS_FILE)

    df = pd.DataFrame(columns=["Student ID", "Name", "Class"])
    df.to_csv(STUDENTS_FILE, index=False)
    return df


def load_attendance():
    if os.path.exists(ATTENDANCE_FILE):
        return pd.read_csv(ATTENDANCE_FILE)

    df = pd.DataFrame(
        columns=["Date", "Student ID", "Name", "Class", "Status"]
    )
    df.to_csv(ATTENDANCE_FILE, index=False)
    return df


def save_attendance(df):
    df.to_csv(ATTENDANCE_FILE, index=False)


st.set_page_config(
    page_title="Smart Attendance System",
    page_icon="📋",
    layout="wide",
)

st.title("📋 Smart Attendance System")
st.write("Manage students and record daily attendance.")

students = load_students()
attendance = load_attendance()

tab1, tab2, tab3 = st.tabs(
    ["👨‍🎓 Students", "✅ Mark Attendance", "📊 Attendance Report"]
)

# ---------------- STUDENTS ----------------

with tab1:
    st.header("Student Management")

    with st.form("student_form"):
        student_id = st.text_input("Student ID")
        name = st.text_input("Student Name")
        student_class = st.text_input("Class")

        submitted = st.form_submit_button("Add Student")

        if submitted:
            if not student_id or not name or not student_class:
                st.warning("Please fill all fields.")

            elif student_id in students["Student ID"].astype(str).values:
                st.error("Student ID already exists.")

            else:
                new_student = pd.DataFrame(
                    [
                        {
                            "Student ID": student_id,
                            "Name": name,
                            "Class": student_class,
                        }
                    ]
                )

                students = pd.concat(
                    [students, new_student],
                    ignore_index=True,
                )

                students.to_csv(STUDENTS_FILE, index=False)

                st.success("Student added successfully.")
                st.rerun()

    st.subheader("Registered Students")

    if students.empty:
        st.info("No students registered yet.")
    else:
        st.dataframe(
            students,
            use_container_width=True,
            hide_index=True,
        )


# ---------------- ATTENDANCE ----------------

with tab2:
    st.header("Mark Attendance")

    if students.empty:
        st.warning("Please add students first.")

    else:
        selected_date = st.date_input(
            "Attendance Date",
            value=date.today(),
        )

        records = []

        for _, student in students.iterrows():
            status = st.selectbox(
                f"{student['Student ID']} - {student['Name']}",
                ["Present", "Absent"],
                key=f"status_{student['Student ID']}",
            )

            records.append(
                {
                    "Date": selected_date.strftime("%Y-%m-%d"),
                    "Student ID": student["Student ID"],
                    "Name": student["Name"],
                    "Class": student["Class"],
                    "Status": status,
                }
            )

        if st.button("Save Attendance", type="primary"):
            new_records = pd.DataFrame(records)

            attendance = attendance[
                ~(
                    (attendance["Date"] == selected_date.strftime("%Y-%m-%d"))
                    & (
                        attendance["Student ID"]
                        .astype(str)
                        .isin(students["Student ID"].astype(str))
                    )
                )
            ]

            attendance = pd.concat(
                [attendance, new_records],
                ignore_index=True,
            )

            save_attendance(attendance)

            st.success("Attendance saved successfully.")


# ---------------- REPORT ----------------

with tab3:
    st.header("Attendance Report")

    attendance = load_attendance()

    if attendance.empty:
        st.info("No attendance records available.")

    else:
        total_records = len(attendance)

        present_records = len(
            attendance[attendance["Status"] == "Present"]
        )

        percentage = (
            present_records / total_records * 100
            if total_records > 0
            else 0
        )

        col1, col2, col3 = st.columns(3)

        col1.metric("Total Records", total_records)
        col2.metric("Present", present_records)
        col3.metric(
            "Attendance %",
            f"{percentage:.2f}%"
        )

        st.subheader("Attendance Records")

        st.dataframe(
            attendance.sort_values(
                "Date",
                ascending=False,
            ),
            use_container_width=True,
            hide_index=True,
        )

        st.subheader("Student-wise Attendance")

        attendance["Present_Flag"] = (
            attendance["Status"] == "Present"
        ).astype(int)

        summary = (
            attendance
            .groupby(
                ["Student ID", "Name", "Class"],
                as_index=False,
            )
            .agg(
                Total_Days=("Status", "count"),
                Present_Days=("Present_Flag", "sum"),
            )
        )

        summary["Attendance %"] = (
            summary["Present_Days"]
            / summary["Total_Days"]
            * 100
        ).round(2)

        st.dataframe(
            summary,
            use_container_width=True,
            hide_index=True,
        )