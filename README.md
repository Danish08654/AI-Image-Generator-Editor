# AI-Canva-Style-Editor
An AI-powered image generation and editing platform built with Streamlit and OpenAI. Generate stunning images from text prompts or edit existing images using natural language instructions, all within a simple and intuitive interface.

---

# Features

🖼️ AI Image Generation – Create images from text prompts.

✏️ AI Image Editing – Upload an image and modify it using natural language.

🧠 Prompt Enhancement – Automatically improves user prompts for better results.

🎨 Modern Streamlit UI – Clean and responsive interface.

☁️ OpenAI Integration – Powered by advanced image generation and editing models.

📥 Image Preview & Download – Instantly view and save results.

---

#  Project Structure

ai-canva-editor/
│
├── app.py
│
├── services/
│   ├── generator.py
│   ├── editor.py
│   └── prompt_engine.py
│
├── assets/
│   ├── uploads/
│   └── outputs/
│
├── requirements.txt
├── Dockerfile
├── .env
└── README.md

----

# Install Dependencies

pip install -r requirements.txt

---

# Environment Variables

Create a .env file in the project root:

OPENAI_API_KEY=your_openai_api_key

---

# Run the Application

streamlit run app.py

# Open:

http://localhost:8501

----

#  Use Cases

AI-assisted content creation

Social media graphics generation

Creative image transformations

Marketing and design prototyping

Rapid visual ideation

---

#  Future Enhancements

Layer-based editing system

Background removal

Object selection and replacement

Image history and versioning

Multi-style generation (Anime, 3D, Cinematic, Realistic)

Local AI model fallback support

---

# License

This project is licensed under the MIT License.

---
