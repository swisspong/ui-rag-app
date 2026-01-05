import asyncio
from dataclasses import dataclass
from typing import List, Dict, Any, BinaryIO
import requests
import json
from dacite import from_dict
from src.contexts.rag.domain.services.ocr import OCR
import httpx
from PyPDF2 import PdfReader
from src.shared.domain.entities.asset import Asset


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


class TyphoonOCR(OCR):
    url = "https://api.opentyphoon.ai/v1/ocr"

    async def extract_text(self, asset: Asset, stream: BinaryIO) -> str:
        api_key = "sk-Um5TZvQLijXnFOGtzohvaklkcObXAjrHF8rBt5d7fHq5xCxj"
        model = "typhoon-ocr-preview"
        task_type = "default"
        max_tokens = 16384
        temperature = 0.1
        top_p = 0.6
        repetition_penalty = 1.2
        try:
            reader = PdfReader(stream)
            number_of_pages = len(reader.pages)
            all_pages = list(range(1, number_of_pages+1))
            
            # Split pages into batches of 50
            batch_size = 50
            page_batches = [all_pages[i:i + batch_size] for i in range(0, len(all_pages), batch_size)]
            
            all_extracted_texts = []
            
            # Process each batch sequentially
            for batch_index, batch_pages in enumerate(page_batches):
                print(f"Processing batch {batch_index + 1}/{len(page_batches)} with pages {batch_pages[0]}-{batch_pages[-1]}")
                
                stream.seek(0)
                
                files = {'file': (asset.filename, stream, asset.content_type)}
                data = {
                    'model': model,
                    'task_type': task_type,
                    'max_tokens': str(max_tokens),
                    'temperature': str(temperature),
                    'top_p': str(top_p),
                    'repetition_penalty': str(repetition_penalty)
                }
                print(batch_pages)
                if batch_pages:
                    data['pages'] = json.dumps(batch_pages)

                headers = {
                    'Authorization': f'Bearer {api_key}'
                }
                
                async with httpx.AsyncClient(timeout=None) as client:
                    response = await client.post(self.url, files=files, data=data, headers=headers)
                    if response.status_code == 200:
                        result = response.json()
                        extracted_texts = []
                        # result = from_dict(data_class=TyphoonResponse, data=result)


                        for page_result in result.get('results', []):
                            if page_result.get('success') and page_result.get('message'):
                                content = page_result['message']['choices'][0]['message']['content']
                                try:
                                    # Try to parse as JSON if it's structured output
                                    parsed_content = json.loads(content)
                                    text = parsed_content.get(
                                        'natural_text', content)
                                    # print("=========================")
                                    # print(text)
                                except json.JSONDecodeError:
                                    text = content
                                    # print("=========================")
                                    # print(text)
                                extracted_texts.append(text)
                            elif not page_result.get('success'):
                                print(
                                    f"Error processing {page_result.get('filename', 'unknown')}: {page_result.get('error', 'Unknown error')}")

                        # for page_result in result.results:
                        #     if page_result.success and page_result.message:
                        #         content = page_result.message.choices[0].message.content
                        #         try:
                        #             text = content.natural_text
                        #         except json.JSONDecodeError:
                        #             text = content
                        #         extracted_texts.append(text)
                        #     elif not page_result.get('success'):
                        #         print(
                        #             f"Error processing {page_result.get('filename', 'unknown')}: {page_result.get('error', 'Unknown error')}")

                        all_extracted_texts.extend(extracted_texts)
                    else:
                        print(f"Error: {response.status_code}")
                        print(response.text)
                        return None

            return '\n'.join(all_extracted_texts)
        finally:
            stream.close()
        # with open(file_path, 'rb') as file:
        #     files = {'file': file}
        #     data = {
        #         'model': model,
        #         'task_type': task_type,
        #         'max_tokens': str(max_tokens),
        #         'temperature': str(temperature),
        #         'top_p': str(top_p),
        #         'repetition_penalty': str(repetition_penalty)
        #     }

        #     # reader = PdfReader(file_path)
        #     # number_of_pages = len(reader.pages)
        #     # pages = list(range(1, number_of_pages+1))

        #     if pages:
        #         data['pages'] = json.dumps(pages)

        #     headers = {
        #         'Authorization': f'Bearer {api_key}'
        #     }
        #     async with httpx.AsyncClient(timeout=None) as client:
        #         response = await client.post(self.url, files=files, data=data, headers=headers)
        #         if response.status_code == 200:
        #             result = response.json()
        #             extracted_texts = []
        #             result = from_dict(data_class=TyphoonResponse, data=result)

        #             for page_result in result.results:
        #                 if page_result.success and page_result.message:
        #                     content = page_result.message.choices[0].message.content
        #                     try:
        #                         text = content.natural_text
        #                     except json.JSONDecodeError:
        #                         text = content
        #                     extracted_texts.append(text)
        #                 elif not page_result.get('success'):
        #                     print(
        #                         f"Error processing {page_result.get('filename', 'unknown')}: {page_result.get('error', 'Unknown error')}")

        #             return '\n'.join(extracted_texts)
        #         else:
        #             print(f"Error: {response.status_code}")
        #             print(response.text)
        #             return None


if __name__ == "__main__":
    file_path = "test.pdf"
    ocr = TyphoonOCR()
    result = asyncio.run(ocr.extract_text(file_path))
