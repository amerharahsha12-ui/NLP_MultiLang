from idp_core.text_preprocessing import clean_text, chunk_text

def run_preprocessing_pipeline():
    print("=== Starting Document Preprocessing Pipeline ===")
    
    sample_text = """
    هذا عقد تجاري رسمي يتضمن شروط وأحكام البيع والتسليم. 
    This is a formal commercial contract containing terms and conditions. 
    Dies ist ein offizieller Handelsvertrag.
    """
    
    cleaned = clean_text(sample_text)
    chunks = chunk_text(cleaned, chunk_size=15, overlap=3)
    
    print(f"-> Original Text: {sample_text.strip()}")
    print(f"-> Generated Chunks Count: {len(chunks)}")
    for idx, chunk in enumerate(chunks, 1):
        print(f"   [Chunk {idx}]: {chunk}")
        
    print("=== Preprocessing Pipeline Completed Successfully! ===")

if __name__ == "__main__":
    run_preprocessing_pipeline()
