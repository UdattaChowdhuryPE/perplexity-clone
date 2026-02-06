from orchestrator import answer_user

def main():
    print("Perplexity-style Agent (CLI)")
    while True:
        user_query = input("\nAsk a question (or 'exit'): ")
        if user_query.lower() == "exit":
            break
        answer = answer_user(user_query)
        print("\nANSWER:\n", answer)

if __name__ == "__main__":
    main()
