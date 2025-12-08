from database import repository
from rag import context_builder, llm_engine

if __name__ == "__main__":
    repository.test_connection()
    print("\n=== NarutoGPT (RAG) ===")
    
    while True:
        try:
            q = input("\nAsk anything: ")
            if q.lower() in ["exit", "quit"]: 
                print("Jaa ne! 👋")
                break
            
            ctx = context_builder.build_context(q)
            
            print(f"\n[Context Retrieved]: {ctx[:100]}...\n") 
            
            llm_engine.generate_answer(ctx, q)
            
        except KeyboardInterrupt:
            print("\nForce Quit.")
            break
        except Exception as e:
            print(f"Error: {e}")