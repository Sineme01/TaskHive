# API Documentation

## General Rules for All Endpoints

Unless stated otherwise, the following rules apply to all endpoints:

- Access token should be passed via the `Authorization: Bearer <token>` header.
- All endpoints return `HTTP 200 OK` on success.
- Errors are returned as text messages with appropriate status codes:
  - `4xx` indicates client-side errors such as bad requests or unauthorized access.
  - `5xx` indicates server-side issues.

## Submit a New Computation Job

**Description:**  
Allows an authenticated user to submit a new background job for numerical computations such as sum of squares or cubes.

| Method | Endpoint | Auth Required |
|--------|----------|---------------|
| POST   | /jobs    | Yes           |

### Parameters
- Query: `operation` (e.g., `square_sum` or `cube_sum`)
- Body: JSON list of integers

### Example Request

```bash
curl -X POST "http://localhost:8000/jobs?operation=square_sum"      -H "Authorization: Bearer <token>"      -H "Content-Type: application/json"      -d '[1, 2, 3]'
```

### Example Response

```json
{
  "job_id": 1,
  "status": "IN_PROGRESS"
}
```

## Check Job Status

**Description:**  
Returns the current status of a background job using the job ID.

| Method | Endpoint              | Auth Required |
|--------|-----------------------|---------------|
| GET    | /jobs/{job_id}/status | Yes           |

### Example Request

```bash
curl -X GET http://localhost:8000/jobs/1/status      -H "Authorization: Bearer <token>"
```

### Example Response

```json
{
  "status": "IN_PROGRESS"
}
```

## Retrieve Completed Job Result

**Description:**  
Fetches the result of a completed job. If the job is still in progress, a relevant message is returned.

| Method | Endpoint              | Auth Required |
|--------|-----------------------|---------------|
| GET    | /jobs/{job_id}/result | Yes           |

### Example Request

```bash
curl -X GET http://localhost:8000/jobs/1/result      -H "Authorization: Bearer <token>"
```

### Example Response (Job Complete)

```json
{
  "result": 14
}
```

### Example Response (Job In Progress)

```json
{
  "message": "Still processing..."
}
```

## Job Expiration and Cleanup

- A daily Celery Beat task deletes jobs older than 24 hours to maintain performance and storage efficiency.
- This process runs automatically in the background.

## Rate Limiting

- Rate limiting is enforced using `slowapi`.
- For example: the `/register` endpoint is limited to 5 requests per minute per client.
- Exceeding the rate limit returns a `429 Too Many Requests` response.

```json
{
  "detail": "Rate limit exceeded"
}
```