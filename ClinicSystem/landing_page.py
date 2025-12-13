import tkinter as tk
from login_view import LoginScreen  # Ensure this import matches your file name

class ClinicLandingPage(tk.Frame):  # <--- MUST Inherit from tk.Frame
    def __init__(self, parent, controller): # <--- MUST accept parent and controller
        super().__init__(parent)
        self.controller = controller
        self.configure(bg="#2b2b2b")

        # --- CONFIGURATION ---
        self.primary_color = "#3a3a3a"
        self.accent_color = "#4a90e2"
        self.text_color = "#ffffff"

        # --- NAVBAR ---
        self.create_navbar()

        # --- MAIN CONTENT AREA ---
        self.content_frame = tk.Frame(self, bg="#2b2b2b")
        self.content_frame.pack(fill="both", expand=True, padx=50, pady=50)

        # Show Home page by default
        self.show_home()

    def create_navbar(self):
        nav_frame = tk.Frame(self, bg=self.primary_color, height=60)
        nav_frame.pack(side="top", fill="x")

        # Logo
        logo_label = tk.Label(nav_frame, text="🏥  MediCare Clinic", bg=self.primary_color, 
                              fg=self.text_color, font=("Arial", 16, "bold"))
        logo_label.pack(side="left", padx=20)

        # Menu Buttons
        menu_items = ["Home", "About Us", "Services", "Contact"]
        for item in menu_items:
            btn = tk.Button(nav_frame, text=item, bg=self.primary_color, fg=self.text_color,
                            activebackground=self.primary_color, activeforeground=self.accent_color,
                            bd=0, font=("Arial", 12), cursor="hand2",
                            command=lambda i=item: self.navigate(i))
            btn.pack(side="left", padx=15)

        # --- LOGIN BUTTON ---
        # This uses the controller to switch back to the LoginScreen
        login_btn = tk.Button(nav_frame, text="Login Portal", bg=self.accent_color, fg="white",
                              font=("Arial", 12, "bold"), bd=0, padx=20, pady=5, cursor="hand2",
                              command=lambda: self.controller.show_view(LoginScreen))
        login_btn.pack(side="right", padx=20, pady=10)

    def navigate(self, page_name):
        # Clear the content frame
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        if page_name == "Home": self.show_home()
        elif page_name == "About Us": self.show_about()
        elif page_name == "Services": self.show_services()
        elif page_name == "Contact": self.show_contact()

    def show_home(self):
        tk.Label(self.content_frame, text="Welcome to MediCare", font=("Helvetica", 32, "bold"), bg="#2b2b2b", fg="white").pack(pady=(50, 20))
        tk.Label(self.content_frame, text="Advanced Healthcare Management.", font=("Helvetica", 16), bg="#2b2b2b", fg="#cccccc").pack(pady=10)

    def show_about(self):
        tk.Label(self.content_frame, text="About Us", font=("Helvetica", 28, "bold"), bg="#2b2b2b", fg="white").pack(pady=20)
        tk.Label(self.content_frame, text="We provide top-tier medical services.", font=("Helvetica", 14), bg="#2b2b2b", fg="#cccccc").pack(pady=10)

    def show_services(self):
        tk.Label(self.content_frame, text="Our Services", font=("Helvetica", 28, "bold"), bg="#2b2b2b", fg="white").pack(pady=20)
        tk.Label(self.content_frame, text="• General Checkups\n• Cardiology", font=("Helvetica", 16), bg="#2b2b2b", fg="#cccccc").pack(pady=10)

    def show_contact(self):
        tk.Label(self.content_frame, text="Contact Us", font=("Helvetica", 28, "bold"), bg="#2b2b2b", fg="white").pack(pady=20)
        tk.Label(self.content_frame, text="📞 +1 234 567 890", font=("Helvetica", 14), bg="#2b2b2b", fg="#cccccc").pack(pady=10)