from django.shortcuts import render, redirect
import datetime
import requests
import wikipedia
import pyjokes
import openai

openai.api_key = 'your_openai_api_key_here'  # Replace with your real key

def home(request):
    response = ''
    if request.method == 'POST':
        command = request.POST.get('command', '').lower()

        if 'time' in command:
            now = datetime.datetime.now().strftime("%H:%M:%S")
            response = f"The time is {now}"

        elif 'date' in command:
            today = datetime.datetime.now().strftime("%Y-%m-%d")
            response = f"Today's date is {today}"

        # 🌐 Website Openers
        elif 'open google' in command:
            return redirect("https://www.google.com")
        elif 'open youtube' in command:
            return redirect("https://www.youtube.com")
        elif 'open instagram' in command:
            return redirect("https://www.instagram.com")
        elif 'open whatsapp' in command:
            return redirect("https://web.whatsapp.com")
        elif 'open facebook' in command:
            return redirect("https://www.facebook.com")
        elif 'open twitter' in command or 'open x' in command:
            return redirect("https://www.twitter.com")
        elif 'open chatgpt' in command:
            return redirect("https://chat.openai.com")
        elif 'open gmail' in command:
            return redirect("https://mail.google.com")
        elif 'open github' in command:
            return redirect("https://github.com")
        elif 'open linkedin' in command:
            return redirect("https://www.linkedin.com")

        elif 'your name' in command:
            response = "I am Jarvis, your assistant."

        elif 'joke' in command:
            response = pyjokes.get_joke()

        elif 'wikipedia' in command:
            try:
                topic = command.replace('wikipedia', '').strip()
                summary = wikipedia.summary(topic, sentences=2)
                response = summary
            except Exception as e:
                response = f"Error searching Wikipedia: {str(e)}"

        elif 'weather' in command:
            city = command.replace('weather', '').strip()
            if not city:
                response = "Please provide a city name."
            else:
                try:
                    api_key = 'your_openweathermap_api_key'
                    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
                    data = requests.get(url).json()
                    if str(data.get('cod')) == '200':
                        temp = data['main']['temp']
                        description = data['weather'][0]['description']
                        response = f"The weather in {city} is {temp}°C with {description}."
                    else:
                        response = "City not found or API error."
                except Exception as e:
                    response = f"Error fetching weather: {str(e)}"

        elif 'chat' in command:
            user_input = command.replace('chat', '').strip()
            if not user_input:
                response = "Please say something for me to respond to."
            else:
                try:
                    completion = openai.ChatCompletion.create(
                        model="gpt-3.5-turbo",
                        messages=[
                            {"role": "system", "content": "You are a helpful assistant named Jarvis."},
                            {"role": "user", "content": user_input}
                        ]
                    )
                    response = completion.choices[0].message['content'].strip()
                except Exception as e:
                    response = f"OpenAI error: {str(e)}"

        else:
            # Default fallback to ChatGPT
            try:
                completion = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant named Jarvis."},
                        {"role": "user", "content": command}
                    ]
                )
                response = completion.choices[0].message['content'].strip()
            except Exception as e:
                response = f"OpenAI error: {str(e)}"

    return render(request, 'jarvis/home.html', {'response': response})
