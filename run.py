import subprocess

def run_script(script_name):
    try:
        result = subprocess.run(['python', script_name], check=True)
        print(f"{script_name} executed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while executing {script_name}: {str(e)}")
        exit(1)  # Exit the script if any of the scripts fail

def main():
    scripts = ["company_scraper.py", "data_analysis.py", "data_storage.py", "api_server.py"]
    
    for script in scripts:
        run_script(script)

if __name__ == "__main__":
    main()
