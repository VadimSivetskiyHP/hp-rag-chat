import nltk

from app.config import CHUNK_SIZE


def chunk_text(text):

    sentences = nltk.sent_tokenize(text)

    chunks = []

    current_chunk = []
    current_length = 0


    for sentence in sentences:

        sentence_length = len(sentence)


        # If adding this sentence exceeds chunk size,
        # save the current chunk and start a new one
        if current_length + sentence_length > CHUNK_SIZE:

            if current_chunk:
                chunks.append(
                    " ".join(current_chunk)
                )

            current_chunk = []
            current_length = 0


        current_chunk.append(sentence)
        current_length += sentence_length


    # Add remaining sentences
    if current_chunk:
        chunks.append(
            " ".join(current_chunk)
        )


    return chunks