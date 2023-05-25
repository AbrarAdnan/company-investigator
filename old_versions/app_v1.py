from flask import Flask, render_template, request
import asyncio
from EdgeGPT import Chatbot, ConversationStyle
import re

app = Flask(__name__, static_url_path='/static')

async def main(prompt):
    bot = await Chatbot.create()  # Passing cookies is optional

    response = await bot.ask(prompt=prompt, conversation_style=ConversationStyle.balanced)

    # Get the response message
    messages = response['item']['messages']
    response_message = messages[1]['text']  # Assuming the response is at index 1

    await bot.close()

    return response_message

def get_data(prompt):
    # Run the script and capture the output
    response = asyncio.run(main(prompt))
    print("Response:", response)

    # Extract the part within the `output` variable
    output_match = re.search(r"output\s+=\s+(\[.*?\])", response, re.DOTALL)
    if output_match:
        output_code = output_match.group(1)
        output = eval(output_code)
    else:
        output = []
    return output

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        company_name = request.form['company_name']
        country = request.form['country']
        company_website = request.form['company_website']
        print(company_name)
        print(company_website)
        print(country)
        result = company_name

        # Get the products/services list
        product_services_prompt = f"Give me the products/services of {company_name} from {country} as a list variable in Python called output"
        product_services = get_data(product_services_prompt)
        print(product_services)

        # Get the keywords
        keyword_prompt = f"Give me the Keywords related to {company_name} from {country} as list variable in python called output"
        keyword = get_data(keyword_prompt)
        print(keyword)

        # Get the keywords
        sic_prompt = f"Give me the SIC company classification of {company_name} from {country} as list variable in python called output"
        sic = get_data(sic_prompt)
        print(sic)

        # Get the keywords
        naics_prompt = f"Give me the NAICS company classification of {company_name} from {country} as list variable in python called output"
        naics = get_data(naics_prompt)
        print(naics)

        return render_template('index.html', show='result', results=result, product_services = product_services, keyword = keyword, sic = sic, naics = naics)
    else:
        return render_template('index.html', show=False)

if __name__ == '__main__':
    app.run(debug=True)