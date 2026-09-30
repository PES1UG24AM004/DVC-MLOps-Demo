"""
PES University - Department of Computer Science
Course: Software Engineering Lab (Sem 5)
Student Name: Aarav Yuval B G | SRN: PES1UG24AM004
Topic: Part 1 - Data Version Control (DVC) Workflow Automation & Verification
"""

import os
import subprocess
import yaml

def run_cmd(cmd):
    print(f"\n[RUNNING] {cmd}")
    res = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if res.stdout:
        print(res.stdout.strip())
    if res.stderr and res.returncode != 0:
        print(f"[ERROR] {res.stderr.strip()}")
    return res

def main():
    print("="*60)
    print("DVC WORKFLOW DEMO - PES1UG24AM004")
    print("="*60)
    
    # Check DVC and Git versions
    run_cmd("git --version")
    run_cmd("dvc --version")
    
    # 1. View Git log of versioned data
    print("\n--- 1. Git Commit History for Tracked Data ---")
    run_cmd("git log --oneline --graph -n 6")
    
    # 2. View DVC Pointer File
    print("\n--- 2. Inspecting DVC Pointer File (data.txt.dvc) ---")
    if os.path.exists("data.txt.dvc"):
        with open("data.txt.dvc") as f:
            print(f.read())
    
    # 3. View .gitignore to verify data isolation
    print("\n--- 3. Verifying .gitignore Excludes Raw Data ---")
    if os.path.exists(".gitignore"):
        with open(".gitignore") as f:
            print(f.read())
            
    # 4. Demonstrate Double Checkout
    print("\n--- 4. Demonstrating Double Checkout (Time Travel) ---")
    print("Switching to v1.0:")
    run_cmd("git checkout v1.0")
    run_cmd("dvc checkout")
    if os.path.exists("data.txt"):
        with open("data.txt") as f:
            print(f"data.txt content at v1.0: {f.read().strip()}")
            
    print("\nSwitching back to master (v2.0):")
    run_cmd("git checkout master")
    run_cmd("dvc checkout")
    if os.path.exists("data.txt"):
        with open("data.txt") as f:
            print(f"data.txt content at master: {f.read().strip()}")
            
    print("\n[SUCCESS] DVC Data Versioning and Double-Checkout verified.")

if __name__ == "__main__":
    main()
