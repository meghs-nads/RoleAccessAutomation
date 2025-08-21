
---

#  AI Ticket Automation

This project automates the process of **extracting role assignment requests from Gmail** and updating them in a **PostgreSQL database** via a Flask API.
It uses **Google Cloud Workflows**, **Secret Manager**, and **Cohere AI** for intelligent data extraction.

---

##  Features

* Fetches Gmail messages with subject starting with `Ticket`
* Extracts **employee\_id, role\_name, and application\_name** using Cohere AI
* Validates and forwards extracted data to a Flask API
* Flask API assigns roles by calling a PostgreSQL stored procedure
* Secure handling of secrets using **Google Secret Manager**
* Exposed for testing via **ngrok**

---

##  Architecture

```
Gmail --> Google Workflow --> Cohere AI --> Flask API --> PostgreSQL
```

* **Workflow**: Orchestrates fetching Gmail, parsing with Cohere, and calling the API
* **Flask API (`/assign_role`)**: Accepts extracted data and executes `assign_role_to_employee` in PostgreSQL
* **PostgreSQL**: Stores employee-role assignments
* **ngrok**: Tunnels Flask server for external access

---

##  Project Structure

```
AITicketAutomation/
│
├── app2.py              # Flask backend API
├── workflow.yaml        # Google Cloud Workflow definition
├── requirements.txt     # Python dependencies
├── README.md            # Documentation
└── .gitignore           # Ignore unnecessary files
```

---

##  Setup & Installation

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR-USERNAME/AITicketAutomation.git
cd AITicketAutomation
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run PostgreSQL Locally

* Ensure PostgreSQL is running on `localhost:5432`
* Create databases: `CBS_Dev`, `WorkAtRisk_Dev`
* Implement stored procedure:

  ```sql
  CREATE OR REPLACE FUNCTION assign_role_to_employee(emp_id INT, role_name TEXT)
  RETURNS TEXT AS $$
  BEGIN
    -- Custom logic here
    RETURN 'Role assigned successfully';
  END;
  $$ LANGUAGE plpgsql;
  ```

### 5. Run Flask API

```bash
python app2.py
```

By default, it runs on `http://127.0.0.1:5000`

### 6. Expose via ngrok

```bash
ngrok http 5000
```

Use the generated URL (e.g., `https://xxxx.ngrok-free.app/assign_role`) in your Workflow.

---

##  Secret Management

Secrets like `gmail-client-id`, `gmail-client-secret`, `refresh-token`, and `cohere-api-key` are stored securely in **Google Secret Manager** and accessed inside the workflow.

---

##  Testing

### Test API with curl

```bash
curl -X POST https://xxxx.ngrok-free.app/assign_role \
  -H "Content-Type: application/json" \
  -d '{"AppName": "CBS_Dev", "EmployeeId": 123, "RoleName": "Manager"}'
```

Expected Response:

```json
{"result": "Role assigned successfully"}
```

### Trigger Workflow

Run workflow → Gmail → Cohere → API → PostgreSQL.

---

##  Future Improvements

* Add support for more applications (expand `db_map`)
* Improve Cohere prompt to return exact DB keys
* Add authentication layer to the Flask API
* Dockerize for easier deployment

---

##  Contributing

Feel free to fork, open issues, and submit pull requests.

---

##  License

MIT License

---

