import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000

#fixes - typos (corus instead of corpus), used weights in with probability, forgot to return sample_pagerank, messy logic in transition model, formatting cleanup. 
#notes for future, in py [0] always returns first item, don't forget that. use the formula they provide. 

def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.
    """
    n = len(corpus)
    links = corpus[page] if corpus[page] else corpus.keys()

    probkb = {}
    for p in corpus:
        probkb[p] = (1 - damping_factor) / n
        if p in links:
            probkb[p] += damping_factor / len(links)

    return probkb


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to the transition model, starting with a page at random.
    """
    pagerank = {page: 0 for page in corpus}

    page = random.choice(list(corpus.keys()))

    for _ in range(n):
        pagerank[page] += 1
        model = transition_model(corpus, page, damping_factor)
        pages = list(model.keys())
        probabilities = list(model.values())
        page = random.choices(pages, weights=probabilities, k=1)[0]

    normalized_pagerank = {page: pagerank[page] / n for page in pagerank}
    return normalized_pagerank


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.
    """
    n = len(corpus)
    pagerank = {page: 1 / n for page in corpus}
    threshold = 0.001

    while True:
        new_pagerank = {}
        for page in corpus:
            total = (1 - damping_factor) / n
            for p in corpus:
                if corpus[p]:
                    if page in corpus[p]:
                        total += damping_factor * pagerank[p] / len(corpus[p])
                else:
                    total += damping_factor * pagerank[p] / n
            new_pagerank[page] = total

        converged = all(abs(new_pagerank[p] - pagerank[p]) < threshold for p in pagerank)
        if converged:
            break
        pagerank = new_pagerank.copy()

    return new_pagerank


if __name__ == "__main__":
    main()
