PCR Amplification
=====================

.. |degC| unicode:: U+00B0 C
   :ltrim:

General Protocol
--------------------

This protocol describes the general procedure to conduct PCR experiment.
Optimal reaction conditions vary and need to be optimized. 

.. note::

    PCR reactions should be assembled in a DNA-free environment.
    Use of "clean" dedicated automatic pipettors and aerosol resistant barrier tips
    are recommended. Always keep the control DNA and other templates to be
    amplified isolated from the other components. [1]_


Objective
~~~~~~~~~~~~~~~~~~

Amplify a DNA segment from tmplates.


Experiment Principle
~~~~~~~~~~~~~~~~~~~~~~~~~

PCR is based on the natural process of DNA replication. It involves the enzymatic
amplification of a specific DNA sequence using a pair of primers and a DNA polymerase
enzyme. The process can produce millions to billions of copies of a particular
DNA sequence from a small initial sample, making it possible to analyze DNA
even when only a very small amount is available. 


Materials and Reagents
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Reaction Buffer

- DNA polymerase

- dNTPs

- Forward and Reverse Primers

- Template DNA

- Nuclease-free Water


Procedure
~~~~~~~~~~~~~~~~~

1. Assemble reaction components

.. attention::

    Assemble all reaction components on ice and quickly transferring the
    reactions to a thermocycler preheated to the denaturation temperature.

.. note::

    Gently mix the reaction. Collect all liquid to the bottom of the tube by
    a quick spin if necessary. Overlay the sample with mineral oil if using
    a PCR machine without a heated lid.

2. Seting reaction thermal cycle

===================== ======================================= ==========================================
Step                  Temp                               Time
===================== ======================================= ==========================================
Initial Denaturation  95 |degC|                               5 min
Denaturation Cycle    95 |degC|                               30 s
Anneal                40-70 |degC| (depended on Primer)       30 s 
Extension Cycle       72 |degC| (depended on DNA polymerase)  30 s (evaluate by extension speed)    
Final Extension       72 |degC|                               5 min
Hold                  4-10 |degC|                             Any
===================== ======================================= ==========================================

3. Validate the PCR products

Use gel eletrophoresis to validate the PCR products.


References
-----------------

.. [1] https://tools.thermofisher.com/content/sfs/manuals/taqnative_pps.pdf

https://www.neb.com/en-sg/protocols/0001/01/01/taq-dna-polymerase-with-standard-taq-buffer-m0273

https://assets.thermofisher.com/TFS-Assets/LSG/manuals/MAN0012027_TaqDNAPolymerase_recombinant_5_UuL_500U_UG.pdf
