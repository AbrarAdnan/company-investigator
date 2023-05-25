from flask import Flask, render_template, request, jsonify
import asyncio, re
from EdgeGPT import Chatbot, ConversationStyle

app = Flask(__name__, static_url_path='/static')

async def main(prompt, conversation_style):
    for i in range(5):
        try:
            bot = await Chatbot.create()
            response = await bot.ask(prompt=prompt, conversation_style=conversation_style)

            # Get the response message
            messages = response['item']['messages']
            response_message = messages[1]['text']

            if bot:
                await bot.close()

            return response_message
        except Exception as e:
            print(f"An error occurred: {e}")
            if bot:
                await bot.close()
            await asyncio.sleep(1)  # Wait for 1 second before retrying

    # If all attempts fail, close the bot and return "N/A"
    if bot:
        await bot.close()
    return "N/A"

def get_data(prompt):
    responses = []
    # conversation_styles = [ConversationStyle.balanced, ConversationStyle.creative, ConversationStyle.precise]
    conversation_styles = [ConversationStyle.balanced, ConversationStyle.precise]

    for conversation_style in conversation_styles:
        print(conversation_style)
        try:
            response = asyncio.run(main(prompt, conversation_style))
        except Exception:
            response = "N/A"
        responses.append(response)
        print(response)

    outputs = []
    for response in responses:
        if response == "N/A":
            continue

        output_match = re.search(r"output\s+=\s+(\[.*?\])", response, re.DOTALL)
        if output_match:
            output_code = output_match.group(1)
            try:
                output = eval(output_code)
                outputs.extend(output)
            except Exception:
                pass

    flattened_outputs = list(set(outputs))
    return flattened_outputs

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if request.content_type == 'application/json':
            data = request.get_json()
            company_name = data.get('company_name')
            country = data.get('country')
            company_website = data.get('company_website')
        else:
            company_name = request.form.get('company_name')
            country = request.form.get('country')
            company_website = request.form.get('company_website')

        print(company_name)
        print(company_website)
        print(country)
        result = company_name

        product_services_prompt = f"Give me the products/services of the company {company_name} from {country} as a list variable in Python called output"
        product_services = get_data(product_services_prompt)
        print(product_services)

        keyword_prompt = f"Give me the keywords related to the company {company_name} from {country} as list variable in python called output"
        keyword = get_data(keyword_prompt)
        print(keyword)

        sic_prompt = f"Give me the SIC company classification number of company {company_name} from {country} as list variable in python called output"
        sic = list(set(get_data(sic_prompt)))
        sic_int = []
        for s in sic:
            try:
                sic_int.append(int(s))
            except ValueError:
                pass
        print(sic_int)

        naics_prompt = f"Give me the NAICS company classification number of company {company_name} from {country} as list variable in python called output"
        naics = list(set(get_data(naics_prompt)))
        naics_int = []
        for n in naics:
            try:
                naics_int.append(int(n))
            except ValueError:
                pass
        print(naics_int)

        if request.content_type == 'application/json':
                response = {
                        'product_services': product_services,
                        'keyword': keyword,
                        'sic' : sic,
                        'naics' : naics
                }
                return jsonify(response)
        else:
            return render_template('index.html', show='result', results=result, product_services = product_services, keyword = keyword, sic = sic, naics = naics)
    else:
        return render_template('index.html', show=False)

if __name__ == '__main__':
    app.run(debug=True)