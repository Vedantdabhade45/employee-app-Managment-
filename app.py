import streamlit as st

# Session state me employees list ko initialize karna taaki data refresh hone par delete na ho
if "employees" not in st.session_state:
    st.session_state.employees = []

st.title("👥 Employee Management System")
st.divider()

# Sidebar Navigation
menu = ["Add Employee", "Display & Search", "Update Employee", "Delete Employee"]
choice = st.sidebar.selectbox("Navigation Menu", menu)

# 1. Add Employee
if choice == "Add Employee":
    st.subheader("➕ Add New Employee")
    
    with st.form("add_employee_form"):
        name = st.text_input("Employee Name")
        department = st.text_input("Department")
        empcode = st.number_input("Employee Code", min_value=1, step=1)
        salary = st.text_input("Salary")
        
        submit_btn = st.form_submit_button("Add Employee")
        
        if submit_btn:
            if name.strip() and department.strip() and salary.strip():
                code_exists = any(emp["Empcode"] == int(empcode) for emp in st.session_state.employees)
                
                if code_exists:
                    st.error(f"Employee code {empcode} pehle se maujood hai!")
                else:
                    employee = {
                        "Name": name,
                        "Department": department,
                        "Empcode": int(empcode),
                        "Salary": salary
                    }
                    st.session_state.employees.append(employee)
                    st.success(f"Employee '{name}' safaltapurvak add ho gaya hai! 🎉")
            else:
                st.warning("Kripya sabhi fields ko bharein.")

# 2. Display & Search Employees
elif choice == "Display & Search":
    st.subheader("📋 Employee Records")
    
    if not st.session_state.employees:
        st.info("Koi bhi employee nahi mila.")
    else:
        search_query = st.text_input("🔍 Search Employee by Name").strip().lower()
        
        filtered_list = st.session_state.employees
        if search_query:
            filtered_list = [emp for emp in st.session_state.employees if search_query in emp["Name"].lower()]
            if not filtered_list:
                st.warning("Is naam ka koi employee available nahi hai.")
        
        if filtered_list:
            st.write(f"Total Employees: **{len(filtered_list)}**")
            
            for index, emp in enumerate(filtered_list):
                with st.expander(f"👤 {emp['Name']} (Code: {emp['Empcode']})"):
                    st.write(f"**Department:** {emp['Department']}")
                    st.write(f"**Salary:** {emp['Salary']}")

# 3. Update Employee
elif choice == "Update Employee":
    st.subheader("✏️ Update Employee Details")
    
    if not st.session_state.employees:
        st.info("Update karne ke liye koi employee available nahi hai.")
    else:
        emp_names = [emp["Name"] for emp in st.session_state.employees]
        selected_name = st.selectbox("Update karne ke liye Employee chunein", emp_names)
        
        emp_to_update = next((emp for emp in st.session_state.employees if emp["Name"] == selected_name), None)
        
        if emp_to_update:
            with st.form("update_form"):
                new_dept = st.text_input("New Department", value=emp_to_update["Department"])
                new_code = st.number_input("New Employee Code", value=int(emp_to_update["Empcode"]), min_value=1, step=1)
                new_salary = st.text_input("New Salary", value=emp_to_update["Salary"])
                
                update_btn = st.form_submit_button("Update Employee")
                
                if update_btn:
                    emp_to_update["Department"] = new_dept
                    emp_to_update["Empcode"] = int(new_code)
                    emp_to_update["Salary"] = new_salary
                    st.success(f"Employee '{selected_name}' ki details update ho gayi hain! ✅")

# 4. Delete Employee
elif choice == "Delete Employee":
    st.subheader("🗑️ Delete Employee")
    
    if not st.session_state.employees:
        st.info("Delete karne ke liye koi employee available nahi hai.")
    else:
        emp_names = [emp["Name"] for emp in st.session_state.employees]
        selected_name = st.selectbox("Delete karne ke liye Employee chunein", emp_names)
        
        if st.button("Delete Employee", type="primary"):
            st.session_state.employees = [emp for emp in st.session_state.employees if emp["Name"] != selected_name]
            st.success(f"Employee '{selected_name}' ko hata diya gaya hai!")
            st.rerun()
