import os
import json

from typing import Dict
from google import genai
from google.genai.types import Tool, GenerateContentConfig, GoogleSearch
from tavily import TavilyClient
from dotenv import load_dotenv

load_dotenv()

# Get the API keys from the environment variables
genai_key = os.getenv("GENAI_API_KEY")
tavily_key = os.getenv("TAVILY_API_KEY")

# Define the AgentInterface class
class AgentInterface:

    def __init__(self, user_data: Dict) -> None:
        """
        Initialize the AgentInterface class with the user data.
        """
        self.user_data  = user_data
        self.gen_client = genai.Client(api_key=genai_key)
        self.tav_client = TavilyClient(tavily_key)
        self.gen_tools  = [
            Tool(google_search=GoogleSearch())
        ]

    def get_pizzarias(self, user_prompt: str):
        """
        Generate a response for the user prompt to list pizzarias.
        """

        # Get the source URL to search for pizzarias from
        url_query = """\
            liste pizzeria
            via : google search
        """
        url_list = self.tav_client.search(query=url_query)

        # Generate the generative AI prompt
        prompt = f"""\
        **Instructions :**

        - Lister les pizzerias tire de ce resultats {url_list} avec les informations suivantes :
        - **Statut** : `true`
        - **Nom** : Nom de la pizzeria
        - **Location** : Emplacement de la pizzeria
        - **Ouverture status** :
            - `true` si ouvert
            - `false` si fermé
            - `null` si indisponible
        - **Logo** : Lien image  du pizzeria via Internet   (mettre `null` si indisponible)
        - **Statut de livraison** : Valeur booléenne (`true` ou `false`)
        - **Contact** (objet contenant les attributs suivants) :
            - **Téléphone**
            - **E-mail**
            - **Facebook**

        - Utiliser comme sources de données : Google Search, Google Maps, Facebook, autres réseaux sociaux, etc.
        - Si les données sont indisponibles, mettre `null`.

        **Prompt utilisateur :**
        `{user_prompt}`

        **Données de l'utilisateur :**
        `{self.user_data}`

        **Instructions supplémentaires :**
        - Veuillez afficher uniquement les données sous forme de JSON, sans aucun texte dans la réponse.
        - Si le prompt utilisateur ne précise pas de localisation, prioriser les résultats les plus proches de sa localisation ; sinon, prioriser la localisation spécifiée par l’utilisateur.
        - Si les résultats contiennent des valeurs `null`, définir `statut` à `false`.

        """

        # Generate the response
        response = self.gen_client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt,
            config=GenerateContentConfig(
                tools=self.gen_tools,
                response_modalities=["TEXT"],
            )
        )

        # Return the response
        try:
            return json.loads(response.text)
        except json.JSONDecodeError:
            raise Exception(f"Error decoding the response.\nCurrent output: {response.text}")


        def get_all_pizza(self, prompt_user: str):
            """
            Generate a response for the user prompt to list all pizzas.
            """

            # Generate the generative AI prompt
            prompt_standard = (
                "### Instruction\n"
                "Génère une liste de dictionnaires Python correspondant aux pizzas qui répondent au mieux à la demande suivante.\n\n"
                "### Voici le prompt de l'utilisateur\n"
                + prompt_user + "et à" + self.userData + "\n\n"
                "### Format des données\n"
                "Chaque dictionnaire devra contenir les clés suivantes : 'statut', 'nom', 'localisation', 'pizzeria', "
                "'ingrédients', 'taille', 'prix'.\n\n"
                "- 'statut' : true si les résultats sont acceptables, false sinon.\n"
                "- 'nom' : Le nom de la pizza (ex. : 'Pizza 4 fromages').\n"
                "- 'localisation' : L'adresse complète de la pizzeria.\n"
                "- 'pizzeria' : Le nom de la pizzeria.\n"
                "- 'ingrédients' : Une liste des ingrédients utilisés (ex. : ['Mozzarella', 'Gorgonzola', 'Parmesan', 'Emmental']).\n"
                "- 'taille' : La taille de la pizza (ex. : '30 cm').\n"
                "- 'prix' : Le prix en euros (ex. : 12.50).\n\n"
                # "### Données de l'utilisateur\n"
                # + self.userData + "\n\n"
                "### Instructions supplémentaires\n"
                "- Fournir autant de dictionnaires que possible, un par pizzeria.\n"
                "- La réponse doit être une liste de dictionnaires Python valide, sans aucune explication ou commentaire supplémentaire."
                "- Si certaines informations sont indisponibles, utiliser NULL comme valeur.\n"
                "- L'utilisation de Facebook comme source de recherche est conseillée.\n"
                "- L'utilisation de google map comme source de recherche est conseillée. \n"
                "- Si les résultats contiennent trop de valeurs NULL, définir 'statut' à false.\n"
                "- Si le prompt de l'utilisateur ne contient pas de localisation, en ajouter une par défaut en fonction du contexte.\n"
            )

            # Generate the response
            response = self.gen_client.models.generate_content(
                model="gemini-2.0-flash",
                contents=prompt_standard,
                config=GenerateContentConfig(
                    tools=self.gen_tools,
                    response_modalities=["TEXT"],
                )
            )

            # Return the response
            try:
                return json.loads(response.text)
            except json.JSONDecodeError:
                raise Exception(f"Error decoding the response.\nCurrent output: {response.text}")


        def get_all_pizza_by_pizzeria(self, pizzeria: str):
            """
            Generate a response for the user prompt to list all pizzas by pizzeria.
            """

            # Generate the generative AI prompt
            prompt_standard = (
                "### Instruction\n"
                "Génère une liste de dictionnaires Python correspondant aux pizzas disponibles dans la pizzeria spécifiée.\n\n"
                "### Pizzeria ciblée\n"
                + pizzeria + "\n\n"
                "### Format des données\n"
                "Chaque dictionnaire devra contenir les clés suivantes : 'statut', 'nom', 'localisation', 'pizzeria', "
                "'ingrédients', 'taille', 'prix'.\n\n"
                "- 'statut' : true si les informations sont valides, false sinon.\n"
                "- 'nom' : Le nom de la pizza (ex. : 'Pizza 4 fromages').\n"
                "- 'localisation' : L'adresse complète de la pizzeria.\n"
                "- 'pizzeria' : Le nom de la pizzeria.\n"
                "- 'ingrédients' : Une liste des ingrédients utilisés (ex. : ['Mozzarella', 'Gorgonzola', 'Parmesan', 'Emmental']).\n"
                "- 'taille' : La taille de la pizza (ex. : '30 cm').\n"
                "- 'prix' : Le prix en euros (ex. : 12.50).\n\n"
                "### Instructions supplémentaires\n"
                "- Fournir autant de dictionnaires que de pizzas proposées par la pizzeria.\n"
                "- La réponse doit être une liste de dictionnaires Python valide, sans aucune explication ou commentaire supplémentaire."
                "- Si certaines informations sont indisponibles, utiliser NULL comme valeur.\n"
                "- L'utilisation de Facebook comme source de recherche est conseillée.\n"
                "- L'utilisation de google map comme source de recherche est conseillée. \n"
                "- Si les résultats contiennent trop de valeurs 'Inconnu', définir 'statut' à false.\n"
            )

            # Generate the response
            response = self.gen_client.models.generate_content(
                model="gemini-2.0-flash",
                contents=prompt_standard,
                config=GenerateContentConfig(
                    tools=self.gen_tools,
                    response_modalities=["TEXT"],
                )
            )

            # Return the response
            try:
                return json.loads(response.text)
            except json.JSONDecodeError:
                raise Exception(f"Error decoding the response.\nCurrent output: {response.text}")
