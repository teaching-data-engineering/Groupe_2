from google.oauth2 import service_account
import pandas_gbq

credentials = service_account.Credentials.from_service_account_file(
    'sa-key-group-2.json',
)
df = pandas_gbq.read_gbq("data_NY.csv", project_id="ai-technologies-ur2", credentials=credentials)