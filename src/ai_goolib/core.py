import vertexai
from vertexai.generative_models import GenerativeModel, SafetySetting
import json

class OCR():
    def __init__(self, 
                 project:str,
                 model:str, 
                 location:str = "europe-west3"):
        vertexai.init(
            project=project,
            location=location,
        )
        self.__model = GenerativeModel(
            model,
        )
        self.__generation_config = {
            'max_output_tokens' : 8192,
            'temperature' : 1,
            'top_p' : 0.95,
            'response_mime_type' : 'application/json',
            'response_schema' : {"type":"OBJECT", "properties":{"response":{"type":"STRING"}}},
        }
        self.__safety_settings = []
        
    def set_config__max_output_tokens(self, value:int):
        """Setting della configurazione per il massimo numero di token generati.

        Args:
        max_output_tokens: numero massimo di token che il modello può generare.

        Returns:
        None.
        """
        self.__generation_config["max_output_tokens"] = value
        
    def set_config__temperature(self, value:int):
        """Setting della configurazione per la quantità di token generati ad interazione.

        Args:
        temperature: indicatore che va da 0 a 2, più è alto più la risposta è prolissa.

        Returns:
        None.
        """
        self.__generation_config["temperature"] = value
        
    def set_config__top_p(self, value:int):
        """Setting della configurazione per .

        Args:
        top_p: .

        Returns:
        None.
        """
        self.__generation_config["top_p"] = value
        
    def set_config__response_mime_type(self, value:str):
        """Setting della configurazione per il tipo di formato della response.

        Args:
        response_mime_type: formato della risposta, può essere di tipo json o text.

        Returns:
        None.
        """
        self.__generation_config["response_mime_type"] = value
        
    def set_config__response_schema(self, value:dict):
        """Setting della configurazione per il formato della response.

        Args:
        response_schema: schema di generazione della risposta.

        Returns:
        None.
        """
        self.__generation_config["response_schema"] = value
        
    def get_generation_config(self):
        """Ottenimento delle configurazioni di generazione (a solo scopo consultativo, per modificare le configurazioni utilizzare i metodi set_config).

        Args:
        None.

        Returns:
        None.
        """
        return self.__generation_config
    
    def set_safety_settings(self, 
                            odio:bool = True, 
                            pericolo:bool = True, 
                            sesso:bool = True, 
                            molestie:bool = True):
        """Setting delle configurazioni di sicurezza.

        Args:
        odio: blocca la generazione di contenuti di odio.
        pericolo: blocca la generazione di contenuti potenzialmente pericolosi.
        sesso: blocca la generazione di contenuti sessualmente espliciti.
        molestie: blocca la generazione di contenuti molesti.

        Returns:
        None.
        """
        if odio == True:
            setting = SafetySetting(
                category=SafetySetting.HarmCategory.HARM_CATEGORY_HATE_SPEECH,
                threshold=SafetySetting.HarmBlockThreshold.OFF
            )
            self.__safety_settings.append(setting)
        if pericolo == True:
            setting = SafetySetting(
                category=SafetySetting.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
                threshold=SafetySetting.HarmBlockThreshold.OFF
            )
            self.__safety_settings.append(setting)
        if sesso == True:
            setting = SafetySetting(
                category=SafetySetting.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
                threshold=SafetySetting.HarmBlockThreshold.OFF
            )
            self.__safety_settings.append(setting)
        if molestie == True:
            setting = SafetySetting(
                category=SafetySetting.HarmCategory.HARM_CATEGORY_HARASSMENT,
                threshold=SafetySetting.HarmBlockThreshold.OFF
            )
            self.__safety_settings.append(setting)
            
    def run_chat(self, 
                 document, 
                 pipeline):
        response_sequence = []
        
        pipeline.start_pipeline()
        doc = document.get_part_document()
        chat = self.__model.start_chat()
        resp_0 = chat.send_message(
            [doc, pipeline.get_current_prompt()],
            generation_config=self.__generation_config,
            safety_settings=self.__safety_settings
        )
        response_sequence.append(resp_0)
        pipeline.move_forward(response=json.loads(resp_0.candidates[0].content.parts[0].text)['response'])
        while pipeline.get_current_prompt()!="<STOP>":
            resp_n = chat.send_message(
                [pipeline.get_current_prompt()],
                generation_config=self.__generation_config,
                safety_settings=self.__safety_settings
            )
            response_sequence.append(resp_n)
            pipeline.move_forward(response=json.loads(resp_n.candidates[0].content.parts[0].text)['response'])
        
        return response_sequence