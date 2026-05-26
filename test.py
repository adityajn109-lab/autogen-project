import os
from dotenv import load_dotenv
from openai import AzureOpenAI

# Load env variables
load_dotenv()

# Read values
api_key = os.getenv("AZURE_API_KEY")
endpoint = os.getenv("AZURE_ENDPOINT")
deployment = os.getenv("AZURE_DEPLOYMENT")
api_version = os.getenv("AZURE_API_VERSION")

# Debug check (optional)
# print("Using endpoint:", endpoint)
# print("Using deployment:", deployment)

# Create client
client = AzureOpenAI(
    api_key=api_key,
    api_version=api_version,
    azure_endpoint=endpoint
)

# Call model
response = client.responses.create(
    model=deployment,
    input="Give me 2 lines about AutoGen"
)

# Print output
print(response.output[0].content[0].text)