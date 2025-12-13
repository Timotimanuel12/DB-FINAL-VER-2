import tkinter as tk

class AdminScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        # Simple Styling
        self.configure(bg="white")
        
        # Title
        tk.Label(self, text="Admin Portal", font=("Arial", 24, "bold"), bg="white").pack(pady=50)

        # Back Button
        # We call self.go_back instead of a lambda to handle the import cleanly
        tk.Button(self, text="Back to Login", font=("Arial", 12),
                  command=self.go_back).pack(pady=20)

    def go_back(self):
        # --- LOCAL IMPORT TO PREVENT CIRCULAR ERROR ---
        from login_view import LoginScreen 
        self.controller.show_view(LoginScreen)