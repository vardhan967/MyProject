# Seat Booking - React Frontend

This is the modern frontend for the Seat Booking application, built with React, Vite, and TypeScript. It provides a dynamic and responsive user interface for students and administrators to interact with the seat reservation system.

The live application is deployed and accessible here: **[Add Your Deployed Frontend Link Here]**

## Features

- **Modern UI/UX:** A fast, responsive, and visually appealing interface built with Tailwind CSS.
- **Role-Based Views:** Custom dashboards and actions tailored for Students and Admins.
- **Live Status Updates:** Real-time reflection of seat status (Available, Pending, Reserved).
- **Component-Based Architecture:** Clean and maintainable code structure using React functional components and hooks.
- **Global State Management:** Uses React Context API for managing authentication and seat data across the application.

---

## Tech Stack

- **Framework:** React
- **Build Tool:** Vite
- **Language:** TypeScript
- **Styling:** Tailwind CSS & Shadcn/UI
- **Data Fetching:** Axios
- **Routing:** React Router DOM

---

## Getting Started

To run this project locally, you must have the [Django backend](https://github.com/your-username/seat-booking-django-backend) running simultaneously.

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/seat-booking-react-frontend.git
    cd seat-booking-react-frontend
    ```

2.  **Install dependencies:**
    This will install all required packages from `package.json`.
    ```bash
    npm install
    ```

3.  **Configure the backend proxy:**
    The `vite.config.ts` file is pre-configured to proxy API requests starting with `/api` to the local Django server at `http://127.0.0.1:8000`. Ensure your Django backend is running on this address.

4.  **Run the development server:**
    The application will be available at `http://localhost:5173`.
    ```bash
    npm run dev
    ```

---

## Project Structure

- `src/`: Contains all the application source code.
  - `components/`: Reusable UI components (e.g., `Seat`, `Navbar`).
  - `pages/`: Top-level components for each route (e.g., `LoginPage`, `SeatDashboardPage`).
  - `contexts/`: React Context providers for global state (`AuthContext`, `SeatContext`).
  - `utils/`: Utility functions, including the configured Axios instance.
- `vite.config.ts`: Configuration for the Vite development server and build process.
- `tailwind.config.ts`: Configuration for the Tailwind CSS framework.
- `package.json`: Lists all project dependencies and scripts.
