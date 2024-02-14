# autofinetune

Welcome to `autofinetune`, a project by [yoheinakajima](https://twitter.com/yoheinakajima) on GitHub designed to streamline the process of generating conversation data for fine-tuning AI models. This tool leverages OpenAI's GPT models for conversation generation and Together AI's platform for fine-tuning, aiming to create models tailored for specific tasks or behaviors.

## Overview

`autofinetune` is a Python-based tool that automates the generation of conversational datasets and uses them for model fine-tuning. It's particularly useful for projects where custom conversation patterns and responses are needed, such as creating an AI that can classify messages or respond in a specific manner.

### How It Works

1. **Conversation Generation**: The script generates a specified number of conversational entries using OpenAI's Chat Completion API. Each entry consists of a user input and an assistant's response, based on predefined objectives and rules.
   
2. **Data Preparation**: The generated conversations are formatted into a structure compatible with Together AI's specifications for fine-tuning datasets.

3. **Fine-Tuning**: The prepared dataset is uploaded to Together AI, and a fine-tuning job is initiated with specified parameters.

### Features

- Dynamic content generation based on user-defined objectives and rules.
- JSON array output for easy parsing and manipulation.
- Integration with Together AI for seamless model fine-tuning.

## Usage

### Prerequisites

- Python 3.6 or later.
- OpenAI API key: Obtain from [OpenAI](https://openai.com/api/).
- Together AI API key: Sign up at [Together AI](https://together.xyz/) and obtain your API key.

### Installation

1. Clone the `autofinetune` repository from GitHub:

   ```
   git clone https://github.com/yoheinakajima/autofinetune.git
   ```

2. Install the required Python packages:

   ```
   pip install openai together
   ```

3. Set your API keys as environment variables:

   ```sh
   export OPENAI_API_KEY='your_openai_api_key_here'
   export TOGETHER_API_KEY='your_together_api_key_here'
   ```

### Running autofinetune

Navigate to the `autofinetune` directory and run the script:

```sh
python autofinetune.py
```

### Customization

You can customize the script by modifying the following variables at the beginning of the `autofinetune.py` file:

- `objective`: Defines the goal of the model you're fine-tuning (e.g., spam detection).
- `user_input_rules`: Guidelines for the type of user inputs to generate.
- `assistant_response_rules`: Specifies the desired response behavior from the assistant.
- `suffix`: A unique identifier for the fine-tuned model on Together AI.
- `target_conversations`: The total number of conversations to generate. More conversations can improve the model's accuracy but increase computational costs.
- `conversation_batch_size`: The number of conversations generated per API call. Smaller batches might be more stable and diverse but could result in a higher number of API calls.

**Note on Customization:**
Increasing `target_conversations` generally leads to better model performance by providing more diverse training data, but also incurs higher costs due to more OpenAI API calls. Adjusting `conversation_batch_size` affects generation stability and diversity; smaller batch sizes are often more stable but may increase the risk of duplicates across batches.


### Customization

You can tailor the `autofinetune` script to better fit your project's needs by adjusting several key variables at the beginning of the `autofinetune.py` file:

- `objective`: Define the overarching goal of the model you're fine-tuning (e.g., classifying messages as spam or not spam).
- `user_input_rules`: Set guidelines for the types of user inputs the script should generate (e.g., random email titles).
- `assistant_response_rules`: Specify the desired behavior for the assistant's responses (e.g., responding with "spam" or "not spam").
- `suffix`: Provide a unique identifier for your fine-tuned model on the Together AI platform.
- `target_conversations`: The total number of conversation entries you aim to generate for your dataset. Increasing this number can enhance the model's performance by providing it with more training data but will also increase the computational cost.
- `conversation_batch_size`: The number of conversation entries to generate in each batch. Smaller batch sizes may lead to a more stable generation process and reduce the risk of duplicate entries, but adjusting this number can help find the right balance between efficiency and diversity in your dataset.

#### Note on Generation Settings:

- **Cost vs. Quality**: Generating a larger number of conversations (`target_conversations`) is likely to result in a better-trained model due to the increased amount and variety of training data. However, it's important to be mindful of the cost associated with API calls to OpenAI, as more conversations mean more calls.
  
- **Batch Size Considerations**: Opting for a smaller `conversation_batch_size` can help in managing API request loads and may reduce the risk of generating duplicate or highly similar entries. This setting can be crucial for ensuring the diversity of your dataset but might necessitate fine-tuning to achieve the best balance between uniqueness and stability in generation.



## Contributing

Contributions to `autofinetune` are welcome! Whether it's feature requests, bug reports, or code contributions, please feel free to open an issue or submit a pull request on GitHub.

## License

`autofinetune` is open-source software licensed under the MIT license.

---

This README provides a basic overview of `autofinetune`, its functionality, and how to get started. For more detailed information, please refer to the code comments or open an issue on GitHub.
