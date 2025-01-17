Terms in Bioinformatics
===============================================

The terms or concepts is not well defined in bioinformatics.
Sametimes, same terms can reprent different concepts. For example,
The term 'coverage', the term can refer to the read coverage along 
a sequence, or the depth of base covered a defined segement of
sequence. The ambiguous terms usage in bioinformatics often can confusion
for peoples not familar in the field. Even peoples work in the field.

Following is the explaination from ChatGPT of why ambiguity of terms in bioinformatics
happen.

--------------------------

    Many terms in bioinformatics are not rigorously or universally defined, which can sometimes cause confusion. This is partly because the field is highly interdisciplinary and rapidly evolving, with researchers from diverse backgrounds (biology, computer science, mathematics, etc.) contributing their own terminologies and practices. Here are some reasons why this happens:

    1. Lack of Standardization

        Reason: Bioinformatics covers a broad range of applications, from genome assembly to RNA-seq analysis, and different tools or communities may define the same term differently.
        Example: Terms like coverage, pileup, or mapping quality can mean slightly different things depending on whether you're working with DNA-seq, RNA-seq, or ChIP-seq.

    2. Field-Specific Jargon

        Reason: Fields like transcriptomics, epigenomics, and proteomics have their own specialized tools and workflows, leading to unique definitions of shared terms.
        Example: In transcriptomics, "coverage" might refer to the proportion of exons sequenced, whereas in ChIP-seq, it could mean the number of reads overlapping a region of interest.

    3. Rapid Tool Development

        Reason: New tools are constantly developed, each with its own documentation, parameters, and naming conventions. Tool developers often use existing terms but adapt or redefine them for their specific context.
        Example: "Peak calling" in ChIP-seq focuses on transcription factor binding sites, but in ATAC-seq, it identifies accessible chromatin regions. Both use "peaks," but the biological interpretation differs.

    4. Informal Usage

        Reason: Scientists often prioritize functionality over precise language. Terms may be adopted informally or without consensus, leading to variability in usage.
        Example: "Alignment" and "mapping" are sometimes used interchangeably, even though they have subtle distinctions.

    5. Multi-disciplinary Nature

        Reason: Bioinformatics integrates biology, statistics, and computer science. Each discipline brings its own language, which can overlap or conflict.
        Example: In statistics, "normalization" might refer to standardizing data distribution, while in RNA-seq, it often means adjusting read counts to account for sequencing depth.

    6. Evolution of the Field

        Reason: As technologies like next-generation sequencing (NGS) and single-cell analysis advance, new terms and concepts emerge, and older ones get redefined.
        Example: The term "isoform" used to strictly mean splice variants of a gene, but with advancements in single-cell RNA-seq, it might now also refer to alternative polyadenylation events.

----------------------------


Here I try to define some term by my understanding.


Coverage
-----------



Cover Depth
----------------


Read density
-----------------



