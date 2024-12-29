import customtkinter as ctk
import database.queries as db

root = ctk.CTk()
ctk.set_appearance_mode('dark')
ctk.set_default_color_theme('dark-blue')

root.title('Shift Schedule Manager')
root.geometry('1300x800')

control_frame = ctk.CTkFrame(root)
control_frame.pack(side='left', fill='y', padx=10, pady=10)


def generate_schedule():
    year = int(choose_year.get())
    month = int(choose_month.get())
    current_team = choose_team.get()

    db.generate_schedule(year, month, current_team)


choose_year_label = ctk.CTkLabel(control_frame, text='Изберете година')
choose_year_label.pack(pady=(20, 0))
choose_year = ctk.CTkComboBox(control_frame, values=['2024', '2025', '2026'])
choose_year.pack(pady=10)

choose_month_label = ctk.CTkLabel(control_frame, text='Изберете месец')
choose_month_label.pack(pady=(20, 0))
choose_month = ctk.CTkComboBox(control_frame, values=['1', '2', '3', '4', '5'])
choose_month.pack(pady=10)

choose_team_label = ctk.CTkLabel(control_frame, text='Изберете смяна')
choose_team_label.pack(pady=(20, 0))
choose_team = ctk.CTkComboBox(control_frame, values=['А', 'Б', 'В', 'Г'])
choose_team.pack(pady=10)

generate_button = ctk.CTkButton(control_frame, text='Generate', command=generate_schedule)
generate_button.pack(pady=10)

root.mainloop()
