import tkinter as tk
from tkinter import messagebox, simpledialog
import datetime
import os
import sys

class SimpleOS:
    def __init__(self, root):
        self.root = root
        self.root.title("SimpleOS")
        self.root.geometry("800x600")
        self.root.configure(bg='darkblue')

        # Create menu bar
        self.menu_bar = tk.Menu(root)
        root.config(menu=self.menu_bar)

        # System menu
        self.system_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="System", menu=self.system_menu)
        self.system_menu.add_command(label="Shutdown", command=self.shutdown)
        self.system_menu.add_command(label="Restart", command=self.restart)

        # Applications menu
        self.apps_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Apps", menu=self.apps_menu)
        self.apps_menu.add_command(label="Notepad", command=self.open_notepad)
        self.apps_menu.add_command(label="Terminal", command=self.open_terminal)

        # Status bar
        self.status_bar = tk.Label(root, text="SimpleOS Ready", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

        # Clock update
        self.update_clock()

    def update_clock(self):
        """Update system clock in status bar"""
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.status_bar.config(text=f"SimpleOS | {current_time}")
        self.root.after(1000, self.update_clock)

    def shutdown(self):
        """Shutdown the system"""
        if messagebox.askyesno("Shutdown", "Are you sure you want to shutdown?"):
            messagebox.showinfo("Shutdown", "System is powering off...")
            self.root.quit()

    def restart(self):
        """Restart the system"""
        if messagebox.askyesno("Restart", "Are you sure you want to restart?"):
            messagebox.showinfo("Restart", "System is restarting...")
            python = sys.executable
            os.execl(python, python, *sys.argv)

    def open_notepad(self):
        """Open a simple notepad application"""
        notepad_window = tk.Toplevel(self.root)
        notepad_window.title("SimpleOS Notepad")
        notepad_window.geometry("600x400")

        text_area = tk.Text(notepad_window, wrap=tk.WORD)
        text_area.pack(expand=True, fill=tk.BOTH)

        # Notepad menu
        notepad_menu = tk.Menu(notepad_window)
        notepad_window.config(menu=notepad_menu)

        file_menu = tk.Menu(notepad_menu, tearoff=0)
        notepad_menu.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New", command=lambda: text_area.delete('1.0', tk.END))
        file_menu.add_command(label="Save", command=self.save_file)
        file_menu.add_command(label="Open", command=self.open_file)

    def open_terminal(self):
        """Open a simple terminal application"""
        terminal_window = tk.Toplevel(self.root)
        terminal_window.title("SimpleOS Terminal")
        terminal_window.geometry("700x400")

        output_area = tk.Text(terminal_window, wrap=tk.WORD, state=tk.DISABLED)
        output_area.pack(expand=True, fill=tk.BOTH)

        input_area = tk.Entry(terminal_window)
        input_area.pack(fill=tk.X)

        def execute_command(event):
            command = input_area.get()
            output_area.config(state=tk.NORMAL)
            output_area.insert(tk.END, f"\n>>> {command}\n")
            
            # Simple command handling
            if command.startswith('echo'):
                output_area.insert(tk.END, command[5:] + "\n")
            elif command == 'help':
                output_area.insert(tk.END, "Available commands:\n")
                output_area.insert(tk.END, "echo [text] - Repeats the text\n")
                output_area.insert(tk.END, "help - Show this help message\n")
                output_area.insert(tk.END, "date - Show current date and time\n")
            elif command == 'date':
                output_area.insert(tk.END, str(datetime.datetime.now()) + "\n")
            else:
                output_area.insert(tk.END, f"Command not recognized: {command}\n")
            
            output_area.config(state=tk.DISABLED)
            output_area.see(tk.END)
            input_area.delete(0, tk.END)

        input_area.bind('<Return>', execute_command)

    def save_file(self):
        """Save file dialog"""
        file_path = simpledialog.asksaveasfilename(defaultextension=".txt")
        if file_path:
            with open(file_path, 'w') as file:
                file.write(self.text_area.get('1.0', tk.END))

    def open_file(self):
        """Open file dialog"""
        file_path = simpledialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if file_path:
            with open(file_path, 'r') as file:
                content = file.read()
                self.text_area.delete('1.0', tk.END)
                self.text_area.insert('1.0', content)

def main():
    root = tk.Tk()
    os_app = SimpleOS(root)
    root.mainloop()

if __name__ == "__main__":
    main()