from fastapi import FastAPI, Body
from fastapi.middleware.cors import CORSMiddleware  # Import CORS middleware
from pydantic import BaseModel
from openai import OpenAI

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

# Define a Pydantic model for the request body
class TreatmentRequest(BaseModel):
    treatment: str
    condition: str

@app.post("/diffbot")
def read_item(request: TreatmentRequest):
    treatment = request.treatment
    condition = request.condition

    treatment_and_condition = f"{treatment} for {condition}"

    base_prompt = """
    I am going to ask you about whether a certain treatment or medication is the best choice for a specific condition. I want you to give the opinion in the context of different individual jurisdictions which may have different opinions and justifications. give the opinions and justifications from medical associations in the United States, United Kingdom, Australia, Ireland and Canada. If it is not the preferred treatment, state what is the preferred treatment.
    I want you to display it in ery plain text. No higlighting.
    """
    conversation = [{'role': "system", 'content': base_prompt}]
    conversation.append({'role': 'user', 'content': treatment_and_condition})

    client = OpenAI(
        base_url="https://llm.diffbot.com/rag/v1",
        api_key="your-api-key"
    )

    completion = client.chat.completions.create(
        model="diffbot-small-xl",
        temperature=0,
        messages=conversation
    )

    return {"response": completion.choices[0].message.content}
