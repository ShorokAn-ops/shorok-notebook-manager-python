import json
import os
from datetime import datetime

file_name = "notes.json"


def load_notes():
    if not os.path.exists(file_name):
        return []
    try:
        with open(file_name, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print("Failed to read notes file:", e)
        print("Starting with empty notebook.")
        return []
    

def save_notes(notes):
    try:
        with open(file_name, "w") as f:
            json.dump(notes, f, ensure_ascii=False, indent=2) #ensure_ascii=False -> שמור את הטקסט בקובץ כמו שהוא – כולל עברית – בלי להמיר אותו לקודים
    except Exception as e:
        print("Error saving notes:", e)


def add_note(notes):
    print("\n Add New Note ")
    title = input("Title: ").strip() #strip -> מסיר רווחים מיותרים מההתחלה ומהסוף
    content = input("Content: ").strip()
    tags = input("Tags (comma separated): ").strip()
    date= datetime.now().strftime("%d/%m/%Y")  # auto timestamp
    
    note = {
        "title": title,
        "content": content,
        "tags": [t.strip() for t in tags.split(",")] if tags else [],
        "date": date
    }
    notes.append(note)
    save_notes(notes)
    print("✅ Note added successfully.\n")


def list_notes(notes):
    if not notes:
        print("No notes yet.")
        return
    print("\n All Notes : \n")

    for i, note in enumerate(notes, start=1):
        print(f"\n[{i}] {note['title']}")
        print("Tags:", ", ".join(note["tags"]) if note["tags"] else "None")
        print("Content:", note["content"])
        print(f"Date  : {note.get('date')}")
    print(f"Total Notes: {len(notes)}\n")


def search_notes(notes):
    print("\n Search Notes ")
    keyword = input("Enter keyword to search (title or content): ").strip().lower()
    found = False
    for i, note in enumerate(notes, start=1):
        if keyword in note["title"].lower() or keyword in note["content"].lower():
            print(f"\n[{i}] {note['title']}")
            print("Content:", note["content"])
            print("Tags:", ", ".join(note["tags"]) if note["tags"] else "None")
            print(f"Date: {note.get('date')}")
            found = True

    print("The search is complete.")
    if not found:
        print("No matches found.")


def filter_by_tag(notes):
    print("\n Filter by Tag ")
    tag = input("Tag: ").strip().lower()
    found = False

    for i, note in enumerate(notes, start=1):
        tags_lower = [t.lower() for t in note["tags"]]
        if tag in tags_lower:
            print(f"\n[{i}] {note['title']}")
            print("Tags:", ", ".join(note["tags"]))
            print("Content:", note["content"])
            print(f"Date: {note.get('date')}")
            found = True
    print("Filtering by Tag complete.")
    if not found:
        print("No notes with this tag.")


def edit_note(notes):
    list_notes(notes)
    if not notes:
        print("No notes to edit.\n")
        return
    
    print("\n Edit Note \n")
    try:
        num = int(input("Choose note index: ")) - 1
    except ValueError:
        print("Please enter a valid number.\n")
        return
    
    if num < 0 or num >= len(notes):
        print("Invalid number.\n")
        print(f"Index must be between 0 and {len(notes)} \n")
        return

    print("Leave blank to keep current value.")
    new_title = input("New title: ").strip()
    new_content = input("New content: ").strip()
    new_tags = input("New tags (comma separated): ").strip()

    changes_made = False
    if new_title:
        notes[num]["title"] = new_title
        changes_made = True
    if new_content:
        notes[num]["content"] = new_content
        changes_made = True
    if new_tags:
        notes[num]["tags"] = [t.strip() for t in new_tags.split(",")]
        changes_made = True
    if not changes_made:
        print("No changes made.\n")
        return

    notes[num]["date"] = datetime.now().strftime("%d/%m/%Y")  # update timestamp only if changed
    save_notes(notes)
    print("✅ Note updated! \n")


def delete_note(notes):
    list_notes(notes)
    if not notes:
        print("No notes to delete.\n")
        return
    
    print("\n Delete Note \n")
    try:
        num = int(input("Choose note index: ")) - 1
    except ValueError:
        print("Please enter a valid number.\n")
        return

    if num < 0 or num >= len(notes):
        print("Invalid number.")
        print(f"Index must be between 1 and {len(notes)} \n")
        return
    
    confirm = input("Type 'yes' to confirm deletion: ").strip().lower()
    if confirm != "yes":
        print("Deletion cancelled.\n")
        return
    notes.pop(num)
    save_notes(notes)
    print("🗑️ Note deleted!")


def main():
    notes = load_notes()
    menu = (
            "(1) Add note\n"
            "(2) List notes\n"
            "(3) Search notes by keyword\n"
            "(4) Filter notes by tag\n"
            "(5) Edit a note\n"
            "(6) Delete a note\n"
            "(0) Exit\n"
        )
    
    print("Welcome to Personal Notebook Manager")

    while True:
        print(menu)
        choice = input("Choose: ").strip()

        if choice == "1":
            add_note(notes)
        elif choice == "2":
            list_notes(notes)
        elif choice == "3":
            search_notes(notes)
        elif choice == "4":
            filter_by_tag(notes)
        elif choice == "5":
            edit_note(notes)
        elif choice == "6":
            delete_note(notes)
        elif choice == "0":
            print("thank you for using the Personal Notebook Manager.\n Goodbye!\n")
            break
        else:
            print("Invalid choice.\n")


if __name__ == "__main__":
    main()
