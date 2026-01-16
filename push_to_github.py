import subprocess
import sys

def run_command(command):
    try:
        result = subprocess.run(
            command,
            shell=True,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {command}")
        print(e.stderr)
        sys.exit(1)

def main():
    print("🚀 Starting GitHub Push Process...")

    # 1. Add all files
    print("\n📦 Adding files...")
    run_command("git add .")

    # 2. Commit changes
    print("\n📝 Committing changes...")
    commit_message = input("Enter commit message (default: 'Update project'): ") or "Update project"
    # We use || echo to prevent failure if there's nothing to commit
    try:
        subprocess.run(f'git commit -m "{commit_message}"', shell=True, check=True)
    except subprocess.CalledProcessError:
        print("Nothing to commit or commit failed (maybe no changes?). Continuing...")

    # 3. Ensure branch is main
    print("\n🌿 Ensuring branch is 'main'...")
    run_command("git branch -M main")

    # 4. Push to origin
    print("\n⬆️ Pushing to GitHub...")
    run_command("git push -u origin main")

    print("\n✅ Done! Code pushed successfully.")

if __name__ == "__main__":
    main()
