import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os
import re

def run_deep_fairness_audit():
    # Naya header takay aapko terminal mein pata chalay ke naya code chal raha hai
    print("\n--- ⚖️ Executing DEEP Automated Fairness Audit Pipeline ---")

    try:
        # File path
        file_path = os.path.join("data", "Gender_StatsEXCEL.xlsx")

        # Load Excel (Sheet: footnote)
        df = pd.read_excel(file_path, sheet_name="footnote")
        print(f"[INFO] Dataset loaded successfully with {len(df)} records.")

        # DEEP Gender detector using Regex for patterns like .FE. and .MA.
        def deep_detect_gender(row):
            desc = str(row['DESCRIPTION']).lower()
            code = str(row['SeriesCode']).lower()
            
            # Female indicators (.fe., female, maternal mortality)
            if re.search(r'\.fe\.|female|mmrt|maternal', desc + code):
                return 'Female-Specific'
            # Male indicators (.ma., male)
            elif re.search(r'\.ma\.|male', desc + code):
                return 'Male-Specific'
            else:
                return 'General/Neutral'

        # Category column banayein
        df["Category"] = df.apply(deep_detect_gender, axis=1)

        # Count results
        audit_results = df["Category"].value_counts().reset_index()
        audit_results.columns = ["Category", "Data_Points"]

        print("\n--- 📊 Deep Audit Findings ---")
        print(audit_results)

        # Plotting with Log Scale
        sns.set_theme(style="whitegrid")
        plt.figure(figsize=(10, 6))

        # Graph banayein
        plot = sns.barplot(
            data=audit_results,
            x="Category",
            y="Data_Points",
            hue="Category",
            palette="magma",
            legend=False
        )

        # LOG SCALE: Ye sab se aham hai choti bars dekhne ke liye
        plt.yscale('log') 
        
        plt.title("Feminist Audit: Deep Representation Analysis", fontsize=14)
        plt.xlabel("Data Category")
        plt.ylabel("Number of Records (Log Scale)")

        # Save naya graph
        output_file = "deep_audit_report.png"
        plt.savefig(output_file)

        print(f"\n[SUCCESS] Deep Audit Report saved as '{output_file}'")
        plt.show()

    except Exception as e:
        print(f"[ERROR] Could not complete deep audit: {e}")

if __name__ == "__main__":
    run_deep_fairness_audit()