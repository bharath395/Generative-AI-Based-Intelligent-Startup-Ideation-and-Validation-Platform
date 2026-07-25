# API Documentation — Student Startup Ideation & Validation Platform

**Base URL**: `http://localhost:5000` (local) or `https://your-app.onrender.com` (production)

All API endpoints return JSON. Protected endpoints require Flask-Login session authentication.

---

## 1. Authentication APIs

### POST `/api/v1/register`
Create a new student account.

| Field | Type | Required | Description |
|---|---|---|---|
| name | string | ✅ | Full name |
| email | string | ✅ | Email address (unique) |
| password | string | ✅ | Password (min 6 chars) |
| department | string | ❌ | Academic department |
| skills | string | ❌ | Comma-separated technical skills |
| interest | string | ❌ | Domain interest area |

**Success Response** (201):
```json
{ "status": "success", "message": "User created successfully", "user_id": 1, "user": { ... } }
```

### POST `/api/v1/login`
Authenticate and create a session.

| Field | Type | Required |
|---|---|---|
| email | string | ✅ |
| password | string | ✅ |
| remember | boolean | ❌ |

**Success Response** (200):
```json
{ "status": "success", "message": "Logged in successfully", "user_id": 1 }
```

### POST `/api/v1/logout`
🔒 End current session.

### GET `/api/v1/profile`
🔒 Get authenticated user profile.

### PUT `/api/v1/profile`
🔒 Update profile fields (name, department, skills, interest).

---

## 2. AI Idea Generation APIs

### POST `/api/v1/generate-idea`
🔒 Run the full Multi-Agent AI pipeline.

| Field | Type | Required | Description |
|---|---|---|---|
| domain | string | ✅ | Target industry domain |
| skills | string | ✅ | Student technical skills |
| budget | string | ❌ | Initial budget (default: 50000) |
| interest | string | ❌ | Focus area |

**Success Response** (201):
```json
{
  "status": "success",
  "startup_id": 1,
  "startup_name": "Smart Agri AI Assistant",
  "problem": "...",
  "solution": "...",
  "technology": "...",
  "target_customer": "...",
  "innovation_score": 88.5
}
```

### GET `/api/v1/ideas`
🔒 List all startup projects for the current user.

---

## 3. Market Analysis API

### GET `/api/v1/market-analysis/<startup_id>`
🔒 Retrieve market size, CAGR, trend score, demand level.

---

## 4. Competitor Analysis API

### GET `/api/v1/competitors/<startup_id>`
🔒 Retrieve competitor comparison matrix data.

---

## 5. Validation Scoring APIs

### POST `/api/v1/validate`
🔒 Calculate validation score using weighted formula.

| Field | Type | Default |
|---|---|---|
| innovation | float | 90 |
| market | float | 85 |
| technology | float | 80 |
| business | float | 88 |

**Formula**: `Overall = (Innovation × 0.25) + (Market × 0.30) + (Tech × 0.25) + (Business × 0.20)`

### GET `/api/v1/validation/<startup_id>`
🔒 Retrieve saved validation result for a startup project.

---

## 6. Business Model Canvas API

### GET `/api/v1/business-model/<startup_id>`
🔒 Retrieve 9-block Business Model Canvas data.

---

## 7. Financial Analysis API

### GET `/api/v1/financial-analysis/<startup_id>`
🔒 Retrieve financial projections (costs, revenue, ROI, break-even).

---

## 8. Pitch Deck API

### GET `/api/v1/pitch/<startup_id>`
🔒 Generate investor pitch deck content.

---

## 9. Report APIs

### POST `/api/v1/generate-report`
🔒 Compile PDF startup intelligence report using ReportLab.

| Field | Type | Required |
|---|---|---|
| startup_id | integer | ❌ (uses latest project if omitted) |

### GET `/api/v1/download-report/<report_id>`
🔒 Download generated PDF report file.

---

## 10. AI Mentor Chat API

### POST `/api/v1/mentor-chat`
🔒 Send a message to the AI Startup Mentor with RAG context and conversation memory.

| Field | Type | Required |
|---|---|---|
| message | string | ✅ |

---

## 11. Dashboard API

### GET `/api/v1/dashboard`
🔒 Retrieve aggregated dashboard analytics (total ideas, average score, domain distribution).

---

## 12. Advanced Platform APIs

### GET `/api/v1/startup-history`
Protected. Retrieve the current user's generated ideas, validation results, reports, and mentor-chat memory.

### POST `/api/v1/idea-comparison`
Protected. Compare two or more startup ideas owned by the current user and return the strongest weighted score.

| Field | Type | Required |
|---|---|---|
| startup_ids | array[integer] | Yes |

### GET `/api/v1/recommendations`
Protected. Suggest three startup directions using student skills, interests, previous domains, and market-fit rules.

### GET `/api/v1/progress/<startup_id>`
Protected. Return project progress across idea generation, market analysis, validation, business plan, financial plan, and report generation.

### GET `/api/v1/notifications`
Protected. Return recent generated-idea, validation-updated, and report-ready notifications.

### GET `/api/v1/admin-dashboard`
Admin only. Return total users, total startup ideas, average validation score, popular domains, and report count.

---

## Error Response Format

All errors follow this structure:
```json
{ "status": "error", "error": "Description of the error", "status_code": 400 }
```

| Code | Meaning |
|---|---|
| 400 | Bad Request / Validation Error |
| 401 | Unauthorized / Not Logged In |
| 404 | Resource Not Found |
| 500 | Internal Server Error |
