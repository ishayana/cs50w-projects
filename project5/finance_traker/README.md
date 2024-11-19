
# Personal Finance Tracker

## Overview
Personal Finance Tracker is a dynamic web application that helps users manage and track their personal finances. Users can create budgets for different categories, record income and expenses, and monitor their financial status in real-time. The application allows for seamless interaction without the need for page reloads, offering a smooth and efficient experience.

---

## Distinctiveness and Complexity
This project stands out by offering an all-in-one user experience where all actions—creating budgets, adding transactions, editing or deleting them, and tracking financial summaries—occur on a single URL. The application dynamically loads content, making interactions smooth without requiring full-page reloads, which sets it apart from typical multi-page applications.

The complexity of this project lies in how it manages relationships between users, budgets, categories, and transactions. A major challenge was ensuring that each transaction correctly updates the corresponding budget’s `current_amount` based on whether the transaction was income or an expense. Maintaining data consistency, especially with real-time updates, was a critical part of the development process.

In addition, the project implements real-time financial data updates. As users add or remove transactions, the budget amounts, as well as total income and expenses, are recalculated and updated instantly. This functionality provides users with immediate feedback on their financial status, contributing to a more dynamic and interactive experience.

Handling EventListeners with Dynamic Content: A significant challenge I faced was ensuring that JavaScript `EventListeners` attached correctly when dynamically loading HTML content. Since the page doesn’t refresh, event listeners often didn’t work as expected when new content was loaded. This required careful reinitialization of JavaScript functions and listeners after each dynamic load. Through thorough research and testing, I was able to solve this issue by properly delegating event listeners and ensuring that they were consistently applied to dynamically added elements, allowing the app to function smoothly.

Data Integrity and Real-Time Calculations: The backend ensures that the financial data remains consistent across multiple models (e.g., Budgets and Transactions). When a user updates or deletes a transaction, the system immediately recalculates the budget amounts and displays the updated information to the user.

Charts and Visual Representations: A key feature of the project is the use of visual aids like charts to help users understand their financial data. These charts, which are generated dynamically based on the user's input, provide a graphical summary of income, expenses, and budget status. The integration of real-time updates with charting libraries adds another layer of complexity, as changes in the data need to reflect instantly in the visual elements.

SPA Navigation and Form Handling: The single-page application design ensures that users can perform all actions within the same interface without refreshing the page. Dynamic form submissions (for both creating and updating transactions) are handled via AJAX requests, which load content into specific page sections. This setup allows the app to provide a modern, responsive, and interactive user experience.

---

## File Overview

- `models.py`: Defines the data models (`Category`, `Budget`, and `Transaction`), managing relationships between users and their financial data.
- `views.py`: Handles the backend logic for creating, updating, and deleting budgets and transactions, as well as returning JSON responses for dynamic interactions.
- `forms.py`: Contains the form classes for validating user inputs.
- `urls.py`: Maps URLs to the corresponding views.
- `templates/`: Contains the HTML templates used to render the user interface.
- `static/`: Houses the static assets like CSS and JavaScript, including scripts for dynamic page interactions.
- `requirements.txt`: Lists the Python packages required to run the project.

---

## How to Run the Application

1. Clone the repository:
   ```bash
   git clone https://github.com/me50/ishayana/blob/web50/projects/2020/x/capstone
   ```

2. Navigate to the project directory:
   ```bash
   cd finance_traker
   ```

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the database make migration files:
   ```bash
   python manage.py makemigrations
   ```

5. Run the database migrations:
   ```bash
   python manage.py migrate
   ```

6. Start the development server:
   ```bash
   python manage.py runserver
   ```

7. Open your browser and go to:
   ```
   http://127.0.0.1:8000
   ```

---

