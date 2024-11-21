import os
import json
import pandas as pd
import google.generativeai as genai
import re
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s: %(message)s')

def configure_gemini_api(api_key):
    """Configure Gemini API with provided key."""
    os.environ["GEMINI_API_KEY"] = api_key
    genai.configure(api_key=os.environ["GEMINI_API_KEY"])
    logging.info("Gemini API configured successfully")

def extract_json_from_response(response_text):
    """
    Extract JSON from a text response using regex.
    
    This function attempts to find a JSON block in the response,
    which can help handle cases where Gemini includes explanatory text.
    """
    logging.info("Attempting to extract JSON from response")
    json_match = re.search(r'\{[^}]+\}', response_text, re.DOTALL)
    if json_match:
        try:
            parsed_json = json.loads(json_match.group(0))
            logging.info(f"Successfully parsed JSON: {parsed_json}")
            return parsed_json
        except json.JSONDecodeError:
            logging.error(f"Could not parse JSON. Response was: {response_text}")
            return {}
    logging.warning(f"No JSON found in response: {response_text}")
    return {}

def get_artist_data(artists, data_type='nationality'):
    """Retrieve artist information via Gemini with improved JSON handling."""
    logging.info(f"Retrieving {data_type} for artists: {artists}")
    
    generation_config = {
        "temperature": 0.7,
        "top_p": 0.95,
        "top_k": 64,
        "max_output_tokens": 8192,
    }
    
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=generation_config,
    )
    
    data_prompts = {
        'nationality': (
            "For the following artists, provide their nationalities as ISO country codes. "
            "If nationality is unknown, use 'NA'. "
            "Respond ONLY with a valid JSON in this format: "
            "{'ArtistName1': 'CountryCode', 'ArtistName2': 'CountryCode'}"
        ),
        'age': (
            "For the following artists, provide their approximate ages. "
            "If age is unknown, use 'NA'. "
            "Respond ONLY with a valid JSON in this format: "
            "{'ArtistName1': Age, 'ArtistName2': Age}"
        )
    }
    
    prompt = (
        f"{data_prompts[data_type]} "
        f"Artists: {', '.join(artists)}"
    )
    
    try:
        logging.info(f"Sending prompt to Gemini for {data_type}")
        response = model.generate_content(prompt)
        logging.info(f"Received response: {response.text}")
        
        data = extract_json_from_response(response.text)
        
        if not data:
            logging.error(f"No valid JSON found for {data_type}")
            return {}
        
        return data
    
    except Exception as e:
        logging.error(f"Error retrieving {data_type} data: {e}")
        return {}

def get_venue_data(venues):
    """Retrieve venue types with improved JSON handling."""
    logging.info(f"Retrieving venue types for venues: {venues}")
    
    generation_config = {
        "temperature": 0.7,
        "top_p": 0.95,
        "top_k": 64,
        "max_output_tokens": 8192,
    }
    
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=generation_config,
    )
    
    prompt = (
        "Categorize these venues into types (bar, concert hall, club, festival, theater, etc.). "
        "If category is unknown, use 'NA'. "
        "Respond ONLY with a valid JSON in this format: "
        "{'VenueName1': 'Category', 'VenueName2': 'Category'}"
        f"Venues: {', '.join(venues)}"
    )
    
    try:
        logging.info("Sending venue data prompt to Gemini")
        response = model.generate_content(prompt)
        logging.info(f"Received venue response: {response.text}")
        
        venue_types = extract_json_from_response(response.text)
        
        if not venue_types:
            logging.error("No valid JSON found for venues")
            return {}
        
        return venue_types
    
    except Exception as e:
        logging.error(f"Error retrieving venue types: {e}")
        return {}

def enrich_data(df, api_key):
    """Enrich DataFrame with additional information."""
    configure_gemini_api(api_key)
    
    # Create metadata directory if it doesn't exist
    os.makedirs('metadata', exist_ok=True)
    logging.info("Metadata directory created/verified")
    
    # Log DataFrame info
    logging.info(f"DataFrame shape: {df.shape}")
    logging.info(f"DataFrame columns: {list(df.columns)}")
    
    artists = list(set(df['artistName']))
    venues = list(set(df['venueName']))
    
    logging.info(f"Unique artists count: {len(artists)}")
    logging.info(f"Unique venues count: {len(venues)}")
    
    nationalities = get_artist_data(artists, 'nationality')
    ages = get_artist_data(artists, 'age')
    venue_types = get_venue_data(venues)
    
    # Save metadata with error handling and logging
    def safe_save_json(data, filename):
        try:
            with open(filename, 'w') as f:
                json.dump(data, f, indent=2)
            logging.info(f"Successfully saved {filename}")
        except Exception as e:
            logging.error(f"Error saving {filename}: {e}")
    
    safe_save_json(nationalities, 'metadata/artist_nationalities.json')
    safe_save_json(ages, 'metadata/artist_ages.json')
    safe_save_json(venue_types, 'metadata/venue_types.json')
    
    # Map data to DataFrame
    df['nationality'] = df['artistName'].map(nationalities).fillna('NA')
    df['age'] = df['artistName'].map(ages).fillna('NA')
    df['venue_type'] = df['venueName'].map(venue_types).fillna('NA')
    
    # Binarization example
    df['is_international'] = df['nationality'].apply(lambda x: x != 'NA')
    
    logging.info("Data enrichment completed")
    return df

def main():
    try:
        # Load data
        logging.info("Attempting to load data")
        df = pd.read_csv('data_NY.csv')
        
        # Replace with your actual Gemini API key
        API_KEY = 'AIzaSyCnslAzMMLo_-iyywto80Kn0OcW-3tgfcw'
        
        # Enrich data
        enriched_df = enrich_data(df, API_KEY)
        
        # Save enriched data
        enriched_df.to_csv('enriched_data_NY.csv', index=False)
        
        logging.info("Data enrichment and saving complete!")
    
    except Exception as e:
        logging.error(f"An error occurred during data processing: {e}")

if __name__ == '__main__':
    main()

# Afficher les artistes qui on une nationalite != 'NA'
data_enri = pd.read_csv('enriched_data.csv')
nb_artistes_internationaux = data_enri[data_enri['nationality'] == 'NA'].shape[0]
print(f"Nombre d'artistes internationaux: {nb_artistes_internationaux}")