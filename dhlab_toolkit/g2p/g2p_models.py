#%% 
from pathlib import Path
from google.cloud import storage
import phonetisaurus
import logging

logging.basicConfig(level=logging.INFO)


def download_g2p_model(dialect='e', style= "written"):
    """
    Download a pre-trained g2p model for a given language.
    """
    filename = f"nb_{dialect}_{style}.fst"
    download_dir = Path.home() / ".cache" / "dhlab_toolkit" 
    download_dir.mkdir(parents=True, exist_ok=True)
    download_path = download_dir / filename
    
    if not download_path.exists():        
        try:
            client = storage.Client()
            bucket_name = "g2p-models"
            bucket = client.get_bucket(bucket_name)
            blob = bucket.blob(filename)
            blob.download_to_filename(download_path)
            logging.debug("Download successful.")
        except Exception as e:
            logging.error(e)
            logging.info(f'No pre-trained g2p model available for {dialect} {style}.')
    
    logging.debug(f"Path to the G2P model: {download_path}.")
    return download_path


def transcribe(words, dialect='e', style= "written"):
    """
    Transcribe a list of words using a pre-trained g2p model.
    """
    model_path = download_g2p_model(dialect=dialect, style=style)
    transcriptions = phonetisaurus.predict(words, model_path = model_path)
    return transcriptions


if __name__ == "__main__":
    #download_g2p_model(dialect='n', style= "written")
    result = transcribe(["I", "Nasjonalbiblioteket", "har", "vi", "veldig", "mange", "gamle", "og", "sjeldne", "bøker"])
    for word, pronunciation in result:
        print(f"{word}\t{' '.join(pronunciation)}")
        
# %%
