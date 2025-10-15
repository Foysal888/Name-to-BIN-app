import streamlit as st
import pandas as pd
from rapidfuzz import process, fuzz
import time

st.set_page_config(page_title="Name to BIN Matcher", layout="wide")
st.title(" 𝄃𝄃𝄂𝄂𝄀𝄁𝄃𝄂𝄂𝄃  BIN Matcher App ● Developed By Foysal Ahammed Mozumder")

uploaded_file = st.file_uploader("📂 Upload your Excel file", type=["xlsx"])
threshold = st.slider("🔍 Match Threshold (%)", 0, 100, 80)

if uploaded_file:
    try:
        # Read both sheets
        sheet1 = pd.read_excel(uploaded_file, sheet_name="HAWB-1")
        sheet2 = pd.read_excel(uploaded_file, sheet_name="BIN")

        st.info("Processing... please wait ⏳")
        progress_bar = st.progress(0)

        company_names = sheet2["COMPANY NAME"].astype(str).tolist()

        def get_bin_number(consignee):
            if pd.isna(consignee):
                return None
            match, score, idx = process.extractOne(consignee, company_names, scorer=fuzz.token_sort_ratio)
            if score >= threshold:
                return sheet2.iloc[idx]["VAT / BIN - NUMBER"]
            return None

        # Apply fuzzy matching with progress
        result_list = []
        total = len(sheet1)
        for i, val in enumerate(sheet1["Consignee"]):
            result_list.append(get_bin_number(val))
            if i % 10 == 0 or i == total - 1:
                progress_bar.progress(int((i + 1) / total * 100))

        sheet1["OCISupplementaryCustomsInfo"] = result_list

        st.success("✅ Matching Completed Successfully!")
        # Count values in each column
        consignee_count = sheet1["Consignee"].notna().sum()
        oci_count = sheet1["OCISupplementaryCustomsInfo"].notna().sum()

        st.info(f"📊 Total non-empty values in 'Consignee' column: {consignee_count}")
        st.info(f"📊 Total non-empty values in 'OCISupplementaryCustomsInfo' column: {oci_count}")
            

        # Show full dataframe (no row limit)
        st.dataframe(sheet1, use_container_width=True)

        # Save and provide download
        output_file = "output_matched.xlsx"
        try:
            sheet1.to_excel(output_file, index=False)
            with open(output_file, "rb") as f:
                st.download_button("📥 Download Full Result", f, file_name="output_matched.xlsx")
        except PermissionError:
            st.warning("⚠️ Please close 'output_matched.xlsx' and run again.")

    except Exception as e:
        st.error(f"❌ Error: {str(e)}")

else:
    st.info("👆 Please upload an Excel file to start.")
