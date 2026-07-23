from retriever import search
from llm import generate_answer
from config import DEBUG_MODE


def display_sources(results):

    print()
    print("=" * 60)
    print("Retrieved Sources (Debug Mode)")
    print("=" * 60)

    for i, result in enumerate(results, start=1):

        print()
        print(f"Result {i}")
        print(f"Source      : {result['source']}")
        print(f"Chunk ID    : {result['chunk_id']}")
        print(f"Similarity : {result['similarity']:.4f}")

        print()

        print(result["text"])

        print("-" * 60)



def display_citations(results):

    print()
    print("Sources:")

    unique_sources = set()

    for result in results:
        unique_sources.add(
            result["source"]
        )

    for source in unique_sources:
        print(f"- {source}")



def main():

    print("=" * 60)
    print("HP Local RAG Assistant")
    print("=" * 60)

    print()

    if DEBUG_MODE:
        print("Debug Mode: ON")

    else:
        print("Debug Mode: OFF")

    print()
    print("Ask questions about your documents.")
    print("Type 'exit' to quit.")
    print()


    while True:

        question = input(
            "Question: "
        )


        if question.lower() == "exit":

            print()
            print("Goodbye!")
            break


        if not question.strip():
            continue


        results = search(
            question
        )


        if not results:

            print()
            print("=" * 60)
            print("No Relevant Documents Found")
            print("=" * 60)

            print(
                "I could not find relevant information in the knowledge base."
            )

            print()
            continue


        if DEBUG_MODE:
            display_sources(
                results
            )


        context = "\n".join(
            [
                result["text"]
                for result in results
            ]
        )


        answer = generate_answer(
            context,
            question
        )


        print()
        print("=" * 60)
        print("Generated Answer")
        print("=" * 60)

        print(answer)


        display_citations(
            results
        )

        print()



if __name__ == "__main__":
    main()