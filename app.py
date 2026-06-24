import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# ---------------- 1. PAGE CONFIGURATION ----------------
st.set_page_config(page_title="Academic Enterprise Portal", layout="wide")

# ---------------- 2. SECURE LOGIN SYSTEM STATE ----------------
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

# ---------------- 3. DATA ARCHITECTURE GENERATION ----------------
@st.cache_data
def load_comprehensive_data():
    np.random.seed(42)
    num_students = 100
    subjects = ["Python", "Data_Analytics", "Web_Dev", "DBMS", "Machine_Learning", "Cloud_Computing"]
    sections = ["Section A", "Section B", "Section C", "Section D"]

    data = {
        "Roll_No": [f"2026CS{i:03d}" for i in range(1, 101)],
        "Student_Name": [f"Student {i}" for i in range(1, 101)],
        "Class_Section": np.random.choice(sections, num_students),
        "Gender": np.random.choice(["Male", "Female"], num_students),
        "Attendance_%": np.random.randint(55, 100, num_students)
    }

    for sub in subjects:
        data[sub] = np.random.randint(20, 100, num_students)

    df = pd.DataFrame(data)
    df["Total_Marks"] = df[subjects].sum(axis=1)
    df["Average"] = round(df["Total_Marks"] / len(subjects), 2)
    df["Status"] = np.where((df[subjects] >= 40).all(axis=1), "Pass", "Fail")
    
    schools = [f"School {chr(65+i)}" for i in range(15)]
    school_data = {
        "School_Name": schools,
        "School_Attendance_Avg": np.random.uniform(70, 95, 15),
        "School_Pass_Rate": np.random.uniform(60, 98, 15)
    }
    df_schools = pd.DataFrame(school_data)
    
    our_school_row = pd.DataFrame([{
        "School_Name": "⭐ Our School (Naan Mudhalvan Hub)",
        "School_Attendance_Avg": df["Attendance_%"].mean(),
        "School_Pass_Rate": (df["Status"] == "Pass").mean() * 100
    }])
    df_schools = pd.concat([df_schools, our_school_row], ignore_index=True)

    return df, subjects, df_schools

df, subjects, df_schools = load_comprehensive_data()

# ---------------- 4. INTERACTIVE LOGIN INTERFACE ----------------
if not st.session_state["logged_in"]:
    st.markdown("<h2 style='text-align: center;'>🔐 Academic Analytics Enterprise Portal</h2>", unsafe_allow_html=True)
    
    col_l, col_m, col_r = st.columns([1, 2, 1])
    with col_m:
        st.write("### Please Login to Access the Dashboard")
        username = st.text_input("Username (Email ID)", placeholder="example@gmail.com")
        password = st.text_input("Password (6-Digit PIN)", type="password", placeholder="******")
        
        if st.button("Sign In 🚀", use_container_width=True):
            if "@gmail.com" in username and len(password) == 6:
                st.session_state["logged_in"] = True
                st.success("Access Granted! Loading Portal...")
                st.rerun()
            else:
                st.error("❌ Invalid Access! Ensure Email contains '@gmail.com' and Password is exactly 6 digits.")
else:
    # ---------------- 5. ENTERPRISE PORTAL DASHBOARD ----------------
    col_title, col_logout = st.columns([6, 1])
    with col_title:
        st.title("🎓 Smart Academic System & Result Management App")
        st.markdown("**Naan Mudhalvan Technical Arts Portfolio 2026**")
    with col_logout:
        if st.button("Sign Out 🚪", use_container_width=True):
            st.session_state["logged_in"] = False
            st.rerun()

    st.markdown("---")

    # KPI CARDS
    st.markdown("### 📈 Institutional Key Performance Indicators (KPIs)")
    kpi1, kpi2, kpi3 = st.columns(3)
    kpi1.metric("📌 Total Enrolled Students", f"{len(df)} Students")
    overall_pass = round((df["Status"] == "Pass").mean() * 100, 2)
    kpi2.metric("✅ Overall Pass Percentage", f"{overall_pass}%")
    overall_attendance = round(df["Attendance_%"].mean(), 2)
    kpi3.metric("🕒 Overall Attendance Percentage", f"{overall_attendance}%")

    st.markdown("---")

    # 🆕 1. INTERACTIVE FULL STUDENT DATA REPORT TABLE
    st.markdown("### 📑 Full Interactive Student Database Report")
    st.write("Keela irukura table-la Roll No, Student Name, 6 Subjects, Total Marks, Attendance, Pass/Fail status ella datavum live-ah interactive format-la irukku. Neenga search illa filter-um panni paarkalam:")
    
    # Grid View-la total data-vum theriyum
    st.dataframe(df, use_container_width=True)

    st.markdown("---")

    # 🆕 2. SECTION-WISE TOPPERS CORNER
    st.markdown("### 🏆 Section-wise Academic Toppers Corner")
    st.write("Ovvoru Class Section (Section A, B, C, D) laiyum yar **Mugavuriyana Topper** (Highest Total Marks) nu inge paarkalam:")
    
    topper_cols = st.columns(4)
    sections_list = ["Section A", "Section B", "Section C", "Section D"]
    
    for idx, sec in enumerate(sections_list):
        sec_df = df[df["Class_Section"] == sec]
        if not sec_df.empty:
            # Group-la yaruku highest Total Marks-o avangala edukkum
            topper_row = sec_df.loc[sec_df["Total_Marks"].idxmax()]
            with topper_cols[idx]:
                st.markdown(f"""
                <div style='background-color:#1E1E1E; padding:15px; border-radius:10px; border-left: 5px solid #F59E0B;'>
                    <h4 style='color:#F59E0B; margin:0;'>🥇 {sec}</h4>
                    <p style='margin:5px 0; font-weight:bold;'>{topper_row['Student_Name']}</p>
                    <p style='margin:0; font-size:14px; color:#A0A0A0;'>Roll No: {topper_row['Roll_No']}</p>
                    <p style='margin:0; font-size:14px; color:#10B981;'><b>Total: {topper_row['Total_Marks']}</b> ({topper_row['Average']}%)</p>
                </div>
                """, unsafe_allow_html=True)

    st.markdown("---")

    # CHARTS SECTION
    st.markdown("### 🎨 Visual Analytics & Performance Benchmarking")
    left, right = st.columns(2)

    with left:
        st.subheader("🍩 Overall Pass vs Fail Breakdown (Donut Chart)")
        fig_donut = px.pie(df, names="Status", hole=0.55, color="Status", color_discrete_map={"Pass": "#10B981", "Fail": "#EF4444"})
        st.plotly_chart(fig_donut, use_container_width=True)

    with right:
        st.subheader("🎯 Subject-wise Section Performance Analysis")
        selected_subject = st.selectbox("Choose Subject for Section Comparison", subjects)
        
        subject_colors = {
            "Python": "#3B82F6", "Data_Analytics": "#10B981", "Web_Dev": "#F59E0B",
            "DBMS": "#EC4899", "Machine_Learning": "#8B5CF6", "Cloud_Computing": "#06B6D4"
        }
        chosen_color = subject_colors.get(selected_subject, "#34495E")

        sub_sec_avg = df.groupby("Class_Section")[selected_subject].mean().reset_index()
        fig_sub_bar = px.bar(
            sub_sec_avg, x="Class_Section", y=selected_subject,
            title=f"Class Performance for {selected_subject}",
            text_auto=".1f"
        )
        fig_sub_bar.update_traces(marker_color=chosen_color, textposition="outside")
        fig_sub_bar.update_layout(template="plotly_white", yaxis_title="Average Mark")
        st.plotly_chart(fig_sub_bar, use_container_width=True)

    st.markdown("---")

    # STUDENT PROFILING
    st.markdown("### 🔍 Student Longitudinal Profiling (Identifying Weak Students)")
    selected_student = st.selectbox("Select Student Name to Analyze Performance Across Subjects", df["Student_Name"].unique())
    
    student_row = df[df["Student_Name"] == selected_student].iloc[0]
    student_scores = [student_row[sub] for sub in subjects]
    
    df_student_profile = pd.DataFrame({"Subject": subjects, "Marks Obtained": student_scores})
    
    fig_line = px.line(df_student_profile, x="Subject", y="Marks Obtained", markers=True, title=f"Academic Trajectory for {selected_student}")
    fig_line.update_traces(line=dict(color="#FF5722", width=3), marker=dict(size=10, color="#D35400"))
    fig_line.add_hline(y=40, line_dash="dash", line_color="red", annotation_text="Passing Threshold (40 Marks)")
    fig_line.update_layout(template="plotly_white", yaxis_range=[0, 105])
    st.plotly_chart(fig_line, use_container_width=True)
    
    low_subs = df_student_profile[df_student_profile["Marks Obtained"] < 40]["Subject"].tolist()
    if low_subs:
        st.error(f"⚠️ **Attention Required:** {selected_student} is currently failing in: **{', '.join(low_subs)}**. Immediate academic counseling suggested.")
    else:
        st.success(f"🎉 **Safe Zone:** {selected_student} has cleared the passing threshold across all corporate curriculum domains.")

    st.markdown("---")

    # REGIONAL BENCHMARKING
    st.markdown("### 🏆 Regional Institutional Benchmarking (Trend Scatter Plot)")
    st.write("See where our institution stacks up against regional competitor schools based on Attendance vs Passing Ratios.")
    
    fig_trend = px.scatter(
        df_schools, x="School_Attendance_Avg", y="School_Pass_Rate",
        text="School_Name",
        color="School_Name", color_discrete_sequence=px.colors.qualitative.Dark24,
        title="Regional Matrix: Attendance Rate vs Passing Standards"
    )
    st.plotly_chart(fig_trend, use_container_width=True)

    st.markdown("---")
    # CSV FILE DOWNLOAD SECTION
    st.markdown("### 📥 Download Student Academic Data (Excel / CSV)")
    csv_data = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download Full Report as CSV 📄",
        data=csv_data,
        file_name="Student_Academic_Report.csv",
        mime="text/csv",
        use_container_width=True
    )
