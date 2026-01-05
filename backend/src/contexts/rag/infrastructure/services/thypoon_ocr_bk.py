import asyncio
from dataclasses import dataclass
from typing import List, Dict, Any
import requests
import json
from dacite import from_dict

import httpx
from PyPDF2 import PdfReader


@dataclass
class NaturalText:
    natural_text: str


@dataclass
class Content:
    content: NaturalText


@dataclass
class SubMessage:
    message: Content


@dataclass
class Message:
    choices: List[SubMessage]


@dataclass
class Item:

    success: bool
    message: Message


@dataclass
class TyphoonResponse:
    results: List[Item]


class TyphoonOCR:
    url = "https://api.opentyphoon.ai/v1/ocr"

    async def extract_text(self, file_path, config: Dict[str, Any] = None) -> str:
        api_key = "sk-Um5TZvQLijXnFOGtzohvaklkcObXAjrHF8rBt5d7fHq5xCxj"
        model = "typhoon-ocr-preview"
        task_type = "default"
        max_tokens = 16384
        temperature = 0.1
        top_p = 0.6
        repetition_penalty = 1.2

        with open(file_path, 'rb') as file:
            files = {'file': file}
            data = {
                'model': model,
                'task_type': task_type,
                'max_tokens': str(max_tokens),
                'temperature': str(temperature),
                'top_p': str(top_p),
                'repetition_penalty': str(repetition_penalty)
            }

            reader = PdfReader(file_path)
            number_of_pages = len(reader.pages)
            pages = list(range(1, number_of_pages+1))

            if pages:
                data['pages'] = json.dumps(pages)

            headers = {
                'Authorization': f'Bearer {api_key}'
            }
            async with httpx.AsyncClient(timeout=None) as client:
                response = await client.post(self.url, files=files, data=data, headers=headers)
                if response.status_code == 200:
                    result = response.json()
                    extracted_texts = []
                    result = from_dict(data_class=TyphoonResponse, data=result)

                    for page_result in result.results:
                        if page_result.success and page_result.message:
                            content = page_result.message.choices[0].message.content
                            try:
                                text = content.natural_text
                            except json.JSONDecodeError:
                                text = content
                            extracted_texts.append(text)
                        elif not page_result.get('success'):
                            print(
                                f"Error processing {page_result.get('filename', 'unknown')}: {page_result.get('error', 'Unknown error')}")
                    # for page_result in result.get('results', []):
                    #     if page_result.get('success') and page_result.get('message'):
                    #         content = page_result['message']['choices'][0]['message']['content']
                    #         try:
                    #             # Try to parse as JSON if it's structured output
                    #             parsed_content = json.loads(content)
                    #             text = parsed_content.get(
                    #                 'natural_text', content)
                    #         except json.JSONDecodeError:
                    #             text = content
                    #         extracted_texts.append(text)
                    #     elif not page_result.get('success'):
                    #         print(
                    #             f"Error processing {page_result.get('filename', 'unknown')}: {page_result.get('error', 'Unknown error')}")

                    return '\n'.join(extracted_texts)
                else:
                    print(f"Error: {response.status_code}")
                    print(response.text)
                    return None

    def extract_text_from_image(self, image_path, api_key, model, task_type, max_tokens, temperature, top_p, repetition_penalty, pages=None):

        with open(image_path, 'rb') as file:
            files = {'file': file}
            data = {
                'model': model,
                'task_type': task_type,
                'max_tokens': str(max_tokens),
                'temperature': str(temperature),
                'top_p': str(top_p),
                'repetition_penalty': str(repetition_penalty)
            }

            if pages:
                data['pages'] = json.dumps(pages)

            headers = {
                'Authorization': f'Bearer {api_key}'
            }

            response = requests.post(
                self.url, files=files, data=data, headers=headers)

            if response.status_code == 200:
                result = response.json()

                # Extract text from successful results
                extracted_texts = []
                for page_result in result.get('results', []):
                    if page_result.get('success') and page_result.get('message'):
                        content = page_result['message']['choices'][0]['message']['content']
                        try:
                            # Try to parse as JSON if it's structured output
                            parsed_content = json.loads(content)
                            text = parsed_content.get('natural_text', content)
                        except json.JSONDecodeError:
                            text = content
                        extracted_texts.append(text)
                    elif not page_result.get('success'):
                        print(
                            f"Error processing {page_result.get('filename', 'unknown')}: {page_result.get('error', 'Unknown error')}")

                return '\n'.join(extracted_texts)
            else:
                print(f"Error: {response.status_code}")
                print(response.text)
                return None


if __name__ == "__main__":
    file_path = "test.pdf"
    ocr = TyphoonOCR()
    result = asyncio.run(ocr.extract_text(file_path))
    # print(result)

    # if __name__ == "__main__":
    #     # Usage
    #     api_key = "sk-Um5TZvQLijXnFOGtzohvaklkcObXAjrHF8rBt5d7fHq5xCxj"
    #     model = "typhoon-ocr-preview"
    #     task_type = "default"
    #     max_tokens = 16384
    #     temperature = 0.1
    #     top_p = 0.6
    #     repetition_penalty = 1.2
    #     reader = PdfReader(file_path)
    #     number_of_pages = len(reader.pages)
    #     print(number_of_pages)
    #     result = list(range(1, number_of_pages+1))
    #     print(result)
    #     pages = result
    #     ocr = TyphoonOCR()
    #     extracted_text = ocr.extract_text_from_image(
    #         file_path, api_key, model, task_type, max_tokens, temperature, top_p, repetition_penalty, pages)
    #     print(extracted_text)
