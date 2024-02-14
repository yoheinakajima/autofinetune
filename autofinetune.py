from openai import OpenAI
import together
import json
import os

OpenAI.apikey = os.environ['OPENAI_API_KEY']
together.api_key = os.environ['TOGETHER_API_KEY']

client = OpenAI()

# Example dynamic content for the objective, user input rules, and assistant response rules
suffix = "autofinetune" #suffix for model name on together AI
objective = f"to generate a model that labels messages as spam or not spam."
user_input_rules = f"Make it a random title of an email."
assistant_response_rules = f"Only responds with 'spam' or 'not spam'."


def generate_conversations():
  conversations = []  # Initialize the main conversations list
  target_conversations = 100  # Target number of conversation entries
  conversation_batch_size = 5  # Batches of conversations to generate at a time
  generated_count = 0  # Keep track of how many conversations have been generated

  while generated_count < target_conversations:
      response = client.chat.completions.create(
          model="gpt-4-turbo-preview",
          temperature = 1,
          response_format={"type": "json_object"},  # Enable JSON mode
          messages=[
              {
                  "role": "system",
                  "content": f"""You are a helpful assistant designed to output conversations in JSON array format. Generate an array of {conversation_batch_size} elements, each being a conversation entry with a user input and your response, with the keys 'user' and 'assistant', one message each per conversation, with {conversation_batch_size} of these conversations in the array you produce.The purpose of this is to fine-tune a model based for the user using this data, so tailor the questions and answers to match the needs based on the user's input. The array should start with conversations as the top level with an array of conversations.
                  """
              },
              {
                  "role": "user",
                  "content": f"""Start generating the conversation array.
                  Purpose of the conversation data is to fine tune a model.
                  The obective of the model we are fine-tuning is: {objective}.
                  User input rules: {user_input_rules}.
                  Assistant response rules: {assistant_response_rules}.
                  """
              }
          ]
      )

      generated_content = response.choices[0].message.content
      print(generated_content)

      try:
        generated_content = json.loads(response.choices[0].message.content)
        if "conversations" in generated_content:
            for conv in generated_content["conversations"]:
                if "user" in conv and "assistant" in conv:
                    conversations.append(conv)
                    generated_count += 1 
                else:
                    print("Skipping a conversation entry due to missing 'user' or 'assistant' key.")
      except json.JSONDecodeError:
        print("Error decoding JSON from response")

      print(f"Generated {generated_count} conversations so far.")

  return json.dumps({"conversations": conversations}) 


def prepare_data_for_together(generated_content):
  conversations_json = json.loads(generated_content)
  together_data = []
  for conv in conversations_json["conversations"]:
      
      formatted_entry = {
          "text": f'<s>[INST] {conv["user"]} [/INST] {conv["assistant"]} </s>'
      }
      together_data.append(formatted_entry)
  
  with open("conversations_dataset.jsonl", 'w') as outfile:
      for item in together_data:
          outfile.write(json.dumps(item) + '\n') # Save to a JSONL file
  
  return "conversations_dataset.jsonl"


def upload_and_fine_tune(file_name):
  file_id = together.Files.upload(file=file_name)["id"]

  fine_tune_response = together.Finetune.create(
      training_file=file_id,
      model='togethercomputer/llama-2-7b-chat',
      n_epochs=3,
      n_checkpoints=1,
      batch_size=4,
      learning_rate=1e-5,
      suffix=suffix,
      # wandb_api_key='YOUR_WANDB_API_KEY',
  )
  print("Fine-tuning started:", fine_tune_response)
  print("Check your results/status at https://api.together.xyz/playground/jobs")


def main():
  print("Generating conversation data...")
  generated_content = generate_conversations()

  print("Preparing data for Together.ai...")
  file_name = prepare_data_for_together(generated_content)

  print("Uploading and starting fine-tuning...")
  upload_and_fine_tune(file_name)

if __name__ == "__main__":
  main()
