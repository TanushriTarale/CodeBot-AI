from django.shortcuts import render, redirect
from django.contrib import messages
import requests
import google.generativeai as genai
# Your Google Gemini API key
GEMINI_API_KEY = "AIzaSyC_UKCz-ddKdDCn9t8Mn3m1deAcy6HsWWU"


def home(request):
    lang_list = ['c', 'clike', 'cpp', 'csharp', 'css', 'dart', 'django', 'docker', 'go', 'html', 'java', 'javascript',
                 'json', 'json5', 'jsx', 'markup', 'markup-templating', 'perl', 'php', 'plsql', 'powershell', 'python',
                 'regex', 'sql', 'tsx', 'typescript', 'yaml']

    if request.method == "POST":
        code = request.POST['code']
        lang = request.POST['lang']

        if lang == "Select Programming Language":
            messages.success(request, 'Hey! You forgot to pick a programming language...')
            return render(request, 'home.html', {'lang_list': lang_list, 'response': code, 'code': code, 'lang': lang})
        else:
            # Make a request to the Google Gemini API
            headers = {
                "Authorization": f"Bearer {GEMINI_API_KEY}",
                "Content-Type": "application/json"
            }

            payload = {
                "prompt": f"Respond only with code. Fix this {lang} code: {code}",
                "temperature": 0,
                "max_tokens": 1000,
                "top_p": 1.0,
                "frequency_penalty": 0.0,
                "presence_penalty": 0.0
            }

            try:
                # Replace the following URL with the actual Google Gemini API endpoint
                response = requests.post('https://gemini.googleapis.com/v1/engines/text-davinci-003/completions',
                                         headers=headers, json=payload)
                genai.configure(api_key="AIzaSyBuM8g8Z0EWKU8LWwbV-LO6GtLP5cE4epE")
                model = genai.GenerativeModel("gemini-1.5-flash")
                response = model.generate_content(f"Respond only with code. Fix this {lang} code: {code}")

                return render(request, 'home.html',
                    {'lang_list': lang_list, 'response': (response.parts[0].text).replace("```", ""), 'lang': lang})


            except Exception as e:
                return render(request, 'home.html', {'lang_list': lang_list, 'response': str(e), 'lang': lang})

    return render(request, 'home.html', {'lang_list': lang_list})


def suggest(request):
    lang_list = ['c', 'clike', 'cpp', 'csharp', 'css', 'dart', 'django', 'docker', 'go', 'html', 'java', 'javascript',
                 'json', 'json5', 'jsx', 'markup', 'markup-templating', 'perl', 'php', 'plsql', 'powershell', 'python',
                 'regex', 'sql', 'tsx', 'typescript', 'yaml']

    if request.method == "POST":
        code = request.POST['code']
        lang = request.POST['lang']

        if lang == "Select Programming Language":
            messages.success(request, 'Hey! You forgot to pick a programming language...')
            return render(request, 'suggest.html',
                          {'lang_list': lang_list, 'response': code, 'code': code, 'lang': lang})
        else:
            # Make a request to the Google Gemini API
            headers = {
                "Authorization": f"Bearer {GEMINI_API_KEY}",
                "Content-Type": "application/json"
            }

            payload = {
                "prompt": f"Respond only with code. {code}",
                "temperature": 0,
                "max_tokens": 1000,
                "top_p": 1.0,
                "frequency_penalty": 0.0,
                "presence_penalty": 0.0
            }

            try:
                # Replace the following URL with the actual Google Gemini API endpoint
                response = requests.post('https://gemini.googleapis.com/v1/engines/text-davinci-003/completions',
                                         headers=headers, json=payload)
                response_data = response.json()

                if response.status_code == 200:
                    # Parse the response
                    response_text = (response_data["choices"][0]["text"]).strip()
                    return render(request, 'suggest.html',
                                  {'lang_list': lang_list, 'response': response_text, 'lang': lang})
                else:
                    messages.error(request, f"Error: {response_data.get('error', 'Unknown error')}")
                    return render(request, 'suggest.html', {'lang_list': lang_list, 'response': code, 'lang': lang})

            except Exception as e:
                return render(request, 'suggest.html', {'lang_list': lang_list, 'response': str(e), 'lang': lang})

    return render(request, 'suggest.html', {'lang_list': lang_list})