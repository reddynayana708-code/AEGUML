from backend.preprocess import clean_text

def test_clean_text_basic():
    text = "Running, runs! Runner's run."
    out = clean_text(text)
    # Should be lowercase, no punctuation, stopwords removed, lemmatized
    assert "running" in out or "run" in out
    assert "," not in out and "!" not in out
