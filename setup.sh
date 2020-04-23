#!/bin/sh

# export AUTH0_DOMAIN='testfsnd.auth0.com'
# export ALGORITHMS=['RS256']
# export API_AUDIENCE='cap'
# export CLIENT_ID='29v4Ks9deL4ijNb06BvFHmZdk4WXeFtz'
# export producer_token=eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlFrWkdSREUwTlVZNFJEUkNOVU13T1RSRFJUaEJOalJCTXpsQlJqVTNNVGhCTjBVelJVWkNPUSJ9.eyJpc3MiOiJodHRwczovL3Rlc3Rmc25kLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZTc0YzIyNGZmNzliYzBjNjUxZTIwMzMiLCJhdWQiOiJjYXAiLCJpYXQiOjE1ODQ5OTU0MzYsImV4cCI6MTU4NTA4MTgzNiwiYXpwIjoiMjl2NEtzOWRlTDRpak5iMDZCdkZIbVpkazRXWGVGdHoiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTpBY3RvcnMiLCJkZWxldGU6TW92aWVzIiwiZ2V0OkFjdG9ycyIsImdldDpNb3ZpZXMiLCJwYXRjaDpBY3RvcnMiLCJwYXRjaDpNb3ZpZXMiLCJwb3N0OkFjdG9ycyIsInBvc3Q6TW92aWVzIl19.me_VF-vIbYK3EBC_neJBKHaLJGBh4eQnKq7bCt62tIs1jZ2SeaiGVrKcjgMLQ0gT2eRS8tBfx9hkMPQkHudurn80G_whWtOcW4qjNs_DRdyVifqL0ANcBO0iYYgPuKdvxrwUm1sILpWY1rLJK-5FXdhZ42kiXbhsfM77KC7YTuEPmIXxK4Qfd5uHiBd-bmsiRV7HevQFSgv8lvWZ2jRcsQj9ceeC91puz1u580MBg3Olu-N0UCi7mnQyIIbxXjPcFtmFbdJA0myjRa6lUFyHnoZN9uFYjfI2aGc4hAvYuM5KpIHRE0Rw8RxH1kOCK18b1Xtth54kmbWcwNVcoXj3OA

# export director_token=eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlFrWkdSREUwTlVZNFJEUkNOVU13T1RSRFJUaEJOalJCTXpsQlJqVTNNVGhCTjBVelJVWkNPUSJ9.eyJpc3MiOiJodHRwczovL3Rlc3Rmc25kLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZTc0YzhiNjY3MzFkYzBjNjc1MGU4ZjkiLCJhdWQiOiJjYXAiLCJpYXQiOjE1ODQ5OTU3MzQsImV4cCI6MTU4NTA4MjEzNCwiYXpwIjoiMjl2NEtzOWRlTDRpak5iMDZCdkZIbVpkazRXWGVGdHoiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTpBY3RvcnMiLCJnZXQ6QWN0b3JzIiwiZ2V0Ok1vdmllcyIsInBhdGNoOkFjdG9ycyIsInBhdGNoOk1vdmllcyIsInBvc3Q6QWN0b3JzIl19.tmWxNIsZhR5NnHkM6t9xdKloFMutguDbkHpKLmLxFEt7oNRKdGb-Haol7OfnJzhfwdCUVucK4QxzoFutEXTBYABVMjfkMXhmwOlJPrbGp0fyyneI1_BpAK4VoihxD8iATZzBwoQOR7PBed9k4iM7phtmJYAA7OR2-72R_-0Fe29yUzQWdClPjoFIC_eVr_uLlHEqWDeBM6T8r-PTOPs8Hfs1_cA1yQXsCB08JipsKZ5pBB8AZEMIjkD1iymjdhIoLsXR2qDLuZU4iF6hveEJ1wdUZHg5JX5zU4jbiNGQcglup271P3QDIZ4RJzySukf4vA0h4ZpGkd1ypA83YBX9HA

# export assistant_token=eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlFrWkdSREUwTlVZNFJEUkNOVU13T1RSRFJUaEJOalJCTXpsQlJqVTNNVGhCTjBVelJVWkNPUSJ9.eyJpc3MiOiJodHRwczovL3Rlc3Rmc25kLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZTc0Yzk3N2ZmNzliYzBjNjUxZTM4YzAiLCJhdWQiOiJjYXAiLCJpYXQiOjE1ODQ5OTU5NTUsImV4cCI6MTU4NTA4MjM1NSwiYXpwIjoiMjl2NEtzOWRlTDRpak5iMDZCdkZIbVpkazRXWGVGdHoiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImdldDpBY3RvcnMiLCJnZXQ6TW92aWVzIl19.oOIK6vRSLVCJksPH8_QSHgEGLBNqwi0grn7rmlvpCmKjBzhlIWuYYHttJQ5CNdeVXemw-fzphh8loVEpAPXykefvcFybo66R81Eu7Dc_SEBIidXkdVpYT3KVfZGEgYuEH8E-ZWokyAmrKtChCEOWD4ozNazDXAynvuhWHjFwKU4NIo-qdGqw-nm5kS0PRySfwxkQPA3yj55roQZcpxV8SF__IDY_HfnpJxyJiGUIyRHcZ8NOhJHHltGKLy8j16_79nLHshA2Csk1-9KJsabomfqK0ntlIjoNgaLeqsMR6ZoxoOxTNzyEQXpRSiHo2dE4rJ78VtpdNNiN1naJILeKBQ
