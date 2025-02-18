import base64
from vertexai.generative_models import Part

class Document():
    def __init__(self, 
                 b64_encode:str):
        self.__b64_encode = b64_encode
        self.__part_document = None
        
    def part_pdf(self):
        """Converte il documento pdf nella classe Part per poter essere utilizzato da un llm e lo assegna al relativo attributo di classe.

        Args:
        None.

        Returns:
        None.
        """
        self.__part_document = Part.from_data(
            mime_type = "application/pdf",
            data = base64.b64decode(self.__b64_encode)
        )
        
    def part_image(self):
        """Converte il documento immagine nella classe Part per poter essere utilizzato da un llm e lo assegna al relativo attributo di classe.

        Args:
        None.

        Returns:
        None.
        """
        self.__part_document = Part.from_data(
            mime_type = "image/png",
            data = base64.b64decode(self.__b64_encode)
        )
        
    def get_part_document(self):
        """Restituisce il documento in formato Part, da utilizzare solo dopo che il documento è stato trasformato.

        Args:
        None.

        Returns:
        Documento in classe Part.
        """
        return self.__part_document