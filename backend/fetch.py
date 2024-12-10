import time
from datasets import load_dataset

def main():
    dataset = load_dataset("wykonos/movies")
    dataset['train'].to_csv("../data/movies_dataset.csv", index=False)


if __name__=="__main__":
    start_time = time.time()

    main()

    run_time = time.time() - start_time
    print(f"Finished fetching in {run_time}s")
