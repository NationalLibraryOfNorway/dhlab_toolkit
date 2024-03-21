#%% 
from pathlib import Path
from google.cloud import storage
import phonetisaurus
import logging


def download_public_file(bucket_name, source_blob_name, destination_file_name):
    """Downloads a public blob from the bucket."""
    # bucket_name = "your-bucket-name"
    # source_blob_name = "storage-object-name"
    # destination_file_name = "local/path/to/file"

    storage_client = storage.Client.create_anonymous_client()

    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(source_blob_name)
    blob.download_to_filename(destination_file_name)



def download_g2p_model(dialect='e', style= "written"):
    """
    Download a pre-trained g2p model for a given language.
    """
    filename = f"nb_{dialect}_{style}.fst"
    download_dir = Path.home() / ".cache" / "dhlab_toolkit" 
    download_dir.mkdir(parents=True, exist_ok=True)
    download_path = download_dir / filename
    bucket_name = "g2p-models"
    
    if not download_path.exists():        
        try:
            download_public_file(bucket_name, filename, download_path)
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
    logging.basicConfig(level=logging.DEBUG)

    download_g2p_model(dialect='t', style= "written")
    #result = transcribe(["I", "Nasjonalbiblioteket", "har", "vi", "veldig", "mange", "gamle", "og", "sjeldne", "bøker"])
    #for word, pronunciation in result:
     #   print(f"{word}\t{' '.join(pronunciation)}")
    
# %%
