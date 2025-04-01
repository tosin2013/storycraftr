# Getting Started with StoryCraftr 📚✨

**StoryCraftr** is your AI-powered writing companion, designed to help you write your book. Whether you're outlining, building worlds, or writing chapters, StoryCraftr is here to assist you every step of the way.

## Quick Start Guide ⚡️

### 1. Set Up Your Environment

```bash
# Create and activate virtual environment
python3.11 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -e .
```

### 2. Set Up Your Configuration

```bash
# Create StoryCraftr directory and add your OpenAI API key
mkdir -p ~/.storycraftr/
echo "your-openai-api-key" > ~/.storycraftr/openai_api_key.txt

# Configure your preferred AI model
cat > ~/.storycraftr/config.json << EOL
{
  "openai_model": "gpt-4-0125-preview",
  "openai_url": "https://api.openai.com/v1/"
}
EOL
```

### 3. Start Your Book

```bash
storycraftr init "The Last Garden" --primary-language "en" --genre "sci-fi" --behavior "behavior.txt"
```

Before running the init command, create a behavior file that will guide the AI:

```bash
cat > behavior.txt << 'EOL'
You are an AI writing assistant helping to craft a sci-fi novel titled "The Last Garden". Your role is to:

1. Help develop complex characters who embody different perspectives on humanity's relationship with nature
2. Create a scientifically grounded near-future world where synthetic biology has replaced natural ecosystems
3. Maintain a balance between scientific accuracy and engaging storytelling
4. Ensure the plot explores themes of preservation, adaptation, and the value of natural diversity
5. Develop realistic conflicts between technological progress and environmental conservation
6. Focus on hopeful solutions while acknowledging the serious challenges of climate change

Please provide thoughtful, scientifically informed suggestions while crafting an engaging narrative that inspires environmental awareness.
EOL
```

That's it! You're ready to start writing. 🎉

## Writing Your Book 📝

### Interactive Mode

The easiest way to work on your book is through StoryCraftr's interactive chat mode:

```bash
storycraftr chat
```

In chat mode, you can:
- Generate outlines
- Create characters
- Build your world
- Write chapters
- Get writing advice
- And more!

Just type your questions or requests naturally, and StoryCraftr will help you.

#### Interactive Chat Examples

Here's a typical workflow using chat mode for "The Last Garden":

```bash
$ storycraftr chat

# Start with world building
> Help me develop the concept of synthetic vegetation in my world. What are its benefits and drawbacks?

# Create character profiles
> Create a profile for Dr. Maya Chen, including her background in botany and personal motivations for protecting natural ecosystems.

# Develop plot points
> I need a scene where Dr. Chen discovers evidence that the synthetic plants are affecting local wildlife. Help me brainstorm the details.

# Refine existing content
> Review my latest chapter and suggest ways to strengthen the conflict between preservation and progress.

# Get scientific accuracy
> Verify the scientific accuracy of my description of genetic modification techniques used in the synthetic plants.
```

Each chat interaction builds upon previous context, allowing for deep, meaningful development of your story. You can also use special commands in chat mode:

```bash
!save           # Save the current conversation
!history        # View chat history
!context        # Show current story context
!outline        # View/edit your outline
!help           # List all available commands
```

### Available Commands

If you prefer using specific commands, here are the main ones:

1. **Create an Outline**:
   ```bash
   storycraftr outline general-outline "Create a plot structure for 'The Last Garden', focusing on Dr. Maya Chen's mission to protect Earth's final natural ecosystem while confronting the synthetic biology corporation that wants to replace it."
   ```

2. **Build Your World**:
   ```bash
   storycraftr worldbuilding environment "Detail the contrast between the last natural garden - a hidden biodome in the Rockies - and the surrounding world of synthetic, genetically optimized vegetation."
   ```

3. **Write Chapters**:
   ```bash
   storycraftr chapters chapter 1 "Write the opening chapter where Dr. Chen discovers an unprecedented bloom in the garden, suggesting nature's resilience."
   ```

4. **Generate PDF**:
   ```bash
   storycraftr publish pdf en
   ```

## Development Mode 🛠️

### Project Structure

When you initialize a new book project, StoryCraftr creates the following structure:

```
the-last-garden/
├── storycraftr.json         # Project configuration
├── behaviors/
│   └── default.txt         # AI behavior guidelines
├── chapters/
│   ├── chapter-1.md        # First chapter
│   ├── cover.md           # Book cover description
│   ├── back-cover.md      # Back cover synopsis
│   └── epilogue.md        # Epilogue
├── outline/
│   ├── general_outline.md  # Overall plot structure
│   ├── character_summary.md # Character profiles
│   ├── plot_points.md     # Major plot points
│   └── chapter_synopsis.md # Chapter-by-chapter summary
├── worldbuilding/
│   ├── environment.md      # World's environmental details
│   ├── technology.md      # Technological systems
│   └── society.md         # Social and cultural aspects
└── templates/
    └── template.tex       # LaTeX template for PDF generation

Example storycraftr.json:
```json
{
  "book_path": "./the-last-garden",
  "book_name": "The Last Garden",
  "primary_language": "en",
  "genre": "cli-fi",
  "default_author": "Your Name",
  "license": "CC BY-NC-SA",
  "openai_model": "gpt-4-0125-preview",
  "openai_url": "https://api.openai.com/v1/",
  "multiple_answer": true
}
```

When developing StoryCraftr locally:

1. **Install Dev Dependencies**:
   ```bash
   poetry install
   ```

2. **Run Tests**:
   ```bash
   poetry run pytest
   ```

3. **Local Changes**:
   Any changes you make to the code will be immediately reflected in your local installation since we used `pip install -e .`

## Supported AI Models 🤖

StoryCraftr works with various AI models. Here are some popular options:

1. **OpenAI GPT-4** (Recommended)
   ```json
   {
     "openai_model": "gpt-4-0125-preview",
     "openai_url": "https://api.openai.com/v1/"
   }
   ```

2. **Azure OpenAI**
   ```json
   {
     "openai_model": "gpt-4-0125-preview",
     "openai_url": "your-azure-endpoint"
   }
   ```

3. **Other Compatible Models**
   - DeepSeek
   - Qwen
   - Gemini
   - Together AI
   - DeepInfra

## Need Help? 🤔

1. Start the interactive chat:
   ```bash
   storycraftr chat
   ```

2. Ask for help with any command:
   ```bash
   storycraftr --help
   ```

3. Visit our documentation: [docs.storycraftr.ai](https://docs.storycraftr.ai)

## Best Practices & Tips 💡

### Workflow Tips

1. **Start with World Building**
   - Begin by developing your world's core concepts
   - For "The Last Garden", start with the environmental changes that led to synthetic vegetation
   - Document key world elements in the `worldbuilding/` directory

2. **Character Development**
   - Create detailed character profiles before writing
   - Use the chat mode to explore character motivations and conflicts
   - Keep character details consistent in `outline/character_summary.md`

3. **Outline First**
   - Develop a solid outline before diving into chapters
   - Break down major plot points
   - Use the outline commands to structure your story

4. **Iterative Writing**
   - Write first drafts quickly
   - Use the `!iterate` command to refine content
   - Get scientific accuracy checks when needed

### Version Control Tips

1. **Regular Saves**
   ```bash
   !save "Completed first draft of Chapter 1"
   ```

2. **Track Changes**
   - Keep a writing log in `outline/progress.md`
   - Use descriptive save messages
   - Review history with `!history`

### Collaboration Features

1. **Share Context**
   ```bash
   !context export "garden-world-building"
   ```

2. **Import Shared Content**
   ```bash
   !context import "colleague-feedback.json"
   ```

Happy writing! ✍️
