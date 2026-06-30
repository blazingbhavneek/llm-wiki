"""
Global wiki generator.

Consumes per-document chunks from output_embed/ and writes one merged global
wiki to output_wiki/.

Run:
    python md_wiki.py
"""

from wiki_gen.phases import main

if __name__ == "__main__":
    main()
