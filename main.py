import customtkinter as ctk


class ShiftSchedulerGUI(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configure the appearance
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.title("Shift Schedule Manager")
        self.geometry("1300x800")


def main():
    app = ShiftSchedulerGUI()
    app.mainloop()


if __name__ == "__main__":
    main()
