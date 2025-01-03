import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
from calendar import monthrange
from datetime import datetime
import database.queries as db

root = ctk.CTk()
ctk.set_appearance_mode('dark')
ctk.set_default_color_theme('dark-blue')

root.title('Shift Schedule Manager')
root.geometry('1300x800')

# Treeview Customization (theme colors are selected)
bg_color = root._apply_appearance_mode(ctk.ThemeManager.theme["CTkFrame"]["fg_color"])
text_color = root._apply_appearance_mode(ctk.ThemeManager.theme["CTkLabel"]["text_color"])
selected_color = root._apply_appearance_mode(ctk.ThemeManager.theme["CTkButton"]["fg_color"])
hover_color = '#14375e'

tree_style = ttk.Style()
tree_style.theme_use('default')
tree_style.configure("Treeview",
                     background=bg_color,
                     foreground=text_color,
                     fieldbackground=bg_color,
                     borderwidth=2,
                     )
tree_style.map('Treeview', background=[('selected', '#325882')], foreground=[('selected', text_color)])
# Configure Treeview Heading style
tree_style.configure("Treeview.Heading", background=selected_color, foreground=text_color, borderwidth=1)
tree_style.map("Treeview.Heading", background=[('active', hover_color)])
# Toggles the main controls frame on and off
def toggle_frame(frame=None):
    """
    :param frame: is passed from each function that creates new controls frame.
    The default value is None for when the main controls frame is called for the first time
    from each new controls frame
    """
    if bool(main_controls_frame.winfo_ismapped()):
        main_controls_frame.pack_forget()
    else:
        frame.pack_forget()
        main_controls_frame.pack(side='left', fill='y', padx=10, pady=10)


def generate_schedule_controls():
    toggle_frame()

    def generate_schedule():
        """
            Function to generate the automatically generates schedule
            for the chosen year and month starting from the chosen team
        """
        year = int(choose_year.get())
        month = int(choose_month.get())
        current_team = choose_team.get()

        db.generate_schedule(year, month, current_team)

    generate_controls_frame = ctk.CTkFrame(root)
    generate_controls_frame.pack(side='left', fill='y', padx=10, pady=10)

    back_button = ctk.CTkButton(generate_controls_frame,
                                text='⬅ Назад',
                                font=('Helvetica', 15),
                                width=10,
                                fg_color='transparent',
                                command=lambda: toggle_frame(generate_controls_frame))
    back_button.pack(pady=10, padx=20, anchor='w')

    choose_year_label = ctk.CTkLabel(generate_controls_frame, text='Изберете година')
    choose_year_label.pack(pady=(20, 0))
    choose_year = ctk.CTkComboBox(generate_controls_frame, values=['2024', '2025', '2026'])
    choose_year.pack(pady=10)

    choose_month_label = ctk.CTkLabel(generate_controls_frame, text='Изберете месец')
    choose_month_label.pack(pady=(20, 0))
    choose_month = ctk.CTkComboBox(generate_controls_frame, values=['1', '2', '3', '4', '5'])
    choose_month.pack(pady=10)

    choose_team_label = ctk.CTkLabel(generate_controls_frame, text='Изберете смяна')
    choose_team_label.pack(pady=(20, 0))
    choose_team = ctk.CTkComboBox(generate_controls_frame, values=['А', 'Б', 'В', 'Г'])
    choose_team.pack(pady=10)

    generate_button = ctk.CTkButton(generate_controls_frame, text='Generate', command=generate_schedule)
    generate_button.pack(pady=10, padx=20)


def show_collective_schedule_controls():
    toggle_frame()

    show_collective_schedule_frame = ctk.CTkFrame(root)
    show_collective_schedule_frame.pack(side='left', fill='y', padx=10, pady=10)

    back_button = ctk.CTkButton(show_collective_schedule_frame,
                                text='⬅ Назад',
                                font=('Helvetica', 15),
                                width=10,
                                fg_color='transparent',
                                command=lambda: toggle_frame(show_collective_schedule_frame))
    back_button.pack(pady=10, padx=20, anchor='w')

    choose_year_label = ctk.CTkLabel(show_collective_schedule_frame, text='Изберете година')
    choose_year_label.pack(pady=(20, 0))
    choose_year = ctk.CTkComboBox(show_collective_schedule_frame, values=['2024', '2025', '2026'])
    choose_year.pack(pady=10)

    choose_month_label = ctk.CTkLabel(show_collective_schedule_frame, text='Изберете месец')
    choose_month_label.pack(pady=(20, 0))
    choose_month = ctk.CTkComboBox(show_collective_schedule_frame, values=['1', '2', '3', '4', '5'])
    choose_month.pack(pady=10)

    show_schedule_button = ctk.CTkButton(show_collective_schedule_frame, text='Покажи график', command=create_treeview)
    show_schedule_button.pack(pady=10, padx=20)


def create_treeview():
    main_window_frame = ctk.CTkFrame(root)
    main_window_frame.pack(side='right', fill='both', padx=10, pady=10)

    # Define the Treeview widget
    tree = ttk.Treeview(main_window_frame, show='headings')

    def create_headings(year, month):
        """Dynamically create headings based on the number of days in the given month."""
        # Clear existing headings and columns
        tree['columns'] = []  # Reset columns
        for col in tree['columns']:
            tree.heading(col, text="")  # Clear headings

        # Get the number of days in the month
        num_days = monthrange(year, month)[1]

        # Update columns and headings
        tree['columns'] = [f'{datetime(year, month, i).strftime("%d.%m.%Y")}' for i in range(1, num_days + 1)]
        for day in range(1, num_days + 1):
            date = datetime(year, month, day).strftime('%d.%m.%Y')
            weekday = datetime(year, month, day).strftime('%A')

            tree.heading(f'{date}', text=f'{date}\n{weekday}')
            tree.column(f'{datetime(year, month, day).strftime("%d.%m.%Y")}', width=70, anchor='center')

    def update_rows(filtered_dates, num_days):
        """Update the rows in the Treeview with the filtered data."""
        # Clear existing rows
        for row in tree.get_children():
            tree.delete(row)

        # Prepare data for insertion
        rows = [''] * num_days
        for date in filtered_dates:
            day = int(date.split('-')[2])  # Extract the day from the date string
            rows[day - 1] = datetime.strptime(date, '%Y-%m-%d').strftime('%A')

        # Insert a single row with dates
        tree.insert('', tk.END, values=rows)

    def fetch_data(year, month):
        """Fetch data from the database and update the Treeview."""
        # Call the database function to fetch rows
        fetched_rows = db.fetch_dates()  # Returns all dates for the year

        # Filter dates for the specified month
        filtered_dates = [
            date[0] for date in fetched_rows  # Unpack tuple
            if datetime.strptime(date[0], '%Y-%m-%d').month == month and
               datetime.strptime(date[0], '%Y-%m-%d').year == year
        ]

        # Create the headings dynamically based on the selected year and month
        create_headings(year, month)

        # Update the Treeview rows with filtered data
        num_days = monthrange(year, month)[1]
        update_rows(filtered_dates, num_days)

    # Example: Fetch data for January 2024
    fetch_data(2024, 1)

    tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)




main_controls_frame = ctk.CTkFrame(root)
main_controls_frame.pack(side='left', fill='y', padx=10, pady=10)

generate_schedule_button = ctk.CTkButton(main_controls_frame,
                                         text='Генерирай график',
                                         command=generate_schedule_controls)
generate_schedule_button.pack(pady=10, padx=20)

show_collective_schedule_button = ctk.CTkButton(main_controls_frame,
                                                text='Покажи общ график',
                                                command=show_collective_schedule_controls)
show_collective_schedule_button.pack(pady=10, padx=20)


root.mainloop()
