"""
Markdown Wiki Maker — embedding-hybrid chunker.

Structure-agnostic alternative to md.py: chunks large markdown by paragraph-block
embedding distance (Method A) confirmed by single-boundary LLM calls
(Method B / LumberChunker-style), instead of LLM keyhole partitioning.

Run:
    python md2.py
"""

from wiki_embed.phases import main

if __name__ == "__main__":
    main()
