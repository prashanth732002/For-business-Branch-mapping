import streamlit as st
import pandas as pd
from io import BytesIO

st.title("📊 Branch Role Mapping Processor")

st.markdown("""
Upload your Excel file and this app will extract **Branch, Branch ID, District** 
along with role mappings (AM, DM, RM), then stack them one below the other 
with a Role column.
""")

# Upload Excel file
uploaded_file = st.file_uploader("📂 Upload Excel file", type=["xlsx"])

if uploaded_file:
    # Read Excel
    df = pd.read_excel(uploaded_file)

    # Define the roles and their employee ID columns
    roles = {
        "AM": "AM Emp ID",
        "DM": "DM Emp ID",
        "RM": "RM Emp ID"
    }

    # Collect role-based data
    role_data = []
    for role, emp_col in roles.items():
        if role in df.columns and emp_col in df.columns:
            temp = df[["Branch", "Branch ID", "District", role, emp_col]].copy()
            temp["Role"] = role
            temp.rename(columns={role: "Employee Name", emp_col: "Employee ID"}, inplace=True)
            role_data.append(temp)

    # Combine into one dataframe
    if role_data:
        final_df = pd.concat(role_data, ignore_index=True)

        st.success("✅ File processed successfully!")
        st.dataframe(final_df)

        # Export to Excel
        output = BytesIO()
        with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
            final_df.to_excel(writer, index=False, sheet_name="RoleMapping")
        output.seek(0)

        # Download button
        st.download_button(
            label="📥 Download Processed File",
            data=output,
            file_name="processed_mapping.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    else:
        st.error("⚠️ Required columns (AM/DM/RM) not found in the uploaded file!")
